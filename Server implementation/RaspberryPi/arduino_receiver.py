import csv
import serial
import time
from datetime import datetime
#import RPi.GPIO as GPIO
#from lidar_lite import Lidar_Lite
import json
import requests
import os
import termios
from sys import exit


# PIN assignments. Change if board connections change.
SWITCH_PIN = 29
ERROR_PIN = 31
STATUS_PIN = 33
NET_STATUS_PIN = 35

# Other constants
logFileName = 'proximity.log'
DELAY = 1 # In seconds


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
print ('Start new sensor file.')
dataFile.close

gpsFile = open('/home/pi/data/gps_data.json','a')
print ('Start new gps file.\n')
gpsFile.close


ser_gps = serial.Serial('/dev/ttyUSB0', 9600)

with open('/dev/ttyUSB0') as f:
	attrs = termios.tcgetattr(f)
	attrs[2] = attrs[2] & ~termios.HUPCL
	termios.tcsetattr(f, termios.TCSAFLUSH, attrs)


def GPSread():   
    ser_gps.flushInput()
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
        x=ser_gps.readline()
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


# status = True
try:
	path = '/dev/ttyUSB1'
	
	with open(path) as f:
		attrs = termios.tcgetattr(f)
		attrs[2] = attrs[2] & ~termios.HUPCL
		termios.tcsetattr(f, termios.TCSAFLUSH, attrs)

        ser = serial.Serial(
		port=path,
		baudrate=9600,
		parity=serial.PARITY_EVEN,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.SEVENBITS		
	)

        while True:
                ser.flushInput()
                ser.flush()
                serialLine=ser.readline()
                serialLine = serialLine.split()
                
                #GPS Data
                gpsData = GPSread()

                arduinoData = {}
                status = {}

                for i in range(1, len(serialLine)):
                    sensor = serialLine[i-1]
                    value = serialLine[i]

                    if sensor == "Lidar1":
                        arduinoData["LidarLeft"] = value
                        status["LidarLeft"] = True
                    elif sensor == "Lidar2":
                        arduinoData["LidarRight"] = value
                        status["LidarRight"] = True
                    elif sensor == "SONAR1":
                        arduinoData["USLeft"] = value
                        status["USLeft"] = True
                    elif sensor == "SONAR2":
                        arduinoData["USRight"] = value
                        status["USRight"] = True
                    elif sensor == "SONAR3":
                        arduinoData["USRear"] = value
                        status["USRear"] = True
                    elif sensor == "CO":
                        arduinoData["CO"] = value
                        status["CO"] = True
                    elif sensor == "SO":
                        arduinoData["SO"] = value
                        status["SO"] = True
                    elif sensor == "O3":
                        arduinoData["O3"] = value
                        status["O3"] = True
                    elif sensor == "NO":
                        arduinoData["NO"] = value
                        status["NO"] = True
                    elif sensor == "P25":
                        arduinoData["P25"] = value
                        status["P25"] = True
                    elif sensor == "P10":
                        arduinoData["P10"] = value
                        status["P10"] = True                    
                
                print(arduinoData)
                
                try:
                    if str(gpsData['long']) == '':
	       	        status["GPS"] = True
	            else:    
                        status["GPS"] = False
                        
                    gpsJsonData = json.dumps(gpsData)
                    gpsFile = open('/home/pi/data/gps_data.json','a')
                    gpsFile.write(gpsJsonData)
                    gpsFile.close()
		except Exception as e:
		    print (e)
		    gpsFile = open('/home/pi/data/gps_data.json','a')
	            gpsFile.write("GPS not working...\n")
                    gpsFile.close()	
                
                
                timeNow=datetime.now()
                arduinoData.update({"proxTime": timeNow.strftime('%m-%d-%Y-%H-%M-%S')})

                if len(arduinoData) < 10:
                    print ("Could not write data at time " + str(timeNow) + " Arduino data: " + str(arduinoData) + "\n")                        
                    continue                        # Incomplete data

                jsonData = json.dumps(arduinoData)

                #write json data to local file first
                dataFile = open('/home/pi/data/arduino_data.json','a')
                dataFile.write(jsonData)
                dataFile.close()
                
                print (status)
                jsonStatus = json.dumps(status)
                
                # print jsonData 
                try:
                    # response = requests.post(DATA_URL, data=jsonData, headers=headers)
                    response2 = requests.post(STATUS_URL, data=jsonStatus, headers=headers)
                    print (response2.text)
                except requests.exceptions.RequestException:
                    print ("ERROR in posting data to URLs...")
                else:
                    if (response2.status_code != requests.codes.ok):
                            print ("Status posted but no response...")
                    else:
                            print ("Status posted successfully..")
                
                
	
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
        exit()
except Exception as e:
        logFile = open(logFileName,'a')
        logFile.write('Error: '+str(e) + ' stopping script. \n')
        logFile.close()
        exit()
