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


def GPSInit():
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
    date = x[9]
    #while status == 'V':
        
    GPIO.output(enable, GPIO.LOW)
    
def get_speed():
    GPSInit()
    print ("{'Sensor':'speed', 'data':  %s '}\n" %speed)
    return

def get_lat():
    GPSInit()
    print ("{'Sensor':'Latitude', 'data':  %s '}\n" %Latitude)
    return

def get_long():
    GPSInit()
    print ("{'Sensor':'Longitude', 'data':  %s '}\n" %Longitude)
    return

def get_time():
    GPSInit()
    print ("{'Sensor':'UTC_time', 'data':  %s '}\n" %UTC_time)
    return

def get_course():
    GPSInit()
    print ("{'Sensor':'course', 'data':  %s ' }\n"%course)
    return 

def get_date():
    GPSInit()
    print ("{'Sensor':'date', 'data':  %s '}\n" %date)
    return
def get_status():
    GPSInit()
    print ("{'Sensor':'status', 'data':  %s '}\n" %status)
    return

get_speed()
get_date()
get_time()
get_long()
get_lat()
get_status()


