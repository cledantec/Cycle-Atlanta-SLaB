import serial
import time

USBser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    USBser.flushInput()
    USBser.flush()
    read_data = USBser.readline()
    print read_data
    #time.sleep(1)
