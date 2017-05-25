###########################
### Particulate Matter ####
###########################

import serial
import time
import RPi.GPIO as GPIO
import json
import requests
import subprocess
import ast
# Import the ADS1x15 module.
import Adafruit_ADS1x15
jsonStatusLabels = ["gas","gps"]

proc = subprocess.Popen(['ls /dev/ttyACM*'], stdout=subprocess.PIPE, shell=True)
(out,err) = proc.communicate()
print(out.strip())
USBser = serial.Serial('/dev/ttyACM0', 9600)
url = 'http://192.168.1.10:5000/gas'
url2 = 'http://192.168.1.10:5000/gps'
statusurl = 'http://192.168.1.10:5000/status'
headers = {'Content-type': 'application/json'}
def getpm():
    USBser.flushInput()
    USBser.flush()
    read_data = USBser.readline()
    #data is already in json
    pmdata = ast.literal_eval(read_data)
    return pmdata['data']
#############################
########## GPS ##############
#############################
gps = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )
enable = 23

trigger = 25
trigger_en = 24#will remain high and connected to trigger via the switch

GPIO.setmode(GPIO.BCM)
GPIO.setup(enable, GPIO.OUT)
GPIO.setup(trigger_en, GPIO.OUT)
GPIO.setup(trigger, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.output(enable, GPIO.HIGH)#turn enable high for duration of program
GPIO.output(trigger_en, GPIO.HIGH)#high for duration of program
def GPSRead():
    
    global UTC_time
    global status 
    global Latitude 
    global NS_indicator 
    global Longitude 
    global EW_indicator 
    global speed 
    global course 
    global day
    while True:
        x=gps.readline()
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

    GPSoutput = {"speed": speed, "lat": Latitude, "long": Longitude, "utc_time": UTC_time, "day": day, "course": course}
    return GPSoutput
    #GPIO.output(enable, GPIO.LOW)

#############################
########## Gas Array ########
#############################

# Create an ADS1115 ADC (12-bit) instance.
gasArray = Adafruit_ADS1x15.ADS1015()
GAIN = 1

#Low limit for each sensor @ Vx ppm = 0
VxCO = 818
VxSO = 823
VxO = 812
VxNO = 810
#amount of current output for each ppm
COi = 0.00000000475
SOi = 0.000000025
Oi = 0.000000032
NOi = 0.000000040

def getgas():
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = float(gasArray.read_adc(i, gain=GAIN))
    #compute conversion        
    values[0] = (values[0] - VxCO)/(500000*COi)
    values[1] = (values[1] - VxSO)/(500000*SOi)
    values[2] = (values[2] - VxO)/(500000*Oi)
    values[3] = (values[3] - VxNO)/(500000*NOi)

    gasarray = {"co":round(values[0], 2), "so2":round(values[1], 2), "o3":round(values[2], 2), "no2":round(values[3],2)}#, "pm":getpm()}
    return (json.dumps(gasarray))
##    print ("{'Sensor':'GasArray CO', 'data':  %.2f'}\n" %values[0])  
##    print ("{'Sensor':'GasArray SO', 'data':  %.2f'}\n" %values[1])   
##    print ("{'Sensor':'GasArray O', 'data':  %.2f'}\n" %values[2])
##    print ("{'Sensor':'GasArray NO', 'data':  %.2f'}\n" %values[3])

# Main loop.
while True:
    #read trigger pin(enable internal pull down)
    t = GPIO.input(trigger)
    #loop while pin is low (continue to read pin and delay)
    while not t:
        t = GPIO.input(trigger)
        try:
            statusList = ["false","false"]
            statusData = json.dumps(dict(zip(jsonStatusLabels,statusList)))
            response2 = requests.post(statusurl, data=statusData, headers=headers)
            print(response2.content)
        except Exception:
            pass
    GPSRead()
    try:
        if status == 'A':
           response2 = requests.post(url2, data = GPSRead(), headers = headers)
           print(response2.content)
    except Exception:
        pass
    #print str(getgas())
    try:
        response = requests.post(url, data=getgas(), headers=headers)
        print(response.content)
    except Exception:
        pass
    statusList = ["true",str(status == 'A').lower()]
    statusData = json.dumps(dict(zip(jsonStatusLabels,statusList)))
    try:
        response2 = requests.post(statusurl, data=statusData, headers=headers)
        print(response2.content)
    except Exception:
        pass
   # time.sleep (4)
    

