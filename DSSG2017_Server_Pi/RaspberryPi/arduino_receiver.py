import serial
import time
from datetime import datetime
import json
import requests
import os
import termios
from sys import exit
import signal

# Timeout (sec): for how long will Pi wait for Arduino?
TIME_OUT = 5

# Other constants
logFileName = '/home/pi/arduino_logs.log'
DELAY = 0.2 # In seconds

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

# Create a new log file for this trip
print ('Start new sensor file.')

arduino_path = '/dev/cycle_arduino'

ser = serial.Serial(
        port=arduino_path,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

# Setting timeout and timeout handler to prevent communication hiccups
# TimeourError is raised once Arduino does not respond, but the loop continues.
class TimeoutError(RuntimeError):
    pass

def handler(signum, frame):
    ser.write("f")
    time.sleep(1)
    raise TimeoutError()

signal.signal(signal.SIGALRM, handler)

try:
    # "f" is a signal indicating "fail" to reset Arduino
    # "g" is for requesting data from Arduino
    ser.write("f")
    ser.flushInput()
    ser.flush()

    while True:
        ser.write("g")

        try:
            # Setting timeout when reading the serial port
            signal.alarm(TIME_OUT)
            serialLine = ser.readline()
        except TimeoutError as ex:
            status = {}
            status["LidarLeft"] = False
            status["LidarRight"] = False
            status["USLeft"] = False
            status["USRight"] = False
            status["USRear"] = False
            status["CO"] = False
            status["SO"] = False
            status["O3"] = False
            status["NO"] = False
            status["P25"] = False
            status["P10"] = False
            jsonStatus = json.dumps(status)
            time.sleep(1)
            requests.post(STATUS_URL, data=jsonStatus, headers=headers)
            logFile = open(logFileName, 'a')
            logFile.write('Timeout Error... Resetting... \n')
            logFile.close()
            continue

        if "WIN" in serialLine:
            time.sleep(0.5)
            continue
        elif "nack" in serialLine or "NACK" in serialLine:
            ser.write("f")
            status = {}
            status["LidarLeft"] = False
            status["LidarRight"] = False
            status["USLeft"] = False
            status["USRight"] = False
            status["USRear"] = False
            status["CO"] = False
            status["SO"] = False
            status["O3"] = False
            status["NO"] = False
            status["P25"] = False
            status["P10"] = False
            jsonStatus = json.dumps(status)
            print("reset Arduino...")
            time.sleep(7)
            requests.post(STATUS_URL, data=jsonStatus, headers=headers)
            ser.flush()
            continue

        serialLine = serialLine.split()

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

        jsonData = json.dumps(arduinoData)

        # we're not using data here, but just pass to the REST API
        # dataFile = open('/home/pi/data/' + str(gpsData["day"]) + '_arduino_data.json','a')
        # dataFile.write(jsonData)
        # dataFile.write("\n")
        # dataFile.close()
        jsonStatus = json.dumps(status)

        try:
            response = requests.post(DATA_URL, data=jsonData, headers=headers)
            response2 = requests.post(STATUS_URL, data=jsonStatus, headers=headers)
        except requests.exceptions.RequestException:
            print ("ERROR in posting data to URLs...")
            time.sleep(5)
            ser.flushInput()
            ser.flush()
            continue
        else:
            if (response.status_code != requests.codes.ok):
                status = {}
                status["LidarLeft"] = False
                status["LidarRight"] = False
                status["USLeft"] = False
                status["USRight"] = False
                status["USRear"] = False
                status["CO"] = False
                status["SO"] = False
                status["O3"] = False
                status["NO"] = False
                status["P25"] = False
                status["P10"] = False
                jsonStatus = json.dumps(status)
                time.sleep(1)
                requests.post(STATUS_URL, data=jsonStatus, headers=headers)
                print ("Data posted but no response...")
            else:
                print ("Data posted successfully..")

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
