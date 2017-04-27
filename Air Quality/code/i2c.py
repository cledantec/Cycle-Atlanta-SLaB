# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
#todo
#uncomment once the gas array is connected
gasArray = Adafruit_ADS1x15.ADS1015()

# Or create an ADS1015 ADC (12-bit) instance.
PMSense = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

#print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
#print('-' * 37)
VxCO = 818
VxSO = 823
VxO = 812
VxNO = 810
COi = 0.00000000475
SOi = 0.000000025
Oi = 0.000000032
NOi = 0.000000040
# Main loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        #todo
        #change PMSense to gasArray
        values[i] = float(gasArray.read_adc(i, gain=GAIN))
        
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
    #pmVal = PMSense.read_adc(0, gain = GAIN)
    #print 'PM concentration : %.2f kPa' %pmVal
    
    
    values[0] = (values[0] - VxCO)/(500000*COi)
    values[1] = (values[1] - VxSO)/(500000*SOi)
    values[2] = (values[2] - VxO)/(500000*Oi)
    values[3] = (values[3] - VxNO)/(500000*NOi)
    #print 'Vx: %.f ' %masterVal

    print time.strftime('%H:%M:%S')
    
    print ("{'Sensor':'GasArray CO', 'data':  %.2f ppm'}\n" %values[0])
    
    print ("{'Sensor':'GasArray SO', 'data':  %.2f ppm'}\n" %values[1])
    
    print ("{'Sensor':'GasArray O', 'data':  %.2f ppm'}\n" %values[2])
    
    print ("{'Sensor':'GasArray NO', 'data':  %.2f ppm'}\n" %values[3])

    #print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    # Pause for half a second.
    #todo
    #store the values from the pmSense[2] for 1second as
    #mic measurments
    time.sleep(1)

