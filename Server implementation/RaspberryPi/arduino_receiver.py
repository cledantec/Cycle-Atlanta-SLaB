import csv
import serial
import time
from datetime import datetime
#import RPi.GPIO as GPIO
#from lidar_lite import Lidar_Lite
import json
import requests
import os

# This file receives sensor data from Arduino board.
# Also, collect data from GPS.
# Both of them are coming directly from serial ports.

# PIN assignments. Change if board connections change.
SWITCH_PIN = 29
ERROR_PIN = 31
STATUS_PIN = 33
NET_STATUS_PIN = 35

# Other constants
logFileName = 'proximity.log'
DELAY = 1 # In seconds

# Configure GPIO        
#GPIO.setmode(GPIO.BOARD);
# GPIO.setup(SWITCH_PIN, GPIO.IN)
# GPIO.setup(ERROR_PIN,GPIO.OUT)
# GPIO.setup(STATUS_PIN,GPIO.OUT)
# GPIO.output(ERROR_PIN,True)                                                     # Make it alive only if loop starts running.
# GPIO.setup(NET_STATUS_PIN,GPIO.OUT)
# GPIO.output(NET_STATUS_PIN,0)

# JSON Labels.
jsonDataLabels = ['proxTime','USLeft','USRight','LidarLeft','LidarRight','CO','SO','O3','NO','P25','P10']
jsonStatusLabels = ['usLeftStatus','usRightStatus','lidarLeftStatus','lidarRightStatus','COstatus','SOstatus','O3status','NOsstatus','P25status','P10status','diskWriteStatus']
statusList = [0]*11

# Self
HOST_SERVER = '0.0.0.0'

# Network settings
headers = {'Content-type': 'application/json'}
DATA_URL = 'http://' + HOST_SERVER + ':5000/proximity'
STATUS_URL = 'http://' + HOST_SERVER + ':5000/status'

# Open a file with a name appended with current time.
timeNow=datetime.now()
fileTime=timeNow.strftime('%m-%d-%Y-%H-%M-%S')

logFile =  open(logFileName,'a')
logFile.write('Starting script at '+fileTime+'\n')
logFile.close()

#Create a new log file for this trip
dataFile = open('/home/pi/data/arduino_data.json','a')
print ('Start new trip file.\n')
dataFile.close

# status = True
try:
        ser = serial.Serial(port='/dev/ttyUSB1',baudrate=9600)

        while True:
                ser.flushInput()
                ser.flush()
                serialLine=ser.readline()
                serialLine = serialLine.split()

                arduinoData = {}

                for i in range(1, len(serialLine)):
                    sensor = serialLine[i-1]
                    value = serialLine[i]

                    if sensor == "Lidar1":
                        arduinoData["LidarLeft"] = value
                    elif sensor == "Lidar2":
                        arduinoData["LidarRight"] = value
                    elif sensor == "SONAR1":
                        arduinoData["USLeft"] = value
                    elif sensor == "SONAR2":
                        arduinoData["USRight"] = value
                    elif sensor == "CO":
                        arduinoData["CO"] = value
                    elif sensor == "SO":
                        arduinoData["SO"] = value
                    elif sensor == "O3":
                        arduinoData["O3"] = value
                    elif sensor == "NO":
                        arduinoData["NO"] = value
                    elif sensor == "P25":
                        arduinoData["P25"] = value
                    elif sensor == "P10":
                        arduinoData["P10"] = value
                    else:
                        continue

                timeNow=datetime.now()
                arduinoData.update({"proxTime": timeNow.strftime('%m-%d-%Y-%H-%M-%S')})

                if len(arduinoData) < 10:
                    print ("Could not write data at time " + str(dataTime) + " Arduino data: " + ''.join(arduinoData) + "\n")                        
                    continue                        # Incomplete data

                jsonData = json.dumps(arduinoData)

                #write json data to local file first
                dataFile = open('/home/pi/data/arduino_data.json','a')
                dataFile.write(jsonData)
                dataFile.close()

                # statusList = [0,(arduinoData[0] != '0'),(arduinoData[1] != '0'),(arduinoData[2] != '0'),(arduinoData[3] != '0'), 0]
                # statusList  = [str(x).lower() for x in statusList]
                # jsonStatus = json.dumps(dict(zip(jsonStatusLabels,statusList)))

                print jsonData 
                try:
                    response = requests.post(DATA_URL, data=jsonData, headers=headers)
                    # response2 = requests.post(STATUS_URL, data=jsonStatus, headers=headers)
                    print response.text
                except requests.exceptions.RequestException:
                    print "ERROR in posting data to URLs..."
                else:
                    if (response.status_code != requests.codes.ok):
                            print "Data and Status posted but no response..."
                    else:
                            print "Data and Status posted successfully.."
                # else:
                #         statusList = [False]*5
                #         statusList  = [str(x).lower() for x in statusList]
                #         jsonStatus = json.dumps(dict(zip(jsonStatusLabels,statusList)))
                #         #print jsonStatus
                #         try:
                #             response2 = requests.post(STATUS_URL, data=jsonStatus, headers=headers)
                #             print response2.text
                #         except requests.exceptions.RequestException:
                #                 print "Error in posting data to Status URL..."
                #         else:
                #                 if (response2.status_code != requests.codes.ok):
                #                         print "Status posting successful."
                #                 else:
                #                         print "Status posted but no response..."

                time.sleep(DELAY)
                
except KeyboardInterrupt:
        logFile = open(logFileName,'a')
        logFile.write('Script stopped manually. \n')
        logFile.close()
except Exception as e:
        logFile = open(logFileName,'a')
        logFile.write('Error: '+str(e) + ' stopping script. \n')
        logFile.close()
