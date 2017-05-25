#This code connects the arduino with its sensots to the Raspberry Pi 3 with its sensors

import csv
import serial
import time
import datetime
from lidar_lite import Lidar_Lite

#Logging to keep track of system performance
logFileName = 'proximity.log'
DELAY = 0.1 # In seconds

# Open a file with a name appended with current time.
timeNow=datetime.datetime.now();
fileTime=timeNow.strftime('%m-%d-%Y-%H-%M-%S')

logFile =  open(logFileName,'a')
logFile.write('Starting script at '+fileTime+'\n')

status = True
try:
    ser=serial.Serial(port='/dev/ttyACM0',baudrate=4800)

    lidar=Lidar_Lite()
    connected=lidar.connect(1)
    if connected<-1:
        raise valueError('Lidar not connected.')


    while True:
            dataFile = open('data_'+fileTime+'.csv','a')
            dataWriter = csv.writer(dataFile)
            serialLine=ser.readline()
            lidarData=lidar.getDistance()
            arduinoData=serialLine.split()
            if len(arduinoData) !=3: continue           # Incomplete data
            dataList = [lidarData] + arduinoData
            dataWriter.writerow(dataList)
            dataFile.close()
        else:

        time.sleep(DELAY)
        
except KeyboardInterrupt:
    logFile.write('Script stopped manually. \n')

except Exception as e:
    logFile.write('Error: '+str(e) + ' stopping script. \n')
logFile.close()
dataFile.close()
# Close it on the way out.
