import time
import os
import serial


#ser = serial.Serial(
#	port='/dev/ttyUSB0', 
#    	baudrate=9600,
#    	parity=serial.PARITY_NONE,
#    	stopbits=serial.STOPBITS_ONE,
#    	bytesize=serial.EIGHTBITS	
#)
ser = serial.Serial('/dev/ttyUSB0', 9600)


def GPSread():
   
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
        x=ser.readline()
#	print (x)
        if '$GPRMC' in x :
#            print x
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

while True:
	print(GPSread())
	time.sleep(1)
#f = open("gps.json", "a+")
#GPSread()
#if status == 'A':
#print gpsString
#f.write(str(GPSread()))
#f.write("\n")
#f.close()
