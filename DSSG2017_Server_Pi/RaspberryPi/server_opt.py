__author__ = "Jayanth M and Myeong Lee"
__project__ = "Seeing like a bike"

from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

ledfile = open("/home/pi/data/led.log", mode='a')

# Initial Matrix LED statuses; Z=off, W=White, R=Red, B=Blue, G=Green
# White LEDs act as separators and breathe when the server is running normally
# Blue LEDs are dedicated to sensor streams from Proximity - from L to R: Left LIDAR, Right LIDAR, left ultrasonic, right ultrasonic, and log enable
# Green LEDs are dedicated to sensor streams from Surface - from L to R: Inertial, Humidity, Ultraviolet, pressure-temperature-altitude
# Red LEDs are dedicated to sensor streams from Air Quality team - from L to R: Gas sensor array, GPS, Surface mounted microphone
# Other LEDs are static ON, modify to add more

ledStatus = ['Z'] * 35
OFFSET = 0
time = '0'
day = "none"

# DEPRECATED: using /getstatus endpoint now
# use LED file for keeping track of status
def writeLedFile():
    ledfile.seek(0)
    ledfile.truncate()
    ledfile.write(str(ledStatus).replace("\'", "\""))
    ledfile.flush()

# return what the LED status at current time is
@app.route('/getstatus', methods=['GET'])
def retstatus():
    return str(ledStatus).replace("\'","\"")

# update the LED statuses - only Proximity and Surface Quality teams
@app.route('/status',methods=['POST'])
def getstat():
    payload = request.get_json()
    global time
    global day
    day = time[0:6]
    # to keep track of which API is getting data

    if 'LidarLeft' in payload:
        if payload['LidarLeft'] == True:
            ledStatus[OFFSET+30] = 'G'
        else:
            ledStatus[OFFSET+30] = 'B'
    else:
        ledStatus[OFFSET+30] = 'R'

    if 'LidarRight' in payload:
        if payload['LidarRight'] == True:
            ledStatus[OFFSET+22] = 'G'
        else:
            ledStatus[OFFSET+22] = 'B'
    else:
        ledStatus[OFFSET+22] = 'R'

    if 'USLeft' in payload:
        if payload['USLeft'] == True:
            ledStatus[OFFSET+28] = 'G'
        else:
            ledStatus[OFFSET+28] = 'B'
    else:
        ledStatus[OFFSET+28] = 'R'

    if 'USRight' in payload:
        if payload['USRight'] == True:
            ledStatus[OFFSET+24] = 'G'
        else:
            ledStatus[OFFSET+24] = 'B'
    else:
        ledStatus[OFFSET+24] = 'R'

    if 'USRear' in payload:
        if payload['USRear'] == True:
            ledStatus[OFFSET+26] = 'G'
        else:
            ledStatus[OFFSET+26] = 'B'
    else:
        ledStatus[OFFSET+26] = 'R'

    if 'CO' in payload:
        if payload['CO'] == True:
            ledStatus[OFFSET+12] = 'G'
        else:
            ledStatus[OFFSET+12] = 'B'
    else:
        ledStatus[OFFSET+12] = 'R'

    if 'SO' in payload:
        if payload['SO'] == True:
            ledStatus[OFFSET+10] = 'G'
        else:
            ledStatus[OFFSET+10] = 'B'
    else:
        ledStatus[OFFSET+10] = 'R'

    if 'NO' in payload:
        if payload['NO'] == True:
            ledStatus[OFFSET+14] = 'G'
        else:
            ledStatus[OFFSET+14] = 'B'
    else:
        ledStatus[OFFSET+14] = 'R'

    if 'O3' in payload:
        if payload['O3'] == True:
            ledStatus[OFFSET+16] = 'G'
        else:
            ledStatus[OFFSET+16] = 'B'
    else:
        ledStatus[OFFSET+16] = 'R'

    if 'P10' in payload:
        if payload['P10'] == True:
            ledStatus[OFFSET+18] = 'G'
        else:
            ledStatus[OFFSET+18] = 'B'
    else:
        ledStatus[OFFSET+18] = 'R'

    writeLedFile()
    return str(200)

# update the LED statuses - only Proximity and Surface Quality teams
@app.route('/gps_status',methods=['POST'])
def gps():
    payload = request.get_json()
    global time
    global day
    day = time[0:6]
    # to keep track of which API is getting data

    if 'GPS' in payload:
        if payload['GPS'] == True:
            ledStatus[OFFSET+7] = 'B'
            ledStatus[OFFSET+8] = 'B'
        elif payload['GPS'] == "fail":
            ledStatus[OFFSET+7] = 'R'
            ledStatus[OFFSET+8] = 'R'
        else:
            ledStatus[OFFSET+7] = 'G'
            ledStatus[OFFSET+8] = 'G'
    else:
        ledStatus[OFFSET+7] = 'R'
        ledStatus[OFFSET+8] = 'R'
    if 'utc_time' in payload:
        time = payload["utc_time"]

    writeLedFile()
    return str(200)

# proximity sensors receiver
@app.route('/proximity', methods = ['POST'])
def proximity():
    payload = json.loads(str(request.get_json()).replace("\'","\""))
    global time
    global day
    data = {'sensor':'proximity', 'timestamp':time, 'data':payload}
    if day != "none": 
        proxfile = open("/home/pi/data/" + day + "_proximity.json", 'a')
        proxfile.write(str(data))
        proxfile.write("\n")
        proxfile.flush()
    return str(200)

# inertial motion unit receiver
@app.route('/inertial', methods = ['POST'])
def inertial():
    try:
        payload = json.loads(str(request.get_json()).replace("\'","\""))
        global time
        global day
        data = {'sensor':'inertial', 'timestamp':time, 'data':payload}
        
        if payload['accel_x'] == 0 and payload['accel_y']==0 and payload['accel_z']==0:
            ledStatus[OFFSET+34] = 'B'
        else:
            ledStatus[OFFSET+34] = 'G'
    		
        if payload['gyro_x'] == 0 and payload['gyro_y']==0 and payload['gyro_z']==0:
            ledStatus[OFFSET+32] = 'B'
        else:
            ledStatus[OFFSET+32] = 'G'
    except Exception:
        ledStatus[OFFSET+34] = 'R'
        ledStatus[OFFSET+32] = 'R'
    else:    
        if day != "none":
            imufile = open("/home/pi/data/" + day + "_imu.log", mode='a')
            imufile.write(str(data))
            imufile.write("\n")
            imufile.flush()
        return str(200)
    writeLedFile()
    return str(500)

# humidity data receiver
@app.route('/humidity', methods = ['POST'])
def temphumi():
    try:
        payload = json.loads(str(request.get_json()).replace("\'","\"").replace("True","true"))
        # getting temperature data from pressure sensor, that seems more accurate
        payload.pop('temperature_raw', None)
        payload.pop('temperature_is_calibrated', None)
        payload.pop('temperature', None)
        global time
        global day
        data = {'sensor':'humidity', 'timestamp':time, 'data':payload}
    except Exception:
        ledStatus[OFFSET+3] = 'R'
    else:
        ledStatus[OFFSET+3] = 'G'
        if day != "none":
            file = open("/home/pi/data/" + day + "_sensor.log", mode='a')
            file.write(str(data))
            file.write("\n")
            file.flush()
        return str(200)
    writeLedFile()
    return str(500)

# ultraviolet sensor receiver
@app.route('/uvindex', methods = ['POST'])
def uvindex():
    try:
        payload = json.loads(str(request.get_json()).replace("\'","\""))
        global time
        global day
        data = {'sensor':'ultraviolet', 'timestamp':time, 'data':payload}
    except Exception:
        ledStatus[OFFSET+1] = 'R'
    else:
        ledStatus[OFFSET+1] = 'G'
        if day != "none":
            file = open("/home/pi/data/" + day + "_sensor.log", mode='a') 
            file.write(str(data))
            file.write("\n")
            file.flush()
        return str(200)
    writeLedFile()
    return str(500)

# pressure, temperature and altitude receiver
@app.route('/prestempalt', methods = ['POST'])
def pressure():
    try:
        payload = json.loads(str(request.get_json()).replace("\'","\""))
        global time
        global day
        data = {'sensor':'pressure_temperature', 'timestamp':time, 'data':payload}
        if payload['temperature'] == 0:
            ledStatus[OFFSET+5] = 'B'
        else:
            ledStatus[OFFSET+5] = 'G'
        	
        if payload['pressure'] == 0:
            ledStatus[OFFSET+20] = 'B'
        else:
            ledStatus[OFFSET+20] = 'G'
    except Exception:
        ledStatus[OFFSET+5] = 'R'
        ledStatus[OFFSET+20] = 'R'
    else:        
        if day != "none":
            file = open("/home/pi/data/" + day + "_sensor.log", mode='a')
            file.write(str(data))
            file.write("\n")
            file.flush()
        return str(200)
    writeLedFile()
    return str(500)

#@app.route('/gas', methods = ['POST'])
#def gas():
#
#    try:
#        payload = json.loads(str(request.get_json()).replace("\'","\""))
#        global time
#        data = {'sensor':'gasarray', 'timestamp':time, 'data':payload}
#    except Exception:
#        ledStatus[OFFSET+24] = 'B'
#    else:
#        ledStatus[OFFSET+24] = 'R'
#        file.write(str(data))
#        file.write("\n")
#        file.flush()
#        return str(200)
#    finally:
#        writeLedFile()

#@app.route('/gps', methods = ['POST'])
#def gps():
#    try:
#        payload = json.loads(str(request.get_json()).replace("\'","\""))
#        global time
#        data = {'sensor':'gps', 'timestamp':time, 'data':payload}
#    except Exception:
#        ledStatus[OFFSET+7] = 'R'
#        ledStatus[OFFSET+8] = 'R'
#        writeLedFile()
#    else:
#        ledStatus[OFFSET+7] = 'G'
#        ledStatus[OFFSET+8] = 'G'
#        file.write(str(data))
#        file.write("\n")
#        file.flush()
#        writeLedFile()
#        return str(200)
#    return str(500)

#@app.route('/mic', methods = ['POST'])
#def mic():
    #try:
       # payload = json.loads(str(request.get_json()).replace("\'","\""))
      #  time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
     #   data = {'sensor':'surfacemic', 'timestamp':time, 'data':payload}
    #except Exception:
        #ledStatus[OFFSET+26] = 'Z'
    #else:
        #ledStatus[OFFSET+26] = 'R'
     #   micfile.write(str(data))
      #  micfile.write("\n")
       # micfile.flush()
        #return str(200)
    #writeLedFile()
    #return str(500)

# run the server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
