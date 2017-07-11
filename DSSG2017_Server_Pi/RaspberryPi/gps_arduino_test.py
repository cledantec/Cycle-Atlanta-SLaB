import serial
from datetime import datetime
import time
import termios
import os


path = '/dev/ttyUSB0'
	
with open(path) as f:
	attrs = termios.tcgetattr(f)
	attrs[2] = attrs[2] & ~termios.HUPCL
	termios.tcsetattr(f, termios.TCSAFLUSH, attrs)

#GPS
ser2 = serial.Serial(
	port=path,
	baudrate=9600,
   	parity=serial.PARITY_NONE,
    	stopbits=serial.STOPBITS_ONE,
    	bytesize=serial.EIGHTBITS		
	)

path2 = '/dev/ttyUSB1'

with open(path2) as f:
	attrs = termios.tcgetattr(f)
	attrs[2] = attrs[2] & ~termios.HUPCL
	termios.tcsetattr(f, termios.TCSAFLUSH, attrs)

# sensor
ser = serial.Serial(
	port = path2,
	baudrate = 9600,
	parity=serial.PARITY_EVEN,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.SEVENBITS
	)


def GPSread():
    ser2.flushInput()
    global UTC_time
    global status 
    global Latitude 
    global NS_indicator 
    global Longitude 
    global EW_indicator 
    global speed 
    global course 
    global date 
    while 1:
        x=ser2.readline()
        if '$GPRMC' in x :
            break
    x = x.split(',')
    UTC_time = x[1]
    status = x[2]
    Latitude = x[3]
    NS_indicator = x[4]
    Longitude = x[5]
    EW_indicator = x[6]
    speed = x[7]
    course = x[8]
    day = x[9]
    #while status == 'V':
        
    GPSoutput = {"speed": speed, "lat": Latitude, "long": Longitude, "utc_time": UTC_time, "day": day, "course": course}
    return GPSoutput



while 1:
	ser.flushInput()
	x=ser.readline()
	print (x)
	print(GPSread())
	time.sleep(0.5)

