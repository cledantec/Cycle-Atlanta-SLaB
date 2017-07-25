# coding: utf-8
"""
This script collects data from three gas sensors from Arduino.

This code was written particularly for the testbed that will be co-located
in the Atlanta gas sensing station -- this is for fine-grained calibration.
The Arduino board is waiting for commands from the Pi.
Pi sends "f" if there is any misleading signals from Arduino (e.g., "NACK").
If the data is coming in correctly, it starts sending "g" command to Arduino.
Then, Arduino sends the gas sensor data back to Pi.
Pi saves them as a JSON file.

__author__ = "Myeong Lee (myeong@umd.edu)"
__project__ = "Seeing like a bike"

"""

import serial
import time
from datetime import datetime
import json
from sys import exit


# Constant paths and data collection frequency
logFileName = '/home/pi/data/gas_testbed_logs.log'
arduino_path = '/dev/cycle_arduino'
DELAY = 2 # In seconds

# Open a file with a name appended with current time.
timeNow = datetime.now()
fileTime = timeNow.strftime('%m-%d-%Y-%H-%M-%S')

logFile = open(logFileName, 'a')
logFile.write('Starting script at ' + fileTime + '\n')
logFile.close()

# Create a new log file for this trip
print ('Starting the gas testbed.')

ser = serial.Serial(
    port=arduino_path,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

try:
    # "f" is a signal indicating "fail" to reset Arduino
    # "g" is for requesting data from Arduino
    # ser.write("f")
    # ser.flushInput()
    # ser.flush()

    while True:
        ser.write("g")
        serialLine = ser.readline()

        # "WIN" is a start of the serial communication -- it is a good sign.
        if "WIN" in serialLine:
            time.sleep(0.5)
            continue
        elif "nack" in serialLine or "NACK" in serialLine:
            ser.write("f")
            print("reset Arduino...")
            time.sleep(7)
            ser.flush()
            continue

        serialLine = serialLine.split()
        arduinoData = {}

        for i in range(1, len(serialLine)):
            sensor = serialLine[i - 1]
            value = serialLine[i]
            for k in range(1, 4):
                if sensor == ("CO_" + str(k)):
                    arduinoData["CO_" + str(k)] = value
                elif sensor == ("SO_" + str(k)):
                    arduinoData["SO_" + str(k)] = value
                elif sensor == ("O3_" + str(k)):
                    arduinoData["O3_" + str(k)] = value
                elif sensor == ("NO_" + str(k)):
                    arduinoData["NO_" + str(k)] = value

        timeNow = datetime.now()
        fullTime = timeNow.strftime('%H-%M-%S')
        arduinoData.update({'time': fullTime})
        jsonData = json.dumps(arduinoData)

        try:
            date = timeNow.strftime('%m-%d-%Y')
            gasFile = open('/home/pi/data/' + date + '_testbed.json', 'a')
            gasFile.write(jsonData)
            gasFile.write("\n")
            gasFile.close()
        except:
            print ("ERROR in writing files...")
            logFile = open(logFileName, 'a')
            logFile.write('[' + fullTime + ']: ' + 'Error in writing data.\n')
            logFile.close()
            time.sleep(5)
            ser.flushInput()
            ser.flush()
            continue

        time.sleep(DELAY)

except KeyboardInterrupt:
    logFile = open(logFileName, 'a')
    logFile.write('Script stopped manually. \n')
    logFile.close()
    exit()

except Exception as e:
    logFile = open(logFileName, 'a')
    logFile.write('Error: ' + str(e) + ' Stopping script. \n')
    logFile.close()
    exit()
