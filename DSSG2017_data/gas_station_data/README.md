Gas Station Data for Sensor Calibraition
=========
Myeong Lee (myeong@umd.edu)
-----

This data is collected at the Atlanta Sensing Station located at the Atlanta Power by co-locating our sensors.
The timestamps of the data are not correct since we used Linux time in Raspberry Pi. The actual time range that the data was collected is from July 12th 8:50 AM to July 14th 8:20 AM (approximately). The data was collected every 2 seconds in the code, but it is not exactly 2 seconds due to the data collection time lag (so a bit more than 2 sec), so the time interval in the data timestamp can be 2 or 3 seconds (but their actual intervals are same). 

The sensors needs to be calibrated using official sensor data from the sensing station. Also, temperature and humidity needs to be taken into account since these factors affect gas sensor readings. The official data is provided by Raj Lal, a Ph.D. student from the department of Environmental Science.

For the calibration data collection, we used only three sensor boards (#1, 4, 7), since these are only sensors that showed stable signals out of all the fabricated sensors (so, each entry in the dataset shows three sets of sensory data). The rest of the sensors that were not placed for calibration needs to be further debugged or replaced. 

