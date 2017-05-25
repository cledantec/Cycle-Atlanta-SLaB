# Raspberry Pi code

Python code for collecting proximity data, storing on the drive and sending status,data over the network.

Installation 
============

Copy all files in the RaspberryPi directory to the home directory of the Raspberry Pi.
Note: Include all the other files in the folder (the lidar_lite module) for the script to run successfully.

To run:

```
sudo python ~/proximity/proximity_init.py
```
To autorun, edit the ~/.config/lxsession/LXDE-pi/autostart file by adding:

```
@python /home/pi/proximity/proximity_init.py
```

# Arduino code

Refer to sensorAggregate.ino under Arduino folder. This will run all four sensors (2x Lidar Lite, 2x ultra-sound).


# Data Analysis

For a sample analysis of proximity data, run the file giveSummary.py from the directory where the data files are stored. By default, this path is /home/pi/data/
*Note: may not work as data file format has changed (from flat csv to json).*

Typical ouput expected is:

*Trip 1 Summary*
Number of parked cars: 0
Number of parked trucks:0
Approx. number of pedestrians / other short obstacles: 0

*Trip 2 Summary*
Number of parked cars: 6
Number of parked trucks:1
Approx. number of pedestrians / other short obstacles: 50

*Trip 3 Summary*
Number of parked cars: 14
Number of parked trucks:3
Approx. number of pedestrians / other short obstacles: 86

*Trip 4 Summary*
Number of parked cars: 12
Number of parked trucks:2
Approx. number of pedestrians / other short obstacles: 97