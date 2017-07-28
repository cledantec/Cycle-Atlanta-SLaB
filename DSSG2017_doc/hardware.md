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

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/gpsStructure5.png?raw=true" width=600px>

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

#### Observations and Try-and-Error Refinements

1. The holes for resistors in the gas sensor boards are small and different sizes, it was so hard to push the lead of the resistors down, and for those resistors which did not fit into the holes we replace them with smaller resistors different in voltage. For instance, we replaced the 560 K Ohms resitor with 470 K Ohms resitor. This replacement worked fine. 

2. Gas sensor board's behaviour are not consistent. Three out of seven fabricated boards (#1, 4, 7) works fine, and the rest of them has a flaw in at least one sensor. Detailed information about each of the seven sensor boards is found [here](https://docs.google.com/spreadsheets/d/18mLQVb0HjoA-88Tq4y8rYqyIrmJ9yjPXizwVc3SuRZM/edit?usp=sharing).


#### Circuits
A raw value from ADC is a 12-bit reading of voltage status when the power supply is from 0 to 5V. Since an OP-AMP supplies 2.5V as the ground voltage to the final amplifier, the 12-bit value comes out of the range between 0 and 2.5V. So, the raw values can vary, theoretically, between 0 to 2048 where 0 means 0V and 2048 means 2.5V. Even if all the circuit settings and sensor type are same, however, the baseline voltage that comes out of each sensor can vary. Thus, it is required to figure out the baseilne values when none of the target gases exists. 

**Baseline Calibration** In order to get the baseline values of all sensors, we used Wine Preserver Gas in a vacuum bag. First we made a gas sensor testbed that can connect up to three gas boards (using different addresses). The Arduino code for this and sample data coleected is available at the [testbed folder](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_gas_testbed). After pulling out the air out the vacuum bag, we sprayed the wine preserver gas into the bag and see how the values change. Some photos and graphs for this are as follows:

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/images/gas_calibration_setting.jpg" width="500px">
<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/Gas_board1_good.png?raw=true" width="500px">
<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/Gas_board2_bad.png?raw=true" width="500px">

The baseline values can be calculated by averaging the second half of the values (after the signals become stable). The board 2 graph shows that some sensors never become stable. In this case, we mark it as "bad". The overall status of the gas sensors is presented at the [Google Spread Sheet](https://docs.google.com/spreadsheets/d/18mLQVb0HjoA-88Tq4y8rYqyIrmJ9yjPXizwVc3SuRZM/edit?usp=sharing).

**Gas Value Calculation** The gas sensor board composed of two OP-AMP devices, four sensors, and an ADC. Each op-amp chip has four op-amps embedded in it. Each sensor uses two op-amps. The first op-amp is for supplying a stable voltage to the sensor. Our base power for all the sensors is 5V, and the first op-amp supplies 2.5V power to the sensor. The sensor's voltage change outputs to the input of the second op-amp.  

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/gas_circuit.png?raw=true" width="700px">

The second op-amp actually amplifies the sensor signal. The amplification rate is determined by dividing R6 by R5 (150 Ohm now). So the actual voltage change due to a gas stimulus can be calculated as follows:

```
# the units are V
V_gas = (V_out - V_base) / amplification_rate 
```
where `amplification_rate = R6/R5`, `V_out = (2.5V * ADC_reading_output)/2048`, and `V_base = (2.5V * ADC_reading_base)/2048` (here, ADC_reading_base is coming from the mean of the vacuum bag gas values.

Once we have `V_gas` value in V, it's possible to calculate the actual ppm or ppb value of the gas.
For example, if looking at the [CO sensor's data sheet](https://www.spec-sensors.com/wp-content/uploads/2016/04/3SP_CO_1000-P-Package-110-102.pdf), the spec says the sensitivity is 4.75 nA/ppm. This means `V_gas = (4.75nA * CO_ppm) * 150 Ohm`. Thus,

```
CO_ppm = V_gas / (4.75nA * 150 Ohm)
```

Of course, there can be electrical noise, bias, and the impact of other sensors. These need to be adjusted. The impact of temperature, humidity, and other gases can be adjusted based on the data sheet's information. Also for ensuring the accuracy of the gas sensors, we co-located out testbed at the offical Atlanta gas station. 

**Official Sensing Station** Even though we calculated gas values correctly using formula, it is possible that gas sensors are biased electrically. So, the best way to adjust it is to use the real gas values as ground-truth and adjust them empirically given the theoretical values. We co-located gas sensors at the station for 48 hours, and observed how they change over time. The official gas sensor values are available at [this folder](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_data/gas_station_data). We used gas board #1, #4 and $7 since they were only boards without erroneous sensors. The testbed values are available at [this folder](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_data/gas_station_data/original_testbed). Based on these two datasets, we need to find a coefficient for each sensor, and adjust the values.


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
#### NEXT PAGE: [Software Systems](software.md)

