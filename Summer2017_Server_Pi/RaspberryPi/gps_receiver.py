import serial
import time
from datetime import datetime
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
logFileName = '/home/pi/gps_logs.log'
DELAY = 0.5 # In seconds

# Self
HOST_SERVER = '0.0.0.0'

# Network settings
headers = {'Content-type': 'application/json'}
STATUS_URL = 'http://' + HOST_SERVER + ':5000/gps_status'

logFile =  open(logFileName,'a')
logFile.close()

# Create a new log file for this trip
print ('Start new gps file.\n')

gps_path = '/dev/cycle_gps'
ser_gps = serial.Serial(gps_path, 9600)

with open(gps_path) as f:
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
        
    GPSoutput = {"speed": speed, "lat": Latitude, "long": Longitude, "utc_time": UTC_time, "day": day, "course": course}
    return GPSoutput


try:

    while True:

        #GPS Data
        gpsData = GPSread()
        status = {}

        try:
            if str(gpsData['long']) == '':
                status["GPS"] = False
            else:
                status["GPS"] = True

            status["utc_time"] = str(gpsData["day"]) + str(gpsData["utc_time"])
            gpsJsonData = json.dumps(gpsData)
            gpsFile = open('/home/pi/data/' + str(gpsData["day"]) + '_gps_data.json','a')
            gpsFile.write(gpsJsonData)
            gpsFile.write("\n")
            gpsFile.close()
        except Exception as e:
            status = {}
            status["GPS"] = "fail"
            jsonStatus = json.dumps(status)
            time.sleep(1)
            requests.post(STATUS_URL, data=jsonStatus, headers=headers)
            print (e)
            gpsFile = open('/home/pi/data/gps_error_log.log','a')
            gpsFile.write("GPS not working...\n")
            gpsFile.close()
            ser_gps.flush()
            continue

        jsonStatus = json.dumps(status)

        try:
            response2 = requests.post(STATUS_URL, data=jsonStatus, headers=headers)
        except requests.exceptions.RequestException:
            print ("ERROR in posting GPS to URLs...")
            time.sleep(7)
            status = {}
            status["GPS"] = "fail"
            jsonStatus = json.dumps(status)
            requests.post(STATUS_URL, data=jsonStatus, headers=headers)
            continue
        else:
            if (response2.status_code != requests.codes.ok):
                print("NO Response from GPS report...")
                time.sleep(7)
                status = {}
                status["GPS"] = "fail"
                jsonStatus = json.dumps(status)
                requests.post(STATUS_URL, data=jsonStatus, headers=headers)
            else:
                print ("GPS posted successfully..")

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
