import gpiozero
import json
from picamera import PiCamera
import time

camera = PiCamera()
camera.rotation = 180
camera.resolution = (640, 480)
time.sleep(1)

camera.capture("image.jpg")
print("done...")

# cpu = gpiozero.CPUTemperature()
# print(type(cpu.temperature))
# data ={}
# echo ="123"
# 
# temperature = cpu.temperature
# data ={ "echo" : echo,
#         "temp" : temperature
#         }
# ser_data = json.dumps(data)
# if data != b"":
#     print(ser_data)     