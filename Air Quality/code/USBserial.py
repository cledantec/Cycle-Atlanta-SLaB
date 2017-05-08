import serial
import time

#USBser = serial.Serial('/dev/ttyACM1', 9600, timeout = 2)
USBser = serial.Serial('/dev/serial/by-id/usb-Teensyduino_USB_Serial_1520210-if00',
                        baudrate = 9600,
                        timeout =2)

#print USBser.is_open()
#USBser.close()
#USBser.open()
while True:
    
    USBser.flushInput()
    #USBser.flush()
    #time.sleep(0.1)
    read_data = USBser.readline()
    print read_data
    #USBser.close()
    #time.sleep(1)
    execfile("serial_read.py")
    execfile("i2c.py")
    
