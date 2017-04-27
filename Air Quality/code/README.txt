List of Files and contents:

testing\temperature\Adafruit_Python_DHT
This folder holds the library that controlls the reading of the ADC.
See the folder README.md


***** AirMaster.py *******
Contains all the relevant code from the other three python scripts.
It also connects to the server and sends JSON data every 4-5 seconds.

The following three files are test scripts
Once each was working the code was added to AirMaster.py

***** USBserial.py***** 
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