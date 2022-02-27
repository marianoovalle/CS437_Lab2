import bluetooth
import picar_4wd as fc
import time

hostMACAddress = "E4:5F:01:5D:21:CA" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 0
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
fc.stop()
print("listening on port ", port)
try:
    client, clientInfo = s.accept()
    while 1:   
        print("server recv from: ", clientInfo)
        data = client.recv(size)
        if data:
            print(data)
            client.send(data) # Echo back to client
            command = data.decode()
            if command == "forward":
                fc.forward(25)
                time.sleep(3)
            if command == "backward":
                fc.backward(25)
                time.sleep(3)
            if command == "turn right":
                fc.turn_right(25)
                time.sleep(1.5)
            if command == "turn left":
                fc.turn_left(25)
                time.sleep(1.5)
            fc.stop()
            
            
except: 
    print("Closing socket")
    client.close()
    s.close()

