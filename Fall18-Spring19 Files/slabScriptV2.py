# Written by Nic Alton Fall 2018, adapted from code written by Saumik Narayanan, Summer 2018
# This version of the script can be used to pull the timestamp and air quality data from one or two
# sets of data files. Written in Python 3 - not compatible with 2.

import csv
import time
import datetime
import json
import statistics as stats
import fileinput
import re

runDate = '01-09-19'

# you need at least one set of files to run this script. Change the list entries below to match the raw data files.
input_files_one= ['R_240219_gps_data.json', 'R_240219_proximity.json','R_240219_imu.log','R_240219_sensor.log']

# if you need to include a second set of files, change the list entries below to match those raw data files.
# if you don't want to include a second set of files, comment the line below and uncomment the line: # input_files_two = []
input_files_two = ['C_240219_gps_data.json', 'C_240219_proximity.json','C_240219_imu.log','C_240219_sensor.log']
# input_files_two = []

interval = 24
oneSec = []
backgroundAQ = 6.3
test = True

n = 0

"""
Creates the row of headers to be used in the output file
 Returns:
    A string which is to be used as a header in the results file
"""
def getHeaders():
    headers = ['Date', 'Lat', 'Long', '']
    headers =  headers + ['PMS1: pm10_standard','PMS1: pm25_standard','PMS1: pm100_standard']
    headers = headers + ['PMS1: pm10_env','PMS1: pm25_env','PMS1: pm100_env','']
    headers = headers + ['PMS2: pm10_standard','PMS2: pm25_standard','PMS2: pm100_standard']
    headers = headers + ['PMS2: pm10_env','PMS2: pm25_env','PMS2: pm100_env','']
    headers = headers + ['AVG: pm10_standard','AVG: pm25_standard','AVG: pm100_standard']
    headers = headers + ['AVG: pm10_env','AVG: pm25_env','AVG: pm100_env', '']
    headers = headers + ['Diff From BackgroundAQ']
    return headers



"""
Creates a row of data in the results file. Also calls convertLatLong to adjust the coordinate formats so
they are not displaced to south georgia.
 Args: 
    ts: the timestamp
    lat: the latitude
    lon: the longitude
    AQdata: the air quality data from the first sensor
    AQdata2: the air quality data from the second sensor
 Returns:
    A string to be used as a row in the results file
"""
def generateRow(ts,lat, lon, AQdata, AQdata2):
    oneSec.append([ts,lat,lon,AQdata,AQdata2])
    coor = convertLatLong(lat, lon)
    lat = coor[0]
    lon = coor[1]
    outputRow = [float(ts),lat,lon,'']
    outputRow = outputRow + [AQdata[0],AQdata[1],AQdata[2]]
    outputRow = outputRow + [AQdata[3],AQdata[4],AQdata[5],'']
    outputRow = outputRow + [AQdata2[0],AQdata2[1],AQdata2[2]]
    outputRow = outputRow + [AQdata2[3],AQdata2[4],AQdata2[5],'']
    pm25avg = meanDropZero([AQdata[1],AQdata2[1]])
    outputRow = outputRow + [meanDropZero([AQdata[0],AQdata2[0]]), meanDropZero([AQdata[1],AQdata2[1]]), meanDropZero([AQdata[2],AQdata2[2]])]
    outputRow = outputRow + [meanDropZero([AQdata[3],AQdata2[3]]), meanDropZero([AQdata[4],AQdata2[4]]), meanDropZero([AQdata[5],AQdata2[5]]),'']
    outputRow = outputRow + [pm25avg - backgroundAQ]
    return outputRow   



"""
Adjust the coordinate formats so they are not displaced to south georgia.
 Args: 
    lat: the latitude
    lon: the longitude
 Returns:
    A list [lat, long] where both are strings
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



# old utility functions, left for possible future convenience
""" Converts a date string from a Purple Air sensor to a datetime object """
def cPA(inputTime):
    return datetime.datetime.strptime(inputTime, '%Y-%m-%d %H:%M:%S')
""" Converts a date string from a GRIMM sensor to a datetime object """
def cGR(inputTime):
    return datetime.datetime.strptime(inputTime, '%m/%d/%Y %I:%M:%S %p') + datetime.timedelta(hours=1, minutes=1, seconds=18)
""" Converts a date string from the SLaB box to a datetime object """
def cSen(inputTime):
    if len(inputTime) == 16:
        inputTime = inputTime[:-4]
    return datetime.datetime.strptime(inputTime, '%d%m%y%H%M%S') - datetime.timedelta(hours=4)
""" Converts a date string from a GPS sensor to a datetime object """
def cGPS(inputTime):
    return datetime.datetime.strptime(inputTime, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=4)
""" Adds two vectors element-wise """
def addVec(v1,v2):
    ret = []
    for i in range(0,len(v1)):
        ret = ret + [str(float(v1[i]) + float(v2[i]))]
    return ret
""" Divides a vector by a constant element-wise"""
def divVec(v,c):
    ret = []
    for i in range(0,len(v)):
        ret = ret + [str(float(v[i])/c)]
    return ret
""" Finds the mean of either a 1d array, or a 2d array, and ignores any 0 values"""
def meanDropZero(m):
    # print("MDZ")
    result = 0
    result_num = 0
    if isinstance(m[0], list):
        for i in m:
            for j in i:
                if j != 0:
                    result = result + j
                    result_num = result_num + 1
    else:
        for i in m:
            if i != 0:
                result = result + i
                result_num = result_num + 1
    if result_num <= 0:
        return 0
    return result / result_num


"""
Goes through the prox and gps files (left and right) and converts their contents into
and array each. If any of the files don't exist, "" is passed in instead and they are skipped.
The raw prox data files use ' instead of " so the method first goes through each file and replaces
the former with the latter and creates a backup.
Once the data is all in lists, calls collectData for the left and right sets of files (and output file)
which goes through the data and writes it appropriately to the output file
 Args:
    left_gps: the left gps raw data file or ""
    left_prox: the left prox raw data file or ""
    right_gps: the right gps raw data file or ""
    right_prox: the right prox raw data file or ""
    output_file_l: the output file for the left data files
    output_file_r: the output file for the right data files
"""
def parseFiles(left_gps, left_prox, right_gps, right_prox, output_file_l, output_file_r):
    
    #some code from: https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file-using-python

    if (right_prox and right_gps) :
        with fileinput.FileInput(right_prox, inplace=True, backup='.bak') as file:
            for line in file:
                    print(line.replace("\'", "\""), end=' ')
        rightProxLines = []
        if right_prox != '':
            fpr = open(right_prox, newline='')
            rightProxLines = fpr.readlines()

        rightGPSLines = []
        if right_gps != '':
            fpr = open(right_gps, newline='')
            rightGPSLines = fpr.readlines()
        collectData(output_file_r, rightProxLines, rightGPSLines)
        print("one complete")
    else:
        print("one ommitted")


    if (left_prox and left_gps):
        with fileinput.FileInput(left_prox, inplace=True, backup='.bak') as file:
            for line in file:
                    print(line.replace("\'", "\""), end=' ')
        leftProxLines = []
        if left_prox != '':
            fpr = open(left_prox, newline='')
            leftProxLines = fpr.readlines()

        leftGPSLines = []
        if left_gps != '':
            fpr = open(left_gps, newline='')
            leftGPSLines = fpr.readlines()
        collectData(output_file_l, leftProxLines, leftGPSLines)
        print("two complete")
    else:
        print("two omitted")
   
    return None


"""
Goes through the lists of gps and prox entries, matches them up by timestamp and calls 
generateRow with the data to create a new output line, which it then writes to the
output file. 
 Args:
    gps: the list of gps entries - never "" or this function wouldn't be called
    prox: the list of prox entries - never "" or this function wouldn't be called
    output_file: the output file to write to
"""

def collectData(oFile, prox, gps):
    with open(oFile, 'w+', newline='') as outf:


        writer = csv.writer(outf, quoting=csv.QUOTE_ALL)
        writer.writerow(getHeaders())
        ticker = 0
        GPSplace = 0
        for j, row in enumerate(prox):
            rowTS = None
            rowAQ = None
            try:
                jsonRow = json.loads(row)
                rowTS = jsonRow['timestamp']
                PMS1 = jsonRow['data']['PMS1']
                PMS1 = re.split(r'[:|,]', PMS1)
                rowAQ = [int(PMS1[1]),int(PMS1[3]),int(PMS1[5]),int(PMS1[7]),int(PMS1[9]),int(PMS1[11])]
                PMS2 = jsonRow['data']['PMS2']
                PMS2 = re.split(r'[:|,]', PMS2)
                rowAQ2 = [int(PMS2[1]),int(PMS2[3]),int(PMS2[5]),int(PMS2[7]),int(PMS2[9]),int(PMS2[11])]
            except Exception as e:
                pass

            if (rowAQ != None):
                rowGPS = None
                while (rowGPS == None ):
                    if (GPSplace < len(gps)):
                        try:
                            gpsJsonRow = json.loads(gps[GPSplace])
                            gpsTS= gpsJsonRow['day'] + gpsJsonRow['utc_time']
                            if (gpsTS == rowTS) :
                                rowGPS = (gpsJsonRow['lat'], gpsJsonRow['long'])
                                writer.writerow(generateRow(rowTS, gpsJsonRow['lat'], gpsJsonRow['long'], rowAQ, rowAQ2))
                                GPSplace+=1
                            elif (gpsTS > rowTS):
                                rowGPS = 0
                                writer.writerow(generateRow(rowTS, '', '', rowAQ, rowAQ2))
                            else:
                                GPSplace+=1
                        except:
                            GPSplace+=1

                    else:
                       rowGPS = 0
                       writer.writerow(generateRow(rowTS, '', '', rowAQ, rowAQ2))


"""
The main function. Generates the two output file names, calls parseFiles function based
on what raw data files are passed in. 
"""
           
def main():
    print("Compiling Data from " + runDate)
    right_input_files = input_files_one
    left_input_files = input_files_two
    output_file_left = runDate + '_two.csv'
    output_file_right = runDate + '_one.csv'
    if (len(left_input_files) == 0) :
        results = parseFiles(None, None, right_input_files[0], right_input_files[1], output_file_left, output_file_right)
    elif (len(right_input_files) == 0) :
        results = parseFiles(left_input_files[0], left_input_files[1], None, None, output_file_left, output_file_right)
    else:
        results = parseFiles(left_input_files[0], left_input_files[1], right_input_files[0], right_input_files[1], output_file_left, output_file_right)
    print("Success")

main() 