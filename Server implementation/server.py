__author__ = "Jayanth M"

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

ledStatus = ['W', 'Z', 'Z', 'Z', 'Z', 'Z', 'B', 'B', 'B', 'B', 'B', 'W', 'Z', 'Z', 'Z', 'Z', 'G', 'G', 'G', 'G', 'G', 'G', 'W', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'W', 'W']
OFFSET = 0

def writeLedFile():
    ledfile.seek(0)
    ledfile.truncate()
    ledfile.write(str(ledStatus).replace("\'", "\""))
    ledfile.flush()

@app.route('/getstatus', methods=['GET'])
def retstatus():
    return str(ledStatus).replace("\'","\"")

@app.route('/status',methods=['POST'])
def getstat():
    payload = json.loads(str(request.get_json()).replace("\'","\""))
    if 'lidarLeftStatus' in payload:
        ledStatus[OFFSET+1:OFFSET+6] = ['Z']*5
        if payload['lidarLeftStatus'] == 'true':
            ledStatus[OFFSET+1] = 'B'
        if payload['lidarRightStatus'] == 'true':
            ledStatus[OFFSET+2] = 'B'
        if payload['usLeftStatus'] == 'true':
            ledStatus[OFFSET+3] = 'B'
        if payload['usLeftStatus'] == 'true':
            ledStatus[OFFSET+4] = 'B'
        if payload['diskWriteStatus'] == 'true':
            ledStatus[OFFSET+5] = 'B'
##    if 'pmstatus' in payload:
##        if payload['diskWriteStatus'] == 'true':
##            ledStatus[OFFSET+5] = 'B'
            writeLedFile()
    return str(ledStatus) #,str(200)


@app.route('/proximity', methods = ['POST'])
def proximity():
    payload = json.loads(str(request.get_json()).replace("\'","\""))
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    data = {'sensor':'proximity', 'timestamp':time, 'data':payload}
    proxfile.write(str(data))
    proxfile.write("\n")
    proxfile.flush()
    return str(200)

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

@app.route('/humidity', methods = ['POST'])
def temphumi():
    try:
        payload = json.loads(str(request.get_json()).replace("\'","\"").replace("True","true"))
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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
