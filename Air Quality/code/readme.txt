List of Files and Contents:

***kickstart.py***
kickstart will run at boot. It will call i2c.py and serial_read.py in a while loop. 
The loop will continually check the status of the switch. When the switch is off the scipt will spin, when the switch is on the script will run the two files.
bash.rc hold the command the execute kickstart. A terminal is opened in /etc/xdg/lxsession/LXDE/autostart at startup and then bash.rc runs the script.
Data collected is sent to the file "datalog.txt" This file is appended to and never overwritten. It is located in /home/pi (the root directory) on the raspberry pi.
It extract the data plug in a usb drive and copy it over.

testing\temperature\Adafruit_Python_DHT
This folder holds the library that controlls the reading of the ADC.
See the folder README.md


***** AirMaster.py *******(not used)
Contains all the relevant code from the other three python scripts.
It also connects to the server and sends JSON data every 4-5 seconds.

The following three files are test scripts
Once each was working the code was added to AirMaster.py

***** USBserial.py***** (not used)
This script will initialize and read from the USB port.

***** serial_read.py***** 
This script will read from the GPS that is connected to the tx and rx 
lines. It also isolates the desirable data and parses it out.

***** i2c.py ***** 
This code will use the Adafruit_Python_DHT library to read i2c.
It will also scale the values in an attempt to convert them to ppm.

***** DustSensor.ino***** 
This is arduino code that runs on the teensy arduino.
Reads analog value from PM sensor every second and sends over USB