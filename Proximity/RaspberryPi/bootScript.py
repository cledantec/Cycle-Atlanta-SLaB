import csv
import serial
import time
import datetime
import RPi.GPIO as GPIO
from lidar_lite import Lidar_Lite
import json
import requests

# PIN assignments. Change if board connections change.
SWITCH_PIN = 29
ERROR_PIN = 31
STATUS_PIN = 33
NET_STATUS_PIN = 35

# Other constants
logFileName = 'proximity.log'
DELAY = 0.1 # In seconds

# Configure GPIO        
GPIO.setmode(GPIO.BOARD);
GPIO.setup(SWITCH_PIN, GPIO.IN)
GPIO.setup(ERROR_PIN,GPIO.OUT)
GPIO.setup(STATUS_PIN,GPIO.OUT)
GPIO.output(ERROR_PIN,True)                                                     # Make it alive only if loop starts running.
GPIO.setup(NET_STATUS_PIN,GPIO.OUT)
GPIO.output(NET_STATUS_PIN,0)

# JSON Labels.
jsonDataLabels = ['proxTime','UltrasoundLeft','UltrasoundRight','LidarLeft','LidarRight']
jsonStatusLabels = ['usLeftStatus','usRightStatus','lidarLeftStatus','lidarRightStatus','diskWriteStatus']
statusList = [0]*5

# Network settings
headers = {'Content-type': 'application/json'}
DATA_URL = 'http://192.168.1.10:5000/proximity'
STATUS_URL = 'http://192.168.1.10:5000/status'

# Open a file with a name appended with current time.
timeNow=datetime.datetime.now()
fileTime=timeNow.strftime('%m-%d-%Y-%H-%M-%S')

logFile =  open(logFileName,'a')
logFile.write('Starting script at '+fileTime+'\n')
logFile.close()

status = True
try:
        ser=serial.Serial(port='/dev/ttyACM0',baudrate=4800)
        lidar=Lidar_Lite()
        connected=lidar.connect(1)
        if connected<-1:
                raise valueError('Lidar not connected.')
        while True:
                GPIO.output(ERROR_PIN,True)                                     # If this is alive, then it means loop is running.
                switchState = GPIO.input(SWITCH_PIN)
                if switchState:                                                 # This means you have to record. 
                        GPIO.output(STATUS_PIN,status)
                        status = not status
                        ser.flushInput()
                        ser.flush()
                        serialLine=ser.readline()
                        lidarData=lidar.getDistance()
                        arduinoData=serialLine.split()

                        timeNow=datetime.datetime.now()
                        dataTime=timeNow.strftime('%m-%d-%Y-%H-%M-%S')
                        if len(arduinoData) !=3:
                                logFile = open(logFileName,'a')
                                logFile.write("Could not write data at time " + str(dataTime))
                                logFile.close()
                                continue                        # Incomplete data
                        dataList = [dataTime] + arduinoData + [lidarData]
                        #print dataList
                        dataFile = open('/home/pi/data/data_'+fileTime+'.csv','a')
                        dataWriter = csv.writer(dataFile)
                        dataWriter.writerow(dataList)
                        dataFile.close()
                        jsonData = json.dumps(dict(zip(jsonDataLabels,dataList)))

                        
                        statusList = [(lidarData>0),(arduinoData[0] != '0'),(arduinoData[1] != '0'),(arduinoData[2] != '0'),(switchState==1)]
                        statusList  = [str(x).lower() for x in statusList]
                        jsonStatus = json.dumps(dict(zip(jsonStatusLabels,statusList)))
                        #print jsonStatus
                        try:
                            response = requests.post(DATA_URL, data=jsonData, headers=headers)
                            response2 = requests.post(STATUS_URL, data=jsonStatus, headers=headers)
                            print response2.text
                        except requests.exceptions.RequestException:
                                GPIO.output(NET_STATUS_PIN,1)
                        else:
                                if (response.status_code != requests.codes.ok) or (response2.status_code != requests.codes.ok):
                                        GPIO.output(NET_STATUS_PIN,1)
                                else:
                                        GPIO.output(NET_STATUS_PIN,0)
                else:
                        GPIO.output(STATUS_PIN,0)                               # Flash LED different way here (IDLE)
                        statusList = [False]*5
                        statusList  = [str(x).lower() for x in statusList]
                        jsonStatus = json.dumps(dict(zip(jsonStatusLabels,statusList)))
                        #print jsonStatus
                        try:
                            response2 = requests.post(STATUS_URL, data=jsonStatus, headers=headers)
                            print response2.text
                        except requests.exceptions.RequestException:
                                GPIO.output(NET_STATUS_PIN,1)
                        else:
                                if (response2.status_code != requests.codes.ok):
                                        GPIO.output(NET_STATUS_PIN,1)
                                else:
                                        GPIO.output(NET_STATUS_PIN,0)

                #time.sleep(DELAY)
                
except KeyboardInterrupt:
        logFile = open(logFileName,'a')
        logFile.write('Script stopped manually. \n')
        logFile.close()
except Exception as e:
        logFile = open(logFileName,'a')
        logFile.write('Error: '+str(e) + ' stopping script. \n')
        logFile.close()
GPIO.output(ERROR_PIN,False)
GPIO.cleanup()
#logFile.close()
#dataFile.close()
                                        # Close it on the way out.
