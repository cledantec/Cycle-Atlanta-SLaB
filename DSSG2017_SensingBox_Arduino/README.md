# Back Sensing Box design

The back unit is in charge of collecting proximity and air quality data, as well as, providing energy to the whole system.

The case of the back unit is based on a basic electricity connection box made of ABS plastic which is laser cut for providing the required slots for the sensors as well as the ventilation inlets.

Sources files for their fabrication are found [here](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_SensingBox_Arduino/ABS_laser_cutting).

The box is screwed directly on a rack which is mounted in the back part of the bike. After different iterations, direct drilling and screwing with an elastic material between the box and the rack is showed as the most solid alternative.

Inside the box the components which can be found are the following ones:

- a powerbank for providing energy to the whole system
- 2 LIDAR sensors for proximity on left and right sides.
- 3 SONAR sensors for proximity on left, right, and rear sides.
- a PM NOVA sensor for detecting Particulates Matters under 10μm and 2.5μm as air quality metric.
- a custom gas sensor board for the detection of ozone, carbon monoxide, sulfur dioxide, and nitrogenn dioxide as air pollution metric from other vehicles.
- an Arduino UNO board as microcontroller which gather all the data from those sensors.

From the software perspective, the code for the communication between the sensors and the Arduino board are provided in this [folder](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_SensingBox_Arduino/oneArduinoAllAggregated).

For the correct working all of the required sensors, additional libraries are needed for the ADS1015 (custom gas sensors board) and for the LIDAR sensors. They can be found on the repositories for each sensor, in the Arduino library manager, but as well they are provided [here](https://github.com/cledantec/Cycle-Atlanta-SLaB/tree/master/DSSG2017_SensingBox_Arduino/libraries%20to%20install).

From the hardware perspective, the connections of the sensors to the Arduino board is made through a shield / bridge-boards mounted on top of the microcontroller.

The documentation for the wiring of the box has been designed on Fritzing, common software in the Arduino and Raspberry Pi community. It can be downloaded for free from [its website](http://fritzing.org/home/). Additional parts libraries may be required depending on the particular version of the program, but they can be add *ad hoc* from the own program. It is particularly important for being able to use LIDAR or thrid-party components not that common for Arduino users.

![BreadboardView](https://github.com/cledantec/Cycle-Atlanta-SLaB/raw/master/DSSG2017_SensingBox_Arduino/Fritzing_Schema/PCB%20Cycle%20Atlanta/BackBoxConnections_BreadboardView.png)
*Breadboard view of the connections*

![SchematicView](https://github.com/cledantec/Cycle-Atlanta-SLaB/raw/master/DSSG2017_SensingBox_Arduino/Fritzing_Schema/PCB%20Cycle%20Atlanta/BackBoxConnections_SchematicView.png)
*Schematic view of the connections*

The original Fritzing file for editing and designing a custom PCB board in the same software can be found [here](https://github.com/cledantec/Cycle-Atlanta-SLaB/raw/master/DSSG2017_SensingBox_Arduino/Fritzing_Schema/PCB_BackBox_2layers.fzz) for downloading.

Original bridge boards were completely wired manually, although a custom PCB would be highly advisable in the future.

The box is completed by providing electric power to the Arduino board and and outlet externally for the Raspberry located on the front unit of the bike, as well as completing the TTL to USB connection for communicating the Arduino with the Raspberry Pi.

The assembly of the component of the box can be followed on the posted video. The only difference in the last iteration of the design is the replacement of the wooden board separating the battery and the Arduino board by a yoga mat under the microcontroller.

[![Assembly](https://img.youtube.com/vi/Jq7rCaWT5Fk/0.jpg)](https://www.youtube.com/watch?v=t7hX2DIzW0o "Assembly")
*Timelapse of the assembly of the box v.1.0.3*




