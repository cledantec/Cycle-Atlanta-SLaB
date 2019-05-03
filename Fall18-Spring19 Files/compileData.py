# Written by Nic Alton Spring 2019, adapted from code written by Saumik Narayanan, Summer 2018
# This version of the script can be used to pull all data from one a single set of SLaB box raw data files
# and combine it in JSON format in a new file. Written in Python 3 - not compatible with 2.


import csv
import time
import datetime
import json
import statistics as stats
import fileinput
import re

#change the runID here
runID = '040219IP1_1'
# change the list below to contain the files you want to compile
input_files = ['040219_gps_data.json', '040219_proximity.json','040219_imu.log','040219_sensor.log']

"""
The latitude and longitude in the GPS files are in a different format
And when mapped make it look like the route is in south Georgia
Converting to a different format fixes the problem
 Args:
    Lat: the latitude
    Lon: the longitude
 Returns:
    [strLat, strLon] : a list containing the converted coordinates as strings
"""
def convertLatLong(lat, lon):
    strLat = ""
    strLon = ""
    if (lat != '') :
        lat = str(float(lat) / 100)
        strLat = str(int(lat[0:2]) + ((float(lat[2:])*100)/60))
    if (lon != '') :
        lon = str(float(lon) / 100)
        strLon = int(lon[0:2]) + ((float(lon[2:])*100)/60)
        strLon = str( -1 * strLon)
    return [strLat, strLon]

"""
Compiles all data from all sensors for one run, into a list of lists.
 Args:
    gps: GPS data file from the SLaB box
    prox: Proximity data file from the SLaB box
    imu: IMU data file from the SLaB box
    sensor: Sensor data file from the SLaB box
 Returns:
  [gpsLines, proxLines, imuLines, sensorLines]: a list of lists, each individual list containing the lines from the
        respective files as strings
"""
def parseFiles(gps, prox, imu, sensor):
    
    #resoure: https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file-using-python

    gpsLines = []
    proxLines = []
    imuLines = []
    sensorLines = []
    if (prox) :
        """Create backup of file and replace all ' with " """
        with fileinput.FileInput(prox, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace("\'", "\""), end=' ')
        if (prox != ''):
            fpr = open(prox, newline='')
            proxLines = fpr.readlines()
    if (gps != ''):
        fpr = open(gps, newline='')
        gpsLines = fpr.readlines()
    if (imu) :
        """Create backup of file and replace all ' with " """
        with fileinput.FileInput(imu, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace("\'", "\""), end=' ')
        if (imu != ''):
            fpr = open(imu, newline='')
            imuLines = fpr.readlines()
    if (sensor) :
        """Create backup of file and replace all ' with " """
        with fileinput.FileInput(sensor, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace("\'", "\""), end=' ')
        if (sensor != ''):
            fpr = open(sensor, newline='')
            sensorLines = fpr.readlines()
    return [gpsLines, proxLines, imuLines, sensorLines]



"""
Goes through the list of GPS entries and writes them to the output file
this method doesn't account for repeated timestamps as they don't occur
in GPS files
 Args:
    gps: the list of GPS entries (as strings) 
    oFile: The output file
"""
def writeGPS(gps, oFile):
    print("Compiling GPS Data")
    with open(oFile, 'w+', newline='') as outf:
        index = 0;
        # to avoid double quotes, set the escape char to ?, which is removed at end
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE,  escapechar='?', quotechar='')
        for r in gps:
            try:
                row = json.loads(r)
            except:
                index+=1
                continue
            ts= row['day'] + row['utc_time']
            year = '20' + ts[4:6]
            month = ts[2:4]
            day = ts[0:2]
            hour = ts[6:8]
            minute = ts[8:10]
            sec = ts[10:12]
            timestamp = year + '-' + month + "-" + day + " " + hour + ":" + minute + ":" + sec + ".000"
            line = ""
            if (index == 0):
                line = line + "{\"GPS\":{"

            line = line + "\""  + timestamp + "\":"
            lat = row['lat']
            lon = row['long']
            coor = convertLatLong(lat, lon)
            line = line + "{\"latitude\":" + "\"" + coor[0] + "\"" + ", \"longitude\":" + "\"" + coor[1] + "\""
            line = line + ", \"speed\":" + "\"" + row['speed'] + "\"" + ", \"course\":" + "\"" + row['course'] + "\"}"
            if (index == len(gps) - 2):
                line = line + "},"
            else:
                line = line + ","
            writer.writerow([line])
            index+=1
"""
Takes in a row and returns just the hour + minute + sec timestamp for 
everything, good for comparing to basetime but not for printing
Args:
    row: the row of data to pull the timestamp out of
 Returns:
  hour + minute + sec timestamp as a string
"""
def getTS(row):
    try:
        ts= row['timestamp']
        year = '20' + ts[4:6]
        month = ts[2:4]
        day = ts[0:2]
        hour = ts[6:8]
        minute = ts[8:10]
        sec = ts[10:12]
        return (hour + minute + sec)
    except:
        ts= row ['day'] + row['utc_time']
        year = '20' + ts[4:6]
        month = ts[2:4]
        day = ts[0:2]
        hour = ts[6:8]
        minute = ts[8:10]
        sec = ts[10:12]
        return (hour + minute + sec)


"""
Goes through the list of Prox entries and writes them to the output file
This method does account for repeated timestamps and, if it can't calulate the difference
Between the currently repeating time and the next one, it automatically increments by .3.
 Args:
    prox: the list of GPS entries (as strings) 
    oFile: The file to write to
"""
def writeProx(prox, oFile):
    print("Compiling PROX Data")
    with open(oFile, 'a', newline='') as outf:
        index = 0; 
        numRepeats = 0
        # to avoid double quotes, set the escape char to ?, which is removed at end
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE,  escapechar='?', quotechar='')
        basetime = None
        milisec = 0
        increment = 0
        for i,r in enumerate(prox):
            try:
                row = json.loads(r)
            except:
                continue
            ts= row['timestamp']
            year = '20' + ts[4:6]
            month = ts[2:4]
            day = ts[0:2]
            hour = ts[6:8]
            minute = ts[8:10]
            sec = ts[10:12]
            if (int(hour + minute + sec) == basetime):
                # Duplicate Timestamp - we need to determine how much to incrememnt by
                # First determine if an increment has already been found
                if (increment != 0):
                    milisec = milisec + round(increment, 3);
                else:
                    # no increment, so this is the first repeated timestamp
                    increment = getIncrement (hour, minute, sec, basetime, prox, i, .3)
                    milisec = round(increment, 3)
            else:
                increment = 0
                milisec = 0
                basetime = int(hour + minute + sec)
            timestamp = makeTimeStamp (year, month, day, hour, minute, sec, milisec)
            line = ""
            if (i == 0):
                line = line + "\"PROX\":{"
            line = line + "\"" + timestamp + "\":{"
            lineData = row['data']
            sensors = ['USRear','USLeft','USRight','LidarLeft','LidarRight']
            dataList = ['','','','','']
            if (lineData != {}) :
                try:
                    PMS1 = lineData['PMS1']
                    PMS1 = re.split(r'[:|,}]', PMS1)
                    line = line + "\"pm10_standard_left\":" + "\"" + PMS1[1] +  "\"" + ", \"pm25_standard_left\":" + "\"" + PMS1[3] + "\"" + ", \"pm100_standard_left\":" + "\"" +  PMS1[5] + "\""\
                        + ", \"pm10_env_left\":" + "\"" + PMS1[7] + "\"" + ", \"pm25_env_left\":" + "\"" + PMS1[9] + "\"" + ", \"pm100_env_left\": " + "\"" + PMS1[11] + "\""\
                        + ", \"particles_03um_left\":" + "\"" + PMS1[13] + "\"" + ", \"particles_05um_left\":" + "\"" + PMS1[15]  + "\"" + ", \"particles_10um_left\":" + "\"" + PMS1[17] + "\""\
                        + ", \"particles_25um_left\":" + "\"" + PMS1[19] + "\"" + ", \"particles_50um_left\":" + "\"" + PMS1[21] + "\"" + ", \"particles_100um_left\":" + "\"" + PMS1[23] + "\","
                except:
                    pass
                try:
                    PMS2 = lineData['PMS2']
                    PMS2 = re.split(r'[:|,}]', PMS2)
                    line = line + " \"pm10_standard_right\":" + "\"" + PMS2[1]  + "\"" + ", \"pm25_standard_right\":" + "\"" + PMS2[3] + "\"" + ", \"pm100_standard_right\":" + "\"" + PMS2[5] + "\""
                    line = line + ", \"pm10_env_right\":" + "\"" +PMS2[7] + "\"" + ", \"pm25_env_right\":" + "\"" + PMS2[9] + "\""  + ", \"pm100_env_right\":" + "\"" + PMS2[11] + "\""
                    line = line + ", \"particles_03um_right\":" + "\"" + PMS2[13] + "\"" + ", \"particles_05um_right\":" + "\"" + PMS2[15] + "\"" + ", \"particles_10um_right\":" + "\"" + PMS2[17] + "\""
                    line = line + ", \"particles_25um_right\":" + "\"" + PMS2[19] + "\"" + ", \"particles_50um_right\":" + "\"" +PMS2[21] + "\"" + ", \"particles_100um_right\":" + "\"" + PMS2[23] + "\"" + ", "
                except:
                    pass
                for j, s in enumerate(sensors):
                    try:
                        dataList[j] = lineData[s]
                    except:
                        continue

                line = line + "\"us_rear\":" + "\"" + dataList[0] + "\"" + ", \"us_left\":" + "\"" + dataList[1] + "\"" +", \"us_right\":" + "\"" + dataList[2] + "\""\
                + ", \"lidar_left\":" + "\"" + dataList[3] + "\"" + ", \"lidar_right\":" + "\"" + dataList[4] + "\"}"
            else:
                line = line + "\"us_rear\":" + "\"" + "" + "\"" + ", \"us_left\":" + "\"" + "" + "\"" + ", \"us_right\":" + "\"\""\
                + ", \"lidar_left\":" + "\"" + "" + "\"" + ", \"lidar_right\":" + "\"\"" + "}"
            if (i == len(prox) - 2):
                line = line + "},"
            else:
                line = line + ","
            writer.writerow([line])
            i+=1

"""
Goes through the list of IMU entries and writes them to the output file
This method does account for repeated timestamps and, if it can't calulate the difference
Between the currently repeating time and the next one, it automatically increments by .05.
 Args:
    imu: the list of IMU entries (as strings) 
    oFile: The file to write to
"""
def writeIMU(imu, oFile):
    print("Compiling IMU Data")

    with open(oFile, 'a', newline='') as outf:
        index = 0;
        numRepeats  = 0
        # to avoid double quotes, set the escape char to ?, which is removed at end
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE,  escapechar='?', quotechar='')
        basetime = None
        bases = []
        milisec = 0
        increment = 0
        for i, r in enumerate(imu):
            try:
                row = json.loads(r)
            except:
                continue
            ts= row['timestamp']
            year = '20' + ts[4:6]
            month = ts[2:4]
            day = ts[0:2]
            hour = ts[6:8]
            minute = ts[8:10]
            sec = ts[10:12]
            if (int(hour + minute + sec) == basetime):
                # Duplicate Timestamp - we need to determine how much to incrememnt by
                # First Determine if an increment has already been found
                if (increment != 0):
                    milisec = milisec + round(increment, 3);
                else:
                    # no increment, so this is the first repeated timestamp
                    increment = getIncrement (hour, minute, sec, basetime, imu, i, .05)
                    milisec = round(increment, 3)
            else:
                increment = 0
                milisec = 0
                basetime = int(hour + minute + sec)
            timestamp = makeTimeStamp (year, month, day, hour, minute, sec, milisec)
            line = ""
            if (i == 0):
                line = line + "\"IMU\":{"
            line = line + "\"" + timestamp + "\"" + ":{"
            sen = ['mag_x','mag_y','mag_z','gyro_x','gyro_y', 'gyro_z','accel_x','accel_y','accel_z','roll','pitch','yaw']
            sensors = ['magnetometer_x','magnetometer_y','magnetometer_z','gyroscope_x','gyroscope_y', 'gyroscope_z','accelerometer_x','accelerometer_y','accelerometer_z','roll','pitch','yaw']
            dataList = ['','','','','', '','','','','','','']
            lineData = row['data']
            if (lineData != {}):
                for j, s in enumerate(sen):
                    try:
                        dataList[j] = lineData[s]
                    except:
                        continue
                line = line + "\"" + str(sensors[0]) + "\":\"" + str(dataList[0]) + "\", \"" + str(sensors[1]) + "\":\"" + str(dataList[1]) + "\", \"" + str(sensors[2]) + "\":\"" + str(dataList[2]) + "\", \"" + str(sensors[3]) + "\":\"" + str(dataList[3]) + "\", \""
                line = line + str(sensors[4]) + "\":\"" + str(dataList[4]) + "\", \"" + str(sensors[5]) + "\":\"" + str(dataList[5]) + "\", \"" + str(sensors[6]) + "\":\"" + str(dataList[6]) + "\", \"" + str(sensors[7]) + "\":\"" + str(dataList[7]) + "\", \""
                line = line + str(sensors[8]) + "\":\"" + str(dataList[8]) + "\", \"" + str(sensors[9]) + "\":\"" + str(dataList[9]) + "\", \"" + str(sensors[10]) + "\":\"" + str(dataList[10]) + "\", \"" + str(sensors[11]) + "\":\"" + str(dataList[11]) + "\"}"
            else:
                line = line + "}"

            if (i == len(imu) - 2):
                line = line + "},"
            else:
                line = line + ","
            writer.writerow([line])


"""
Goes through the list of Sensor entries and writes them to the output file
This method does account for repeated timestamps and, if it can't calulate the difference
Between the currently repeating time and the next one, it automatically increments by 1.
 Args:
    prox: the list of sensor entries (as strings) 
    oFile: The file to write to
"""
def writeSensor(sensor, oFile):
    print("Compiling Sensor Data")
    with open(oFile, 'a', newline='') as outf:
        basetime = None
        milisec = 0
        increment = 0

        # to avoid double quotes, set the escape char to ?, which is removed at end
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE,  escapechar='?', quotechar='')
        for i,r in enumerate(sensor):
            try:
                row = json.loads(r)
            except:
                continue
            ts= row['timestamp']
            year = '20' + ts[4:6]
            month = ts[2:4]
            day = ts[0:2]
            hour = ts[6:8]
            minute = ts[8:10]
            sec = ts[10:12]
            if (int(hour + minute + sec) == basetime):
                # Duplicate Timestamp - we need to determine how much to incrememnt by
                # First Determine if an increment has already been found
                if (increment != 0):
                    milisec = milisec + round(increment, 3)
                else:
                    # no increment, so this is the first repeated timestamp
                    increment = getIncrement (hour, minute, sec, basetime, sensor, i, 1)
                    milisec = round(increment, 3)
            else:
                increment = 0
                milisec = 0
                basetime = int(hour + minute + sec)
            timestamp = makeTimeStamp (year, month, day, hour, minute, sec, milisec)
            line = ""
            if (i == 0):
                line = line + "\"SENSOR\":{"
            line = line + "\"" + timestamp + "\"" + ":{"
            sen = ['uv_index','humidity','altitude','temperature','pressure', 'oms_risk']
            sensors = ['uv_index','humidity','altitude','temperature','pressure', 'oms_risk']
            dataList = ['','','','','', '','','','','','','']
            lineData = row['data']
            if (lineData != {}):
                for j, s in enumerate(sen):
                    try:
                        dataList[j] = lineData[s]
                    except:
                        continue
                line = line + "\"" + str(sensors[0]) + "\":\"" + str(dataList[0]) + "\", \"" + str(sensors[1]) + "\":\"" + str(dataList[1]) + "\", \"" + str(sensors[2]) + "\":\"" + str(dataList[2]) + "\", \"" + str(sensors[3]) + "\":\"" + str(dataList[3]) + "\", \""
                line = line +  str(sensors[4]) + "\":\"" + str(dataList[4]) + "\", \"" + str(sensors[5]) + "\":\"" + str(dataList[5]) + "\"}"
            else:
                line = line + "}"


            if (i == len(sensor) - 2):
                line = line + "}}"
            else:
                line = line + ","
            writer.writerow([line]) 


"""
Takes in timestamp data and creates a timestamp sting. If an interval
has been applied to this timestamp the milisec will be large and will
be converted into minutes and seconds and etc. Converts single digit
timestamp pieces into double digits ("0" -> "00")
Args:
    year: the year
    month: the month
    day: the day
    hour: the hour
    minute: the minute
    sec: the second
    milisec: the milisecond

 Returns:
    a correct timestamp string
"""
def makeTimeStamp (year, month, day, hour, minute, sec, milisec) :
    modMili = milisec
    mil = float(milisec%1)
    mil = round(mil, 3)
    if (mil == 1.0) :
        modMili += 1
        mil - 1.0;
    while (modMili >= 1):
        modMili = modMili - 1
        sec = str(int(sec) + 1)
        if (int(sec) >= 60):
            sec = str(int(sec) - 60)
            minute = str(int(minute) + 1)
        if (int(minute) >= 60):
            minute = str(int(minute) - 60)
            hour = str(int(hour) + 1)
    if (mil == 0):
        mil = ".000"
    else:
        mil = str(mil)[1:5]
    while (len(mil) < 4):
        mil = mil + "0"
    secStr = str(sec)
    if (secStr == "0") :
        secStr = "00"
    elif(int(secStr) < 10 and secStr[0] != "0"):
        secStr = "0" + secStr
    minuteStr = str(minute)
    if (int(minuteStr) < 10):
        minuteStr + "0" + minuteStr
    if (minute == "0") :
        minuteStr = "00"
    hourStr = str(hour)
    if (hour == "0") :
        hourStr = "00"
    milisec = milisec - int(milisec)

    timestamp = year + '-' + month + "-" + day + " " + hourStr + ":" + minuteStr + ":" + secStr + str(mil)
    # print("end with: " + timestamp)
    return timestamp   


"""
Given the time and the base time, calculated the increment for all timestamps
sharing the same time.
Args:
    hour: the hour
    minute: the minute
    sec: the sec
    hour: the hour
    basetime: the basetime - the timestamp repeating
    rows: the list of data from the method that called getIncrement
    index: the index of the current data in the rows list
    baseIncrement: the default increment for this type of data

 Returns:
    a correct timestamp string
"""
def getIncrement (hour, minute, sec, basetime, rows, index, baseIncrement) :
    # if this method is being called, there are already 2 entries with the same timestamp
    entrysUntilChange = 2.0
    endOf = False
    newTS = None
    while (newTS == None and not endOf):
        try:
            nextRow = json.loads(rows[index + 1])
            nextTS = getTS(nextRow)
            if (int(nextTS) == basetime):
                entrysUntilChange+=1.0
                index+=1
            else:
                newTS = nextTS
        except:
            endOf = True
            return baseIncrement
    # we have the number of repeated entries and the next time, so we need to calculate the incrememnt
    nextHour = float(newTS[0:2])
    # check if it's midnight (00:00:00)
    if (float(hour) > nextHour):
        nextHour = nextHour + 24.0;
    differenceInTimeInSeconds = (float(newTS[4:6]) - float(sec) + (60 * (float(newTS[2:4]) - float(minute))) + (3600 * (nextHour - int(hour))))
    return (float(differenceInTimeInSeconds) / float(entrysUntilChange))

           
def main():
    print("Compiling Data from " + runID)
    output_file_left = runID + ".json"
    if (len(input_files) != 0) :
        leftLists = parseFiles(input_files[0], input_files[1], input_files[2], input_files[3])
        writeGPS(leftLists[0], output_file_left)
        writeProx(leftLists[1], output_file_left)
        writeIMU(leftLists[2], output_file_left)
        writeSensor(leftLists[3], output_file_left)
    if(len(input_files) == 0):
        print("no data")
    # have to get rid of all the ?
    with fileinput.FileInput(output_file_left, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace("?", ""), end=' ')
    print("Success")

main() 