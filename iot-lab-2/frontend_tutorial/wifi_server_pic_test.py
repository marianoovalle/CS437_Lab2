import socket
import gpiozero
import json
import time
import picar_4wd as fc
import speed
import threading
from picamera import PiCamera

HOST = "192.168.1.35" # IP address of your Raspberry PI
PORT = 65430          # Port to listen on (non-privileged ports are > 1023)
cpu = gpiozero.CPUTemperature()
#speed_thread = speed.Speed(25)
sp = 0
distance = 0
current_direction = "stop"
data = {}

fc.stop()

def move(direction):
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
#    x = 0
    for i in range(move_time):
        time.sleep(0.1)
        sp = speed_thread()
        if direction == "forward" or direction == "reverse":
            distance += int(sp /10)
        print("%smm/s"%sp)
    print("%smm"%distance)
    speed_thread.deinit()
    sp = 0
    current_direction = "stop"
    fc.stop()

def comms ():
    global current_direction
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()


        while 1:
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                direction = client.recv(1024)      # receive 1024 Bytes of message in binary format
                temp = cpu.temperature
                data ={ "direction" : str(current_direction),
                        "temp" : str(temp),
                        "speed" : str(sp),
                        "distance": str(distance)
                        }
                print (data)
                if str(direction.decode()) != "stop" :
                    m = threading.Thread(target=move, args=(str(direction.decode()),))
                    m.start()
                
                    
                ser_data = json.dumps(data)
                
                if data != b"":
                    print(ser_data)     
                    client.sendall(ser_data.encode()) # Echo back to client
         
    print("Closing socket")
    client.close()
    s.close()

def send_image():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (200, 120)
    time.sleep(0.1)
    camera.capture("image.jpg")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, 65001))
        s.listen()
        while 1:
            client, clientInfo = s.accept()
            print("camera server recv from: ", clientInfo)
        
            file = open("image.jpg", "rb")
            image_data = file.read(65536)
        
            while image_data:
                client.send(image_data)
                image_data = file.read(65336)
            
            
            file.close()
            client.close()
    
send_image()
x =threading.Thread(target=comms)
x.start()
x.join()


