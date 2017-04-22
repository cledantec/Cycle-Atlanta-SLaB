###########################
### Particulate Matter ####
###########################

import serial
import time
import json
import requests
import ast
# Import the ADS1x15 module.
import Adafruit_ADS1x15

USBser = serial.Serial('/dev/ttyACM0', 9600)
url = 'http://192.168.1.10:5000/gas'
headers = {'Content-type': 'application/json'}
def getpm():
    USBser.flushInput()
    USBser.flush()
    read_data = USBser.readline()
    #data is already in json
    pmdata = ast.literal_eval(read_data)
    return pmdata['data']

#############################
########## Gas Array ########
#############################

# Create an ADS1115 ADC (12-bit) instance.
gasArray = Adafruit_ADS1x15.ADS1015()
GAIN = 1

#Low limit for each sensor @ Vx ppm = 0
VxCO = 818
VxSO = 823
VxO = 812
VxNO = 810
#amount of current output for each ppm
COi = 0.00000000475
SOi = 0.000000025
Oi = 0.000000032
NOi = 0.000000040

def getgas():
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = float(gasArray.read_adc(i, gain=GAIN))
    #compute conversion        
    values[0] = (values[0] - VxCO)/(500000*COi)
    values[1] = (values[1] - VxSO)/(500000*SOi)
    values[2] = (values[2] - VxO)/(500000*Oi)
    values[3] = (values[3] - VxNO)/(500000*NOi)

    gasarray = {"co":round(values[0], 2), "so2":round(values[1], 2), "o3":round(values[2], 2), "no2":round(values[3],2), "pm":getpm()}
    return (json.dumps(gasarray))
##    print ("{'Sensor':'GasArray CO', 'data':  %.2f'}\n" %values[0])  
##    print ("{'Sensor':'GasArray SO', 'data':  %.2f'}\n" %values[1])   
##    print ("{'Sensor':'GasArray O', 'data':  %.2f'}\n" %values[2])
##    print ("{'Sensor':'GasArray NO', 'data':  %.2f'}\n" %values[3])

# Main loop.
while True:
    print str(getgas())
    response = requests.post(url, data=getgas(), headers=headers)
    print(response.content)
    time.sleep (5)
    

