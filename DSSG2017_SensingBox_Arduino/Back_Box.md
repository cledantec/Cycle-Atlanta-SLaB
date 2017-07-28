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

