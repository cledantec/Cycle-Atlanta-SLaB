# Written by Saumik Narayanan, Summer 2018

import csv
import time
import datetime
import json
import statistics as stats

## input_sen is the file containing enviromental data from the SLaB box, like humidity, temperature, and altitude
## The file format is 'ddmmyy_sensor.log', or '' if no sensor data exists. Only one file created per day

## input_prox is the file containing proximity and air quality data from the SLaB box, like LIDAR, PM Values, and Sulfur Oxide
## The file format is 'ddmmyy_proximity.log', or '' if no prox data exists. Only one file created per day

## input_files contains a list of list of files for each run: Grimm, Pi1, Pi2, GPS Files
## The file format is ['*****_yyyy-mm-dd_hh_mm-M.dat, 'hh-mm-ss_pi1_output.csv', 'hh-mm-ss_output.csv', 'yyyymmdd-hhmmss.txt']
## Pi1, Pi2, and GPS files are each all optional, replace with empty string if not needed
## GPS files are automatically generated from GPS Logger, by BasicAirData in the Google Play Store

input_sen = ''
input_prox = '130718_proximity.json'
input_files = [['7-17_grimm_019_2018-07-13_08-45-M.dat','09-37-00_pi1_output.csv','09-37-16_output.csv'],
['7-17_grimm_021_2018-07-13_09-23-M.dat','10-24-17_pi1_output.csv','10-24-25_output.csv'],
['7-17_grimm_022_2018-07-13_11-32-M.dat','12-08-02_pi1_output.csv','12-08-08_output.csv']]

## Number of segment lengths to test, starting at 6, and incrementing by 6.
## For example, if num_seg_lengths==7, the code will test segments of length [6, 12, 18, 24, 30, 36, 42]
num_seg_lengths = 21

"""
Creates the row of headers to be used in the output file

Returns:
    A string which is to be used as a header in the results file
"""
def getHeaders():
    headers = ['Date', 'Lat', 'Long', '']
    headers = headers + ['Grimm: PM10','Grimm: PM2.5','Grimm: PM1','']
    headers = headers + ['PA1: PM1','PA1: PM2.5','PA1: PM10','']
    headers = headers + ['PA2: PM1','PA2: PM2.5','PA2: PM10','']
    headers = headers + ['PM1 Diff','PM2.5 Diff','PM10 Diff','']
    headers = headers + ['SLaB PM2.5', 'SLaB 10.0', '']
    return headers

"""
Creates a row of data in the results file

Args:
    ts: Start of the Time Segment which the row contains data pertaining to
    row_pa1: PM values from the Purple Air 1 sensor
    row_pa2: PM values from the Purple Air 2 sensor
    row_gr: PM values from the GRIMM sensor
    row_spm: PM values from the SLaB box
    first_gps: First GPS coordinate available from the time segment

Returns:
    A string to be used as a row in the results file
"""
def generateRow(ts, row_pa1, row_pa2, row_gr, row_spm, first_gps):
    outputRow = ["'" + str(ts)] + first_gps + ['']
    outputRow = outputRow + row_gr[0:3] + [''] + row_pa1[0:3] + [''] + row_pa2[0:3] + ['']
    if float(outputRow[10]) == 0 or float(outputRow[14]) == 0:
        return outputRow + [0,0,0]
    outputRow = outputRow + [str(float(outputRow[4])-meanDropZero([float(outputRow[10]),float(outputRow[14])]))]
    outputRow = outputRow + [str(float(outputRow[5])-meanDropZero([float(outputRow[9]),float(outputRow[13])]))]
    outputRow = outputRow + [str(float(outputRow[6])-meanDropZero([float(outputRow[8]),float(outputRow[12])]))]
    outputRow = outputRow + [''] + [str(float(i)) for i in row_spm]
    return outputRow

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
Compiles all data from all sensors of one run, and writes it to the output_file

Args:
    input_gr: All data from the Grimm sensor
    input_pa1: All data from the Purple Air 1 sensor, optional
    input_pa2: All data from the Purple Air 2 sensor, optional
    input_prox: Proximity data file from the SLaB box, optional
    input_gps: All data from the GPS sensor, optional
    output_file: Location to write the output to
    num_seconds: Duration of segment * 6 seconds (e.g. if num_seconds==3, segment duration will be 18 seconds)
"""
def parseFiles(input_gr, input_pa1, input_pa2, input_gps, input_prox, output_file, num_seconds):
    with open(input_gr, newline='') as fgr, \
        open(output_file, 'w+', newline='') as outf:

        # Converts gps data to list of lists
        lines_gps = []
        if input_gps != '':
            fgp = open(input_gps, newline='')
            lines_gps = fgp.readlines()[3:]
            lines_gps = [i.strip().split(',') for i in lines_gps]

        # Converts PA1 data to list of lists
        lines_pa1 = []
        if input_pa1 != '':
            fp1 = open(input_pa1, newline='')
            lines_pa1 = fp1.readlines()[1:]
            lines_pa1 = [i.strip().split(',') for i in lines_pa1]

        # Converts PA2 data to list of lists
        lines_pa2 = []
        if input_pa2 != '':
            fp2 = open(input_pa2, newline='')
            lines_pa2 = fp2.readlines()[1:]
            lines_pa2 = [i.strip().split(',') for i in lines_pa2]

        # Converts proximity data to list of jsons
        lines_prox = []
        if input_prox != '':
            fpr = open(input_prox, newline='')
            lines_prox = fpr.readlines()[3:]

        # Converts Grimm data to list of lists
        lines_gr = fgr.readlines()[15:]
        lines_gr = [i.strip().split('\t') for i in lines_gr]

        writer = csv.writer(outf, quoting=csv.QUOTE_ALL)
        writer.writerow(getHeaders())

        # Calculates a list of segments based on requested time interval
        segs = [cGR(lines_gr[i][0]) for i in range (0, len(lines_gr), num_seconds)]
        
        start_gr = 0
        start_pa1 = 0
        start_pa2 = 0
        start_gps = 0
        start_spm = 0

        # Calculates data for each x-second segment
        for i, start_seg in enumerate(segs):
            if i+1 == len(segs):
                break
            else:
                end_seg = segs[i+1]
            
            # Initial values for means and counts
            mean_gr = [0]*15
            mean_pa1 = [0]*12
            mean_pa2 = [0]*12
            mean_spm = [0]*2 # SLaB pm2.5 and pm10.0
            first_gps = ['']*2
            num_gr = 0
            num_pa1 = 0
            num_pa2 = 0
            num_spm = 0 # SLaB pm2.5 and pm10.0

            # Grimm Code
            for j, row in enumerate(lines_gr[start_gr:]):
                if cGR(row[0]) < start_seg:
                    continue
                elif cGR(row[0]) >= end_seg or j+1 == len(lines_gr):
                    start_gr = j
                    break
                else:
                    mean_gr = addVec(row[1:], mean_gr)
                    num_gr = num_gr + 1
            if (num_gr > 0):
                mean_gr = divVec(mean_gr, num_gr)

            # Purple Air 1
            for j, row in enumerate(lines_pa1[start_pa1:]):
                if not row[0][0].isalnum() or cPA(row[0]) < start_seg:
                    continue
                elif cPA(row[0]) >= end_seg or j+1 == len(lines_pa1):
                    start_pa1 = j
                    break
                else:
                    mean_pa1 = addVec(row[1:], mean_pa1)
                    num_pa1 = num_pa1 + 1
            if (num_pa1 > 0):
                mean_pa1 = divVec(mean_pa1, num_pa1)

            # Purple Air 2 
            for j, row in enumerate(lines_pa2[start_pa2:]):
                if not row[0][0].isalnum() or cPA(row[0]) < start_seg:
                    continue
                elif cPA(row[0]) >= end_seg or j+1 == len(lines_pa2):
                    start_pa2 = j
                    break
                else:
                    mean_pa2 = addVec(row[1:], mean_pa2)
                    num_pa2 = num_pa2 + 1
            if (num_pa2 > 0):
                mean_pa2 = divVec(mean_pa2, num_pa2)

            # Proximity Code
            # Comment out the below code if proximity code is not needed, as loading json data
            # can make runtime very slow
            for j, row in enumerate(lines_prox[start_spm:]):
                jsonRow = json.loads(row)            
                if cSen(jsonRow['timestamp']) < start_seg:
                    continue
                elif cSen(jsonRow['timestamp']) >= end_seg:
                    start_spm = j
                    break
                elif 'P25' in jsonRow['data']:
                    mean_spm[0] = mean_spm[0] + float(jsonRow['data']['P25'])
                    mean_spm[1] = mean_spm[1] + float(jsonRow['data']['P10'])
                    num_spm = num_spm + 1
            if num_spm > 0:
                mean_spm = divVec(mean_spm, num_spm)
           
            #GPS code
            for j, row in enumerate(lines_gps[start_gps:]):
                if cGPS(row[1]) < start_seg:
                    continue
                elif cGPS(row[1]) >= end_seg or j+1 == len(lines_gps):
                    break
                else:
                    first_gps = [row[2],row[3]]
                    break

            writer.writerow(generateRow(start_seg, mean_pa1, mean_pa2, mean_gr, mean_spm, first_gps))

    with open(output_file, 'r', newline='') as outf:
        lines_outf = outf.readlines()[1:]
        lines_outf = [i.strip().split(',') for i in lines_outf]
        lines_outf = [i for i in lines_outf if i[1] != '"0"' and (i[5] != '"0"' or i[9] != '"0"')]
        res1 = [float(i[16][1:-1]) for i in lines_outf]
        res25 = [float(i[17][1:-1]) for i in lines_outf]
        res10 = [float(i[18][1:-1]) for i in lines_outf]

        res1 = [i for i in res1 if i != 0]
        res25 = [i for i in res25 if i != 0]
        res10 = [i for i in res10 if i != 0]

        line1 = ['']*15 + ['Mean'] + [stats.mean(res1)] + [stats.mean(res25)] + [stats.mean(res10)]
        line2 = ['']*15 + ['STDev'] + [stats.pstdev(res1)] + [stats.pstdev(res25)] + [stats.pstdev(res10)]
    
    results = [line1[16:]] + [line2[16:]]
    with open(output_file, 'a', newline='') as outf:
        writer = csv.writer(outf, quoting=csv.QUOTE_ALL)
        writer.writerow(line1)
        writer.writerow(line2)

    return results
            
def main():
    means = []
    stdevs = []

    for num_seconds in range (1,num_seg_lengths+1):
        output_file = ''
        print(str(num_seconds*6) + ' seconds')
        meanRuns = []
        stdevRuns = []
        for f in input_files:
            print(f)
            if f[1] == '':
                output_file = 'results/result_seg_' + f[2][0:5] + '_' + str(num_seconds*6) + 'sec_' + f[0][-5:-4] + '.csv'
            else:
                output_file = 'results/result_seg_' + f[1][0:5] + '_' + str(num_seconds*6) + 'sec_' + f[0][-5:-4] + '.csv'
            if len(f) < 4:
                f = f + ['']
            if len(f) < 4:
                f = f + ['']
            results = parseFiles(f[0],f[1],f[2],f[3], input_prox, output_file, num_seconds)
            meanRuns = meanRuns + [results[0][1]]
            stdevRuns = stdevRuns + [results[1][1]]


        means = means + [meanDropZero(meanRuns)]
        stdevs = stdevs + [meanDropZero(stdevRuns)]
        print(meanRuns)
        print(stdevRuns)
    print(means)
    print(stdevs)

main()