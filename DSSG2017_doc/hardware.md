Hardware Systems
=======
### <span style="color:grey">Table of Contents</span>

1. [Securing Raspberry Pi and Matrix](#matrix)
2. [GPS](#gps)
3. [Pi-to-Arduino Communication](#commo)
4. [Arduino and Sensor Connections (Bridge Board)](#arduino)
5. [Gas Sensors](#gas)
6. [Sensor Box Design](#box)


<a name="matrix"></a>
## Securing Rapspberry Pi and Matrix
Even though the connection between Pi and the Matrix board is sturdy, Matrix Creator can be detached from the Pi board when shaking a lot during the riding. This led us to secure the Matrix board by tying them through Matrix holes. We used two pieces of wires to secure them. Also, to prevent the shocks between the Pi board and the Matrix board, we put a small piece of Yoga matt between them. Several tests showed that this is a very secure way to make them safely operate. 


<a name="gps"></a>
## GPS Fabrication
Our GPS system consists of a GTPA010 device, a CP2102 USB-to-TTL device, and a small piece of PCB board. As you can see in the picture below, we connected the GPS module to the CP2102 device directly, and used a piece of PCB board as an intermediate bridge. This unit is finally attached to Pi's USB port. 

The reason that we do this is that while the GPS module uses a serial communication as a means to talk to other devices, the USB port of the Pi board is *NOT* a serial port. So, it is necessary to convert "serial communication" signals to TTL (Transistor-Transistor-Logic) signals that USB ports use. The software part for making use of this GPS module is available at [the software system document](software.md).

It is easy to make mistakes when connecting the pins and it is so hard to unsold them especially when you have already finished it, so pay attention to the connection during all the time of soldering. 

![gps](https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/gps2.jpg?raw=true)

The **connections of pins** are as follows. Please note that GTPA010 **DOES NOT** use 5V for VDD, but use 3.3V that comes out of a small pin in the CP2102 device. 

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/gpsStructure4.png?raw=true" width=600px>

The code uses the default settings of the GPS and returns the following data: **course**, **longitude**, **latitude**, **speed**, **day**, and, **utc_time**

   
<a name="commo"></a>
## Pi-to-Arduino Communication
From the outside view, the Master Unit, particularly the Raspberry Pi, and the sensor box are connected through a male-to-male USB cable. Similar to the GPS module, however, the Pi uses a TTL signal for its USB while the Arduino board uses serial signals. So there is another USB-to-TTL device inside the sensor box on the back side. The brand of this USB-to-TTL device is different from the GPS one. Arduino's serial data swings between 0V to 5V while TTL signals swing between 0V and 3.3V. The USB-to-TTL device in the sensor box automatically deals with this power change. However, we do not use VDD between the Pi and Arduino since each of them uses its own power for data signals. Thus, only three wires, i.e., TX, RX, and GND, are connected through the USB-to-TTL device. 

**Note that TX from the USB-to-TTL device is connected to the RX of Arduino, and vice versa.**


<a name="arduino"></a>
## Arduino and Sensor Connections (Bridge Board)
From the hardware perspective, the connections of the sensors to the Arduino board is made through a shield/bridge-board mounted on top of the Arduino.

The documentation for the wiring of the box has been designed using Fritzing, common software in the Arduino and Raspberry Pi community. It can be downloaded for free from [its website](http://fritzing.org/home/). Additional parts libraries may be required depending on the particular version of the program, but they can be add *ad hoc* from the own program. It is particularly important for being able to use LIDAR or thrid-party components not that common for Arduino users.

![BreadboardView](https://github.com/cledantec/Cycle-Atlanta-SLaB/raw/master/DSSG2017_SensingBox_Arduino/Fritzing_Schema/PCB%20Cycle%20Atlanta/BackBoxConnections_BreadboardView.png)
*Breadboard view of the connections*

![SchematicView](https://github.com/cledantec/Cycle-Atlanta-SLaB/raw/master/DSSG2017_SensingBox_Arduino/Fritzing_Schema/PCB%20Cycle%20Atlanta/BackBoxConnections_SchematicView.png)
*Schematic view of the connections*

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_SensingBox_Arduino/Fritzing_Schema/PCB%20Cycle%20Atlanta/BackBoxConnections_PCBView.png?raw=true">

*PCB view of the connections (2-layer Design)*

The original Fritzing file for editing and designing a custom PCB board in the same software can be found [here](https://github.com/cledantec/Cycle-Atlanta-SLaB/raw/master/DSSG2017_SensingBox_Arduino/Fritzing_Schema/PCB_BackBox_2layers.fzz) for downloading. Original bridge boards were completely wired manually, although a custom PCB would be highly advisable in the future.


<a name="gas"></a>
## Gas Sensors
We made use of the following gas sensor design from the Spring 2017 team.

![gps](https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/gasSensor.png?raw=true)

We made seven of them and these are our observations from try-and-error testing. 

1. The holes for resistors in the gas sensor boards are small and different sizes, it was so hard to push the lead of the resistors down, and for those resistors which did not fit into the holes we replace them with smaller resistors different in voltage. For instance, we replaced the 560 K Ohms resitor with 470 K Ohms resitor. This replacement worked fine. 

2. Gas sensor board's behaviour are not consistent. Three out of seven fabricated boards (#1, 4, 7) works fine, and the rest of them has a flaw in at least one sensor. Detailed information about each of the seven sensor boards is found [here](https://docs.google.com/spreadsheets/d/18mLQVb0HjoA-88Tq4y8rYqyIrmJ9yjPXizwVc3SuRZM/edit?usp=sharing).
		
					
<a name="box"></a>
## Sensing Box design

The back unit is in charge of collecting proximity and air quality data, as well as providing energy to the whole system.

The case of the back unit is based on a basic electricity connection box made of ABS plastic which is laser cut for providing the required slots for the sensors as well as the ventilation inlets.

Sources files for their fabrication are found [here](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_SensingBox_Arduino/ABS_laser_cutting).

The box is screwed directly on a rack which is mounted in the back part of the bike. After different iterations, direct drilling and screwing with an elastic material between the box and the rack is showed as the most solid alternative.

Inside the box the components which can be found are the following ones:

- a powerbank for providing energy to the whole system.
- 2 LIDAR sensors for proximity on left and right sides.
- 3 SONAR sensors for proximity on left, right, and rear sides.
- a PM NOVA sensor for detecting Particulates Matters under 10μm and 2.5μm as air quality metric.
- a custom gas sensor board for the detection of ozone, carbon monoxide, sulfur dioxide, and nitrogenn dioxide as air pollution metric from other vehicles.
- an Arduino UNO board gatherㄴ all the data from those sensors.

[![Assembly](https://img.youtube.com/vi/Jq7rCaWT5Fk/0.jpg)](https://www.youtube.com/watch?v=t7hX2DIzW0o "Assembly")<br>
*Timelapse of the assembly of the box v.1.0.3*

The box is completed by providing electric power to the Arduino board and outlet externally for the Raspberry located on the front unit of the bike, as well as completing the TTL-to-USB connection for communicating the Arduino with the Raspberry Pi.

The assembly of the component of the box can be followed on the posted video. The only difference in the last iteration of the design is the replacement of the wooden board separating the battery and the Arduino board by a yoga mat under the microcontroller.


****
#### PREV PAGE: [System Overview](overview.md)
#### NEXT PAGE: [Software Systems](hardware.md)

