import socket
import gpiozero
import json
import time
import picar_4wd as fc
import speed
import threading
from picamera import PiCamera

HOST = "192.168.1.35"  # IP address of your Raspberry PI
PORT = 65434  # Port to listen on (non-privileged ports are > 1023)
cpu = gpiozero.CPUTemperature()
sp = 0
distance = 0
current_direction = "stop"
data = {}

fc.stop()


def move_command(direction):
    """
    Function to execute PiCar move command and update speed and direction
    variables
    :param direction: move command forward, backward, turn_left or turn_right
    :return: None
    """
    global sp
    global distance
    global current_direction
    current_direction = direction
    speed_thread = speed.Speed(25)
    speed_thread.start()
    if direction == "forward":
        fc.forward(25)
        move_time = 40
    if direction == "reverse":
        fc.backward(25)
        move_time = 40
    if direction == "turn_left":
        fc.turn_left(25)
        move_time = 10
    if direction == "turn_right":
        fc.turn_right(25)
        move_time = 10

    for i in range(move_time):
        time.sleep(0.1)

        if direction == "forward" or direction == "reverse":
            distance += round(sp / 10)
            sp = speed_thread()
        print("%smm/s" % sp)
    print("%smm" % distance)
    speed_thread.deinit()
    sp = 0
    current_direction = "stop"
    fc.stop()


def wifi_server():
    """
    Wifi server, will receive information from the client to
    move Picar (forward, backward, turn left or turn right) and
    send information about the Picar status (CPU temperature,
    speed, distance and current movement)
    :return: None
    """
    global current_direction
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        try:
            while 1:
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                direction = client.recv(1024)  # receive 1024 Bytes of message in binary format
                temp = cpu.temperature
                data = {"direction": str(current_direction),
                        "temp": str(temp),
                        "speed": str(sp),
                        "distance": str(distance)
                        }
                print(data)
                if str(direction.decode()) != "stop":
                    move_thread = threading.Thread(target=move_command, args=(str(direction.decode()),))
                    move_thread.start()

                ser_data = json.dumps(data)

                if data != b"":
                    print(ser_data)
                    client.sendall(ser_data.encode())  # Echo back to client

        except:
            print("Closing socket")
            client.close()
            s.close()


server_thread = threading.Thread(target=wifi_server)
server_thread.start()
server_thread.join()
