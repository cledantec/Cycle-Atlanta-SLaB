Data Analysis
=======

Our long-term goal is to refine and complement the LTS model by supplementing sensor data in addition to the survey/interview data, because some of dynamic objects such as cars and people are hardly identified through survey/interview in a quantitative way. However, if we want to detect environmental factors by making use of sensor data, it is essential to distinguish between different objects (sensor data itself does not imply any contents of the environment). Without distinguishing between different factors, operationalizing the LTS model using sensor data can be hardly justified. This process is critical in advancing to informed decision-making based on objective datasets. In order to detect sementic-level objects beyond the sensor-level recognition, we use machine learning techniques to classify environmental factors. The process to analyze data is as follows. 

## Ground-Truth Data Collection 
When collecting the data, we installed a GoPro camera on the bike along with sensor systems. This was to collect ground-truth data. If we want to detect sementic-level factors, we need to know what objects actually exist around the bike way. 

## Data Synchronization
Since GoPro does not keep the real time, it was necessary to sync between the video and sensor data. Sensor data's timestamps are based on the GPS data, so the time was accurate. Meanwhile, the video had only times based on the play time. In order to sync them, we used a corner of the map as a reference point. 

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/gps_reference.png?raw=true" style="width: 500px;"/>

In other words, we first plotted the GPS data on the map, and pin-pointed the timestamp of the data point at the corner. Also, in the video, the cornering time was captured as a sync point. Based on these reference times, other times were matched each other. The final data table looks like this (`time` is the GPS time, and `video_time` is the corresponding time of the video):

|  ...| day   | time  | video_time | lon   | lat   |   USRight  |  more...| 
| ---- |:-----:| :-----:| :-----:| :---:| :------: | :-------:|:-----:|
| | 220717 |03:49:37| 00:02:28  |  -84.3895| 33.77709 |  308.18    |  |
|  |220717 |03:49:38| 00:02:29  |-84.3895| 33.77709  |  589.91    |  | 


## Classifier Generation

Given the synchronized data, we recorded surrounding environment every second by watching the GoPro video. When recording the surrounding factors, we classified them into specific labels. Major objects found on the left *or* right side of the bike were considered **classifiers**. These classifiers were generated separately for the left and right sides (so there are two different kinds of classifiers each second). 

Since the stress level of the riders can vary depending on different types of objects, we tried to distinguish a similar type of objects based on their status. For instance, our classifiers for a car are in the following table.

|     Object   | Classifier  Name |     
| ------------- |:-------------:| 
| a parked car    | Car Stop|
| a moving car     | Car |   
| cars parked in parallel  | Parallel| 

Classifying the objects on the left and right side of the bike from the video was a long process since we had to pause the video every second to write down the objects found. Once we had documented our findings, we added them to a CSV file containing the data captured by the sensors. The following table is an example of one of our csv files. 

|   ...| day   | time  | video_time | LS Classifier | RS Classifier |  USRight  |  USLeft |  USRear| LidarR| LidarL |...| 
| ----- |:------:| :-----:| :-----:| :------:| :------: | :------:| :-----:|:-----:| :---:| :---:| :----:| 
| |220717 |03:49:37| 00:02:28  |    Parallel   |  Parallel     |  308.18    | 640.08  |  640.08 |619.333| 1778.66| |
|  |220717 |03:49:38| 00:02:29  |           |  Tree      |  589.91    | 640.08  |  640.08 |832.25| 1      | |
|  |220717 |03:49:39| 00:02:30  |            |  Tree      |  642.62    | 640.08  |  640.92 |506   | 603    | |
|  |220717 |03:49:40| 00:02:31  |           |  Tree      |  642.11    | 640.08  |  640.08 |521.2 | 366.2  | |
|   |220717 |03:49:41| 00:02:32  |   Parallel    |  Parallel |  487.68    | 640.08  |  640.08 |433   | 616.333| |
|  |220717 |03:49:42| 00:02:33  |               |  Car Stop  |  148.59    | 640.71  |  641.35 |114.5 | 943.5  | |
|  |220717 |03:49:43| 00:02:34  |               |  Car Stop  |  241.93    | 640.08  |  641.35 |744.5 | 770    | |


## Inter-Reliability Test

#### Two coders
Classifying process was conducted by two members of our team separately. They followed the same steps without discussing their findings between each other. The only thing they discussed was the classifier labels so they have a same label for the same object. After the two coders clssified all the data in the CSV file, the inter-reliability scores were calculated based on the agreement rate.   
| LS Classifier | RS Classifier       
| :--------: |:-------:| 
|   81%         | 64%|


Since the inter-reliability score for the RS classifier was not satisfactory, both coders discussed the criterion in classfing objects, and repeated the process. In the second interation, the scores increased as follows:

| LS Classifier | RS Classifier       
| :------: |:------:| 
|   86%    |  76% |

We cannot say these scores are perfect, but reasonable enough for doing some analysis. Special attention should be put on the labels of the classifiers. Different labels for a same object can be a cause of a low inter-reliabilty score. These are the list of our classifiers in the first iteration: **Tree**, **Bike**, **Parallel**, **Car Stop**, **Car**, **Trash Can**, **Wall**, **Cone**, **Bike racks**, **Tunnel**, **Person**, and, **Road sign** 


## Sensor Data Processing 
Given the nature of the sensory data such as high noise level and sensor errors, the data cannot be directly used in the raw format. There need to be several steps to clean up the signals instead. Some techniques for processing noisy sensor/electrical data are known in the field of signal processing. This section describes steps how the data are processed to be used for machine learning. Particularly, we focused on the proximity data (i.e., Lidars and Sonars). R scripts for this are available at [this location](https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/R/170722_Preprocessing.Rmd).

### (1) Converting to the Distance Domain 
Since the bike speed varies depending on the traffic and other factors, signal patterns can be different as well depending on it (even if the objects are same). This led us to normalize the speed by changing the time domain to the distance domain. Since GPS data provide the speed, it was possible to conver the domain easily in R. Some paramters/points to consider carefully are as follows:

* the GPS speed unit is "knot". 1 knot = 0.514444444 m/s
* the time interval of Lidar/Sonar data collection is 0.2994975 seconds (this was calculatated by dividing the entire time span by the number of rows). In the code, the loop time interval is set to 200ms, but the actual interval is a bit more than this due to the script execution time. 

```
distance (m) = speed (m/s) * time_interval (sec)
``` 
Once the proximity data is converted to the distance-domain signals, the signal pattern looks normalized and consistent regardless of bike spped. However, the intervals between data points become inconsistent (intervals vary depending on the speed). An example of the distance-domain data is as follows:

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/lidar_distance_based_close_up.png?raw=true" style="width: 100%;"/>

### (2) Interpolation
Before making the gaps between data points consistent, some errors that came from the sensorse themselves had to be fixed anyhow. One major observation from lidars is that the signal often goes down to 1 or 0 (cm), which in theory is not possible. In order to compensate this sensor errors, we adopted a simple interpolation method. The way we interpolate erroneous data points is to make them same to the previous values whenever the value goes down to 1 or 0. It is also possible to use other interpolation techniques to compensate missing sensory data, but in order to do that, some research on the characteristcs of sensors needs to be conducted, and appropriate assumptions about data need to be made. An example of the naïve interpolation result is shown below.

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/lidar_interpoliation_close_up_car_passing.png?raw=true" style="width: 100%;"/>

### (3) Resampling
Now, it is possible to resample the signal to make the gaps between data points consistent. By prorating the hights of the desired data points based on the distances between original data points, it was possible to reconstruct a fixed-distance axis. The data resolution was set to 1m as it was close to the median value of distance intervals in the distance domain. 

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/distances_density.png?raw=true" style="width: 100%;"/>

An example of resampled data is as follows:

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/resampled_lidar_car_passing.png?raw=true" style="width: 100%;"/>


### (4) Gaussian Smoothing
As the last step of the signal clean-up, the sensor noise was supressed using the Gaussian filter. The window size of the filter can be optimized in the future after conducting some sensitivity analysis. For the initial try, we set the window size to three for both lidars and sonars. The shape of the data before and after the smoothing is as below:

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/gaussian_lidar_eg.png?raw=true" style="width: 100%;"/>


### (5) Feature Generation using DCT
For generating features from the processed dataset, we decided to use the [Discrete Cosine Transform (DCT)](https://en.wikipedia.org/wiki/Discrete_cosine_transform) for making frequency-based patterns of environmental factors. Since the position of the object in a data segment can vary significantly depending on the time chunking strategies, and this variance in the patterns makes it hard to use the temporal signature of the data. This led us to convert the time-domain data into the frequency-domain data. We set the unit size of the data chunk to 15m (i.e., 15 points of data. The chunk size can be also tuned better after doing some testing), and generated frequency-domain signautres of all the 15m chunks from about 1550 observations. 

Since the frequency-based score for 0 (i.e., freq(0)) is high due to the boundary condition for DCT results, we removed values for 0, and took a vector of 28 elements as the feature (14 for a lidar, and 14 for a sonar).
An example frequency-based feature (when a car is passing by) is like this:

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/car_DCT.png?raw=true" style="width: 100%;"/>

## Predictions 
Using the vector of 28 frequency-based pattern feature, two machine learning algorithms, [Support Vector Machine (SVM)](https://en.wikipedia.org/wiki/Support_vector_machine) and [Random Forest](https://en.wikipedia.org/wiki/Random_forest) were used to predict the classifier of each data segment. To compare the performance of the prediction models to the baseline classification power (when randomly predicting classifiers), we plot them together with varying train-test sets. The results are as follows:

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/DSSG2017_data/graphs/prediction_base.png?raw=true" style="width: 100%;"/>


## Future Work
This data analysis is an initial exploration of data, and there are many parameters and methods that we can tune the prediction models (e.g., Gaussian window size, the size of data chunks, types of features in addition to the frequency-domain patterns, machine learning algorithms, and interpolation resolution). 

Actually, our overarching goal is to identify environmental factors that give rise to bike riders' stress level. In order for this, the identification of environment should be achieved first as sensors cannot detect semantic-level objects. Once we can tune and refine the prediction model for detecting environmental fators through feature engineering and modeling, it would be possible to advance to answering the real question -- how bicycle infrastructures and environmental factors affect bike riders' stress level? and how these relationships can be used for constructing the Level of Traffic Stress (LTS) model?



