Backlog
==========
**Issues, Solutions, and Future Suggestions**


## Gas sensor board
* [**Need to Check**] ADC address assignment<br>ADC behavior is inconsistent depending on the address pin assginment. According to the spec, connecting the address pin to GND sets its address to 0x48. Similarly, this pin to VDD (0x49), SDA (0x4A), and SDL(0x4B). However, only GND (0x48) shows a consistent ADC behavior, and others vary randomly. So if you want to use an address other than 0x48 for a testing purpose, you need to check the signals beforehand. Relevant information is available at [the hardware systems doc](hardware.md). 
* [**Things to Consider**] It is always better not to expose resistor legs. For now, resistor legs are exposed due to their sizes. It's better to use shorter resistors to fit them into the slots. 
* [**To-Do**] Gas sensor value adjustment<br>One thing that we found is that baseline ADC readings for each gas sensor was different from each other. This means we cannot use a simple formula to calculate actual gas values in ppm. The official gas values and our sensor values at the same space/time are already collected, so actual adjustment needs to be made. See [the hardware systems doc](hardware.md) for the details.
* [**Done**] Amplifying resisters<br>The amplifying resistor in the 2nd op-amp was 500K in the first board. Since we did not have 500K resistors, we first tried 560K and the signal was not coming in correctly. After doing some testing, we found that it cannot be more than 530K. As soon as it goes over 530K, the sensor signal stops coming in. We thus soldered 470K resistors for R6.
* [**Done**] A gas sensor address changed<br>One of the gas sensors in the complete box was using 0x49 and was working fine when running independently. When connected them with lidars, it stopped working. So we had to move the address to 0x48 instead. This is an unexpected behavior and need to check in the future whenever using different addresses.

## GPS
* [**Done**] GPS's "EN" pin needs to be connected to VDD. Otherwise, the GPS starts working for a minute after running the script and stops randomly.

## Arudino Receiver and GPS Reciever
* [**Done**] Serial communication randomly stops and raises no error <br>In the loop of collecting data from Arduino and GPS, sometimes Arduino or GPS does not send out the data back to Pi, and the Receiver server waits forever. In order to prevent this, we implemented a timeout handler. After a few seconds, if there's no response from a data collection script, it raises an TimeoutError, and the error handler sends out "reset" signals to units. 
* [**Done**] Dealing with "NACK" signal from Arudino<br>Whenever Arduino starts collecting data, it sends out "NACK" signal. Sometimes, it keeps coming in until we reset the Arduino board. To deal with this, we first changed the data collection logic from "polling" to "command-based" one. Pi sends out a "f" signal which means "reset Arduino" when starting up the system. And then sends out "g" signal. The next data coming in contains "WINWIN", that means Arduino correctly started. Then, it keeps sending out "g" and collect data. If "nack" signal comes in again, it automatically sends "f" again to reset the Arudino board. This mechanism makes the system fault tolerant from software- and signal-level failures. 
* [**Done**] Separating GPS and Arduino Receivers<br> Originally, GPS and Arduino data collection scripts were all together. While we need to collect Arduino's sensor data more frequently, the speed is bounded by the GPS speed - 1 second is the maximum speed for GPS. So we separate it into two servers. 

## Arduino Board
* [**Done**] Pin 12 and Reset pin on Arduino were connected with a 1.2K resistor to implement software-driven hard-reset functionality. This makes it possible to use "f" signal (reset) from Pi. 
* [**Need to Check**] Too much solder creates a hardware error<br> If too much solder is applied to a wiring on the bridge (especially for SDA and SDL pins), Arduino randomly stops with no reason. Removing some big solders resolved this kind of problems. An ideal way to deal with this is to make a custom PCB board for the Arduino bridge. Its Fritzing files are available in this repository. 

## Raspberry Pi Linux
* [**Done**] In order to fix the random assignments of USB ports to GPS and Arduino (i.e., sometimes, GPS connects to "ttyUSB0" and Arduino to "ttyUSB1" and sometimes, vice versa), we created symbolic links that check devices' vendor/product IDs and dynamically connects to ttyUSBx ports. For now, GPS is using a symbolic link called "cycle_gps" and Arduino is connected to "cycle_arduino". These rules can be specified at `/etc/udev/rules.d/99-usb-serial.rules` inside the Pi's Linux system. For the details, see [this article](https://unix.stackexchange.com/questions/66901/how-to-bind-usb-device-under-a-static-name). 

## Sensor Pin Connections
* [**Need to Check**] Wire Orders <br> For now, the pin orders of sensor connectors (wires) are not consistent. Some are reversed way, and some are correct way. In the sensor boxes, we made sure that they're correct for each box, but in the future, it is necessary to check wiring orders whenever you change something in each box. 

****
#### PREV PAGE: [Data Analysis](data.md)