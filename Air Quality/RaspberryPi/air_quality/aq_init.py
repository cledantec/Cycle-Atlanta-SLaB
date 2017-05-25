import RPi.GPIO as GPIO
import time
import os
import serial
import Adafruit_ADS1x15

#GPIO registers
enable = 23
trigger = 25
trigger_en = 24

#GPIO record/pause switch
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_en, GPIO.OUT)
GPIO.setup(trigger, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.output(trigger_en, GPIO.HIGH)

#GPIO + serial GPS setup
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

#ADS1115 ADC (16-bit) instance to read the gas array
gasArray = Adafruit_ADS1x15.ADS1015()
GAIN = 1
VxCO = 818
VxSO = 823
VxO = 812
VxNO = 810
COi = 0.00000000475
SOi = 0.000000025
Oi = 0.000000032
NOi = 0.000000040
# Or create an ADS1015 ADC (12-bit) instance.
#PMSense = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

#Read and decode GPS data
def GPSread():
    GPIO.output(enable, GPIO.HIGH)
    while 1:
#        if (ser.inWaiting()>0):
        x=ser.readline()
        if '$GPRMC' in x :
            #print x
            break
    x = x.split(',')
    GPSoutput = {"speed": x[7], "lat": x[3], "long": x[5], "utc_time": x[1], "day": x[9], "course": x[8]}
    return GPSoutput

#Read and decode Gas array    
def GasRead():
    #Read gas array values
    gasValues = [0]*4
    for i in range(4):
        gasValues[i] = float(gasArray.read_adc(i, gain=GAIN))
    #Decode gas values
    gasValues[0] = (gasValues[0] - VxCO)/(500000*COi)
    gasValues[1] = (gasValues[1] - VxSO)/(500000*SOi)
    gasValues[2] = (gasValues[2] - VxO)/(500000*Oi)
    gasValues[3] = (gasValues[3] - VxNO)/(500000*NOi)
    return gasValues

#Rotate json log file.
if os.path.isfile('/home/pi/data/aq_gps_current_trip.json'):
    file_count = len([name for name in os.listdir('/home/pi/data/aq_archive/') if os.path.isfile(name)])
    os.rename("/home/pi/data/aq_gps_current_trip.json","/home/pi/data/aq_archive/aq_gps_"+str(file_count+1)+".json")
#Create a new log file for this trip
dataFile = open('/home/pi/data/aq_gps_current_trip.json','a')
dataFile.write('Start new trip file')
dataFile.close

#Start the collection loop
while True:
    t = GPIO.input(trigger)
    #no-op while record switch is off
    while not t:
        t = GPIO.input(trigger)
        time.sleep(0.1)
        
    #execfile("/home/pi/air_quality/read_gas_array.py")
    #Read gas array values
    gas = GasRead()
    #Read gps
    gps = GPSread()

    #Write values to data file
    f = open("/home/pi/data/aq_gps_current_trip.json", "a+")
    f.write("{'Sensor':'GasArray CO', 'data':  %.2f ppm'}\n" %gas[0])
    f.write("{'Sensor':'GasArray SO', 'data':  %.2f ppm'}\n" %gas[1])
    f.write("{'Sensor':'GasArray O', 'data':  %.2f ppm'}\n" %gas[2])
    f.write("{'Sensor':'GasArray NO', 'data':  %.2f ppm'}\n" %gas[3])
    
    f.write(str(gps))
    f.write("\n")
    f.close()

    #Sleep
    time.sleep(4)
    

    


