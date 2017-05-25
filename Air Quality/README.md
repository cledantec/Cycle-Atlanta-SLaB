# Air Quality & GPS Sensor readme

Code for running air quality and GPS sensors. 

Installation 
============

Copy all files in the RaspberryPi directory to the home directory of the Raspberry Pi.
Install the Adafruit Python DHT and ADS1x15 libraries in the 'dependencies' directory (see README there for details—you will need an active network connection to install their dependencies).

To run:

```
sudo python ~/air_quaility/aq_init.py
```
To autorun, edit the ~/.config/lxsession/LXDE-pi/autostart file by adding:

```
@python /home/pi/airquality/aq_init.py
```

Old Code
--------
Located in the 'unused' directory, these source files aren't used or were renamed for production.

*AirMaster.py*
Contains all the relevant code from the other three python scripts.
It also connects to the server and sends JSON data every 4-5 seconds.

The following three files are test scripts
Once each was working the code was added to AirMaster.py

*USBserial.py*
This script will initialize and read from the USB port.

*serial_read.py* 
This script will read from the GPS that is connected to the tx and rx 
lines. It also isolates the desirable data and parses it out.

*i2c.py*
This code will use the Adafruit Python DHT library to read i2c.
It will also scale the values in an attempt to convert them to ppm.

*DustSensor.ino* 
This is arduino code that runs on the teensy arduino.
Reads analog value from PM sensor every second and sends over USB