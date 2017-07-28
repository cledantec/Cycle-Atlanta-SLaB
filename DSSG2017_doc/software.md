Software Systems
========

### <span style="color:grey">Table of Contents</span>
1. [Raspberry Pi Server Installation](#raspberry)
2. [Raspberry Pi Linux Configurations](#config)
3. [Raspberry Pi RestAPIs](#rest)
4. [Pi-to-Arduino Serial Communications](#socket)
5. [Arduino Sensor Control](#arduino)

<a name="raspberry"></a>
## Raspberry Pi Server Installation
If you want to install a Linux system in a SD card, you can import the Pi image that was created from the most recent system configurations/set-ups. The image file is about 16GB and is in the Google Drive (SLaB Resources/SD Images/DSSG_pi.img.zip). 

1. Unzip the file.
2. Insert the SD card to your computer.
3. In the command line, execute the following commands (Mac or Linux):

```
# Unmount the SD card to make changes in the file system.
sudo diskutil unmount /dev/rdisk2
sudo diskutil unmountDisk /dev/rdisk2

# Write the image to the SD card.
sudo dd bs=1m if=bike.img of=/dev/rdisk2
```

Once this operation is done, you can eject the SD card from your computer, and insert it to the Raspberry Pi. Then all the configurations/software for the sensor system are already installed in the server and the Pi is ready to use.

<a name="config"></a>
## Linux Configurations 
All the configurations are already done, 

* **Auto Start**
* **Auto Login**

<a name="rest"></a>
## RestAPIs for Data Collection and LED Control

<a name="socket"></a>
## Pi-to-Arduino Serial Communications


<a name="arduino"></a>
## Arduino Sensors Control
The code for sensor control from the Arduino board can be found at this [folder](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_SensingBox_Arduino/oneArduinoAllAggregated).

For the correct working of all of the required sensors, additional libraries are needed for the ADS1015 (ADC units on the gas sensors) and for the LIDAR sensors. They can be found in the repository for each sensor, in the Arduino library manager, but as well they are provided [here](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_SensingBox_Arduino/libraries%20to%20install).

## Creating an Image File from a Pi SD Card
If you want to create a new image file after making changes in the Pi configurations, you can follow the following steps (Mac or Linux):

****
#### PREV PAGE: [Hardware Systems](hardware.md)
#### NEXT PAGE: [Cases Design](cases.md)