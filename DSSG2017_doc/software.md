Software Systems
========

### <span style="color:grey">Table of Contents</span>
1. [Raspberry Pi Server Installation](#raspberry)
2. [Raspberry Pi Linux Configurations](#config)
3. [Copying Data from Pi to a USB Stick](#data)
4. [Folder Structure and Useful Scripts](#folder)
5. [Arduino Sensor Control](#arduino)
6. [Creating an Image File from a Pi SD Card](#image)

<a name="raspberry"></a>
## Raspberry Pi Server Installation
If you want to install a Linux system in a SD card, you can import the Pi image that was created from the most recent system configurations/set-ups. The image file is about 16GB and is in the Google Drive (SLaB Resources/SD Images/DSSG_pi.img.zip). 

1. Download the image file to your local machine and unzip it.
2. Insert a SD card to your computer.
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
All the configurations are already done, but you can change it as needed. 

#### Auto Start
Auto start in the command-line mode is configured at 

```
/etc/rc.local
```
You can write down the script that you want to automatically run as the system starts. 

#### Auto Login
Auto login is configured in the Raspberry Pi's configuration menu. 

```
sudo raspi-config
```
You can go to `3. Boot Options` -> `B1 Desktop / CLI` -> `Console Autologin`.
After selecting desired booting option, reboot the system.

## Copying Data from Pi to a USB Stick
Since Pi is using the command-line mode, it is a bit tedious to transfer the collected data out of the Pi system (or copying files into the system). Before starting, a USB stick and the sensor box needs to be connected. Also, all the power needs to be shutdown. The steps are as follows:

1. When a USB stick, the Arduino data cable, a keyboard, and a monitor are connected (using a USB hub, if necessary), turn on the power from the sensor box. Then, the booting screen shows up on the monitor. Wait until automatically running the scripts. 
2. Once it starts collecting data, you need to stop the scripts. However, it's impossible to stop automatically running scripts. Press `Command + Right Arrow` to open a new terminal.
3. Log in to the Linux using a default credential (ID: `pi`, PW: `raspberry`).
4. Open the auto start configuration file.<br>
```
sudo vi /etc/rc.local
```
5. Comment out the shell script execution line `/home/pi/new_start.sh &` by adding `#` at the very beginning of the line. You can type it after changing to the editor mode by hitting `i`.  
6. By hitting `esc` key, change back to the command mode. 
7. Save the file by typing `:wq` + Enter.
8. On the command line, type `reboot` and Enter.
9. The system reboots itself. After rebooting, it does not auto start.
10. Go to the `data` folder. <br>``` cd data```
11. Mount the USB stick to the system.<br> 
```
sudo mount -t vfat /dev/sda1 /mnt/usb
```
12. Copy the newly collected data to the USB stick. Feel free to use wildcard (*) to copy them over altogether.<br>
```
sudo cp [file_name] /mnt/usb
``` 
13. Unmount the USB stick.<br>
```
sudo umount /mnt/usb
```
14. Revert the commented line back in `/etc/rc.local` and save it.
15. Turn off the power.
16. Disconnect the monitor and keyboard, and put the cables back.

** If you want to copy files from a USB stick to the Pi file system, you can take the same step. 

<a name="folder"></a>
## Folder Structure and Useful Scripts
Locations of important files in the Pi Linux system are listed below.

#### The Main Trigger Script for Servers
This shell script triggers all the Python and Node.js servers.

```
/home/pi/new_start.sh
```

#### RestAPI Server
This Python server runs RestAPIs that provide URLs/APIs for other servers. Whenever it receives GPS data from the GPS Receiver server, it updates the global time in a variable so it can be used as timestamps.

```
/home/pi/matrix-creator-malos/src/js_test/server_opt.py
```

#### Arduino Receiver
This Arduino Receiver server sends out "g" or "f" commands to Arduino through the serial port. "g" commands Arduino to send back a row of sensor data, and "f" forces it to reset itself. If it receives Arduino data correctly, it converts data into a JSON format, and posts it to the `/proximity` API. 

```
/home/pi/matrix-creator-malos/src/js_test/arduino_receiver.py
```

#### GPS Receiver
This Python server collects GPS data every second by reading the serial port to the GPS device. When receiving data correctly, it saves it to the `/home/pi/data/` folder as a JSON file. At the same time, it posts the data to the `/gps` API so to update the global time.

```
/home/pi/matrix-creator-malos/src/js_test/gps_receiver.py
```

#### Node.js Servers for Matrix Sensors and LED Control
These files contains Node.js scripts that collect data from sensors on Matrix, and post them to RestAPIs. 

```
/home/pi/matrix-creator-malos/src/js_test/test_imu_server.js
/home/pi/matrix-creator-malos/src/js_test/test_humidity_server.js
/home/pi/matrix-creator-malos/src/js_test/test_uv_server.js
/home/pi/matrix-creator-malos/src/js_test/test_pressure_server.js
```

Everloop server controls LEDs through communicating with the RestAPI server.
```
/home/pi/matrix-creator-malos/src/js_test/test_everloop_server.js
```

#### GPS/Arduino Testing Scripts
Without running all the servers, it is possible to test the GPS device and Arduino by running the testing scripts. If everything works, GPS data and sensor data are printed every second. If you see "nack" or "reset" continuously, it means there are some errors in the hardware.

```
/home/pi/test_both.py
```


<a name="arduino"></a>
## Arduino Sensors Control
The code for sensor control from the Arduino board can be found at this [folder](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_SensingBox_Arduino/oneArduinoAllAggregated).

For the correct working of all of the required sensors, additional libraries are needed for the ADS1015 (ADC units on the gas sensors) and for the LIDAR sensors. They can be found in the repository for each sensor, in the Arduino library manager, but as well they are provided [here](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_SensingBox_Arduino/libraries%20to%20install).

<a name="image"></a>
## Creating an Image File from a Pi SD Card
If you want to create a new image file after making changes in the Pi, you can follow the following steps (Mac or Linux):

1. Eject the SD card from the Pi, and connect your computer.
2. In the command line:

```
# Unmount the SD card to make changes in the file system.
sudo diskutil unmount /dev/rdisk2
sudo diskutil unmountDisk /dev/rdisk2

# Create an image
sudo dd if=/dev/rdisk2 of=[out_path/output_file_name.img] bs=1m
```
This will take a few minutes.

Note that `/dev/rdisk2` can be with a different number (e.g., not 2 but 3) depending on Mac configurations. You need to check the exact file name for the SD card's symbolic link. 

****
#### PREV PAGE: [Hardware Systems](hardware.md)
#### NEXT PAGE: [Cases Design](cases.md)