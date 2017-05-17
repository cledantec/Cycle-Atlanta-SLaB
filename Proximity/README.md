# Raspberry Pi code

## Python code for collecting data, storing on the drive and sending status,data over the network
Refer to bootScript.py under RaspberryPi folder.
Run the script with super user privileges (sudo python bootScript.py)

Note: Include all the other files in the folder (the lidar_lite module) for the script to run successfully.

## Turning it into a bootable script
* Navigate to /home/pi/.config/lxsession/LXDE-pi
*Edit the file autostart and add the following line at the end: @python  /home/pi/bootScript.py (A reference file can be found in RaspberryPi folder.)

## Arduino code
Refer to sensorAggregate.ino under Arduino folder.
* In Arduinio IDE, open the sketch.
* Connect the Arduino and click on program.
* If the programming fails, make sure you select the correct serial port and run again.


## Data Analysis

*Run the file giveSummary.py from the directory where the data files are stored. By default, this path is /home/pi/data/

Typical ouput expected is:

 Trip 1 Summary ************
Number of parked cars: 0
Number of parked trucks:0
Approx. number of pedestrians / other short obstacles: 0

 Trip 2 Summary ************
Number of parked cars: 6
Number of parked trucks:1
Approx. number of pedestrians / other short obstacles: 50

 Trip 3 Summary ************
Number of parked cars: 14
Number of parked trucks:3
Approx. number of pedestrians / other short obstacles: 86

 Trip 4 Summary ************
Number of parked cars: 12
Number of parked trucks:2
Approx. number of pedestrians / other short obstacles: 97