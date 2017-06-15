__author__ = "Jayanth M"
__project__ = "Seeing like a bike"

from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Open files to write to
imufile = open('imu.log', mode='a')
file = open('sense.log', mode='a')
proxfile = open('proximity.log', mode='a')
ledfile = open('led.log',mode='w')

# Initial Matrix LED statuses; Z=off, W=White, R=Red, B=Blue, G=Green
# White LEDs act as separators and breathe when the server is running normally
# Blue LEDs are dedicated to sensor streams from Proximity - from L to R: Left LIDAR, Right LIDAR, left ultrasonic, right ultrasonic, and log enable
# Green LEDs are dedicated to sensor streams from Surface - from L to R: Inertial, Humidity, Ultraviolet, pressure-temperature-altitude
# Red LEDs are dedicated to sensor streams from Air Quality team - from L to R: Gas sensor array, GPS, Surface mounted microphone
# Other LEDs are static ON, modify to add more

ledStatus = ['Z'] * 35
OFFSET = 0

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
    
    # to keep track of which API is getting data
    ledStatus[OFFSET:OFFSET+34] = ['Z']*34

    if 'LidarLeft' in payload:
        ledStatus[OFFSET+31] = 'G'
    if 'LidarRight' in payload:
        ledStatus[OFFSET+23] = 'G'
    if 'USLeft' in payload:
        ledStatus[OFFSET+29] = 'G'
    if 'USRight' in payload:
        ledStatus[OFFSET+25] = 'G'
    if 'USRear' in payload:
        ledStatus[OFFSET+27] = 'G'
    if 'CO' in payload:
        ledStatus[OFFSET+13] = 'G'
    if 'SO' in payload:
        ledStatus[OFFSET+11] = 'G'
    if 'NO' in payload:
        ledStatus[OFFSET+15] = 'G'
    if 'O3' in payload:
        ledStatus[OFFSET+17] = 'G'
    if 'P10' in payload:
        ledStatus[OFFSET+19] = 'G'
    
    # if 'o3' in payload:
    #     if payload['pm'] == 'true':
    #         ledStatus[OFFSET+24] = 'R'
    #     if payload['gas'] == 'true':
    #         ledStatus[OFFSET+25] = 'R'
    # if 'lat' in payload:
    #     if payload['gps'] == 'true':
    #         ledStatus[OFFSET+26] = 'R'
    # if 'mic' in payload:
    #     if payload['mic'] == 'true':
    #         ledStatus[OFFSET+27] = 'R'
    writeLedFile()
    return str(ledStatus) #,str(200)

# proximity sensors receiver
@app.route('/proximity', methods = ['POST'])
def proximity():
    payload = json.loads(str(request.get_json()).replace("\'","\""))
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    data = {'sensor':'proximity', 'timestamp':time, 'data':payload}
    proxfile.write(str(data))
    proxfile.write("\n")
    proxfile.flush()
    return str(200)

# inertial motion unit receiver
@app.route('/inertial', methods = ['POST'])
def inertial():
    try:
        payload = json.loads(str(request.get_json()).replace("\'","\""))
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {'sensor':'inertial', 'timestamp':time, 'data':payload}
    except Exception:
        ledStatus[OFFSET+12] = 'Z'
    else:
        ledStatus[OFFSET+12] = 'G'
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
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {'sensor':'humidity', 'timestamp':time, 'data':payload}
    except Exception:
        ledStatus[OFFSET+13] = 'Z'
    else:
        ledStatus[OFFSET+13] = 'G'
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
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {'sensor':'ultraviolet', 'timestamp':time, 'data':payload}
    except Exception:
        ledStatus[OFFSET+14] = 'Z'
    else:
        ledStatus[OFFSET+14] = 'G'
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
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {'sensor':'pressure_temperature', 'timestamp':time, 'data':payload}
    except Exception:
        ledStatus[OFFSET+15] = 'Z'
    else:
        ledStatus[OFFSET+15] = 'G'
        file.write(str(data))
        file.write("\n")
        file.flush()
        return str(200)
    writeLedFile()
    return str(500)

@app.route('/gas', methods = ['POST'])
def gas():

    try:
        payload = json.loads(str(request.get_json()).replace("\'","\""))
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {'sensor':'gasarray', 'timestamp':time, 'data':payload}
    except Exception:
        ledStatus[OFFSET+24] = 'Z'
    else:
        ledStatus[OFFSET+24] = 'R'
        file.write(str(data))
        file.write("\n")
        file.flush()
        return str(200)
    finally:
        writeLedFile()

@app.route('/gps', methods = ['POST'])
def gps():
    try:
        payload = json.loads(str(request.get_json()).replace("\'","\""))
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {'sensor':'gps', 'timestamp':time, 'data':payload}
    except Exception:
        ledStatus[OFFSET+25] = 'Z'
    else:
        ledStatus[OFFSET+25] = 'R'
        file.write(str(data))
        file.write("\n")
        file.flush()
        return str(200)
    writeLedFile()
    return str(500)

@app.route('/mic', methods = ['POST'])
def mic():
    try:
        payload = json.loads(str(request.get_json()).replace("\'","\""))
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        data = {'sensor':'surfacemic', 'timestamp':time, 'data':payload}
    except Exception:
        ledStatus[OFFSET+26] = 'Z'
    else:
        ledStatus[OFFSET+26] = 'R'
        micfile.write(str(data))
        micfile.write("\n")
        micfile.flush()
        return str(200)
    writeLedFile()
    return str(500)

# run the server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
