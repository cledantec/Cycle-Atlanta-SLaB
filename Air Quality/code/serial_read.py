import time
import serial
import RPi.GPIO as GPIO
enable = 23

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )

GPIO.setmode(GPIO.BCM)
GPIO.setup(enable, GPIO.OUT)


def GPSread():
    GPIO.output(enable, GPIO.HIGH)
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
        if '$GPRMC' in x :
            #print x
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
f = open("datalog.txt", "a+")
GPSread()
#if status == 'A':
#print GPSread()
f.write(str(GPSread()))
f.write("\n")
f.close()


