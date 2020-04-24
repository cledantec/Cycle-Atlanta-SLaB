# Electrical System Documentation
The electrical system includes the sensors and other electrical components used, as well as the PCB that connects them all. The electrical components include:
- 1x [Anker 5000 mAh Battery](https://www.anker.com/products/variant/powercore-5000/A1109011)
- 1x USB-A male-to-male cable
- 1x [Stewart Connector USB-A port](https://www.digikey.com/product-detail/en/stewart-connector/SS-52100-001/380-1412-ND/7902377)
- 1x On/Off Switch
- 1x Current Sensor
- 1x [Teensy 4.0 Microcontroller](https://www.pjrc.com/store/teensy40.html)
- 4x [Garmin LIDAR-Lite v4 LEDs](https://buy.garmin.com/en-US/US/p/610275)
- 1x [Adafruit Bluefruit UART Friend](https://www.adafruit.com/product/2479)
- 2x 1.5 kΩ (pull-up) resistors
- 1x 680 μF capacitor

The current PCB was designed in Eagle 9.6.1. Since Georgia Tech's [Electronics Lab](http://www.me.gatech.edu/facilities/electronic_lab) uses Eagle, PCBs can typically be manufactured within a day of the request if Eagle \*.brd files are submitted. For information on PCB design, I recommend [this tutorial by Brian Benchoff at Hackaday](https://hackaday.com/2016/09/22/making-a-pcb-eagle-part-1/). 

## Overview of Components
### Anker 5000 mAh Battery
This battery provides power to the Teensy and all of the components; it was sized based on the estimated current consumption of the device. It was calculated that the system will draw about 442 mA of current (2 mA from Bluetooth, 85 mA from each LIDAR, 100 from Teensy), so for a half-hour ride, only 221 mAh would be needed. Anker's 5000 mAh model was selected as the smallest and cheapest option, but other options may also be viable. The battery comes with a Micro-USB cable included for charging, but the micro-USB ports that I could find all seemed too small to easily solder to a PCB, so the board has a USB-A ("normal" USB) port instead, which are easier to solder, and still cheap & easy to find. Although the Teensy has a micro-USB port on it for power, connecting directly to this would make it impossible to measure the current draw, as the current sensor must be placed in series with the power source, so power must be provided through a separate USB port. 
The battery has a minimum current draw of 50 mA. We believe that the system will draw more than that, but **this would need to be verified experimentally**. 

### USB-A male-to-male cable
Since the board uses a USB-A port, a separate USB cable must be purchased to connect the battery to the board. A smaller cable would likely be best to prevent tangling. 

### Stewart Connector USB-A port
A USB-A port was chosen instead of a Micro-USB port because they appeared to be much easier to solder to a board, but any type of USB port should work, likely requiring changes to the footprint in the PCB file. This specific port was chosen because it was the cheapest one I could find on Digi-Key, but again, any USB port should work. 
The datasheet for this part did not specify which pin corresponded to what signal, so it had to be extrapolated based on similar connectors. **It needs to be verified experimentally which pin corresponds to 5V and which pin corresponds to ground**. 

### On/Off Switch 
This is a simple power switch to turn the device on or off, so that the battery power can be conserved when not in use. Any switch that holds its state and has leads attached to it can be used. Something like [this](https://www.adafruit.com/product/1092) would be fine, but the possibility of accidentally toggling the switch should be considered too, so a sliding switch might be better. The switch itself would be on the housing, and the leads coming off it would be soldered to the board. 

### Current Sensor 
The current sensor is used to estimate the current battery level by numerically integrating the current consumed over time. We never had the opportunity to test the current sensor, so everything involving it is entirely theoretical, including the wiring. The one used in the PCB is [this one from Allegro MicroSystems](https://www.digikey.com/product-detail/en/allegro-microsystems/ACS750LCA-050/ACS750LCA-050-ND/1006488), a default option provided in Eagle, which is now discontinued. It appears to have the same footprint as [this one](https://www.digikey.com/product-detail/en/allegro-microsystems/ACS770LCB-050B-PFF-T/620-1541-5-ND/4473980), which is still active. These current sensors may be bigger than we need, as they can sense up to 50 A of current, and the voltage outputted from them might be too low to be accurately read by the Teensy. **It may be better to use a different current sensor that is more suited to the range of currents being measured, and if the voltage is still too low, it may be best to amplify it with an op-amp.** It is also possible to calculate current by placing a small known resistor in series with the power source, where the current sensor would go, and measuring the voltage across it, but it is unclear how accurate this would be, and how much this would change the dynamics of the circuit. 

### Teensy 4.0 Microcontroller
This is the microcontroller that manages all of the sensors. It is faster and more powerful than an Arduino Uno, and should be fast enough to handle all the data being gathered. User-made Eagle libraries for the Teensy can be found [here](https://www.pjrc.com/teensy/eagle_lib.html), and the one used in this design is [the one by Constantin](https://forum.pjrc.com/threads/935-Eagle-library-with-Teensy-3-0-footprint?p=20178&viewfull=1#post20178) ("Teensy_3_and_LC_Series_Boards_v1.4.zip"). The Teensy 4.0 has largely the same pinout as the Teensy 3.2 and 3.1, so the Teensy 3.2/3.1 board available in the library is the footprint used in this design. The pins that are used all seem to be the same between 4.0 and 3.2, but **the wiring should be verified experimentally**. 

### Garmin LIDAR-Lite v4 LED
The LIDAR is used to measure the distance to various objects in the environment. Using multiple LIDARs, the speed of passing objects can be calculated. If two LIDARs are placed facing to one side of the bike with a known distance offset in the direction of motion, then the lag between the signals that the two LIDARs read can be used to calculate the speed of the passing object relative to the speed of the bike. This lag can be calculated with cross correlation, with the MATLAB function [xcorr()](https://www.mathworks.com/help/matlab/ref/xcorr.html), or the NumPy function [np.correlate()](https://numpy.org/doc/1.18/reference/generated/numpy.correlate.html), The distance between the LIDARs divided by the time lag between the signals is the speed of the passing object, relative to the bike. With an accurate measurement of the bike speed, coming from the app, the speed of the passing object relative to the ground can be calculated. Tests were done with the previous iteration of this device, [the v3](https://buy.garmin.com/en-US/US/p/557294), and it did not seem to be accurate enough, although only one device was tested. Regardless, it was decided to use the v4 because, according to the specs, it is more accurate, cheaper, and uses less power than its predecessor, however no tests could be done with it. The LIDARs communicate via I2C, and each one needs a different I2C address for proper communication. This can be done programatically with the [LIDAR-Lite Arduino Library](https://github.com/garmin/LIDARLite_Arduino_Library). The wiring was done based on their [specs sheet](http://static.garmin.com/pumac/LIDAR-Lite%20LED%20v4%20Instructions_EN-US.pdf) and comments in their example code, including the two resistors and the capacitor, so **it all needs to be verified experimentally**. 

### Adafruit Bluefruit UART Friend
This is the Bluetooth communication module that establishes a connection with the phone to send LIDAR data. It is not currently in the PCB as we had difficulties with reliably sending/receiving data. **Much more testing needs to be done with Bluetooth.** This device uses the Bluetooth Low Energy protocol, which is distinct from conventional Bluetooth. All the necessary information for this device can be found at the link above. 

## PCB design info
### PCB Files
There are 3 custom library files (\*.lbr) included in this folder: one for the LIDAR, one for the USB, and one for the Teensy. The Teensy library is the one mentioned above, and the other two are simple ones that I made, as I couldn't find EAGLE files for them online. The .brd file is the PCB layout, the .sch file is the schematic, and the .step file is a 3D model used in the CAD. 
### LIDAR Connection
The LIDAR footprint is just 10 holes in two rows spaced 0.1" apart, since the LIDAR itself doesn't have any method of connecting to a board. A port like [this](https://flytron.com/connectorscables/254-10-pin-isp-male-connector-header.html) could be soldered on, and then a ribbon cable soldered to the LIDAR with a plug on the other side could be used to easily connect to the board. 
