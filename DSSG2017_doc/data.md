Data Analysis
=======

Our long-term goal is to refine and complement the LTS model by supplementing sensor data in addition to the survey/interview data, because some of dynamic objects such as cars and people are hardly identified through survey/interview in a quantitative way. However, if we want to detect environmental factors by making use of sensor data, it is essential to distinguish between different objects (sensor data itself does not imply any contents of the environment). Without distinguishing between different factors, operationalizing the LTS model using sensor data can be hardly justified. This process is critical in advancing to informed decision-making based on objective datasets. In order to detect sementic-level objects beyond the sensor-level recognition, we use machine learning techniques to classify environmental factors. The process to analyze data is as follows. 

## Ground-Truth Data Collection 
When collecting the data, we installed a GoPro camera on the bike along with sensor systems. This was to collect ground-truth data. If we want to detect sementic-level factors, we need to know what objects actually exist around the bike way. 

## Data Syncronization
Since GoPro does not keep the real time, it was necessary to sync between the video and sensor data. Sensor data's timestamps are based on the GPS data, so the time was accurate. Meanwhile, the video had only times based on the play time. In order to sync them, we used a corner of the map as a reference point. 

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/gps_reference.png?raw=true" style="width: 500px;"/>

In other words, we first plotted the GPS data on the map, and pin-pointed the timestamp of the data point at the corner. Also, in the video, the cornering time was captured as a sync point. Based on these reference times, other times were matched each other. The final data table looks like this (`time` is the GPS time, and `video_time` is the time of the corresponding video):

|  ...| day   | time  | video_time | lon   | lat   |   USRight  |  more...| 
| ---- |:-----:| :-----:| :-----:| :---:| :------: | :-------:|:-----:|
| | 220717 |03:49:37| 00:02:28  |  -84.3895| 33.77709 |  308.18    |  |
|  |220717 |03:49:38| 00:02:29  |-84.3895| 33.77709  |  589.91    |  | 


## Classifier Generation

Given the syncronized data, we recorded surrounding environment every second by watching the GoPro video. When recording the surrounding factors, we classified them into specific labels. Major objects found on the left *or* right side of the bike were considered **classifiers**. These classifiers were generated separately for the left and right sides (so there are two different kinds of classifiers each second). 

Since the stress level of the riders can vary depending on different types of objects, we tried to distinguish a similar type of objects based on their status. For instance, our classifiers for a car are in the following table.

|     Object   | Classifier  Name |     
| ------------- |:-------------:| 
| a parked car    | Car Stop|
| a moving car     | Car |   
| cars parked in parallel  | Parallel| 

Classifying the objects on the left and right side of the bike from the video was a long process since we had to pause the video every second to write down the objects found. Once we had documented our findings, we added them to a CSV file containing the data captured by the sensors. The following table is an example of one of our csv files. 

|   ...| day   | time  | video_time | LS Classifier | RS Classifier |  USRight  |  USLeft |  USRear| LidarR| LidarL |...| 
| ----- |:------:| :-----:| :-----:| :------:| :------: | :------:| :-----:|:-----:| :---:| :---:| :----:| :-------:| :------:| :---:|      
| |220717 |03:49:37| 00:02:28  |    Parallel   |  Parallel     |  308.18    | 640.08  |  640.08 |619.333| 1778.66| 
|  |220717 |03:49:38| 00:02:29  |           |  Tree      |  589.91    | 640.08  |  640.08 |832.25| 1      | 
|  |220717 |03:49:39| 00:02:30  |            |  Tree      |  642.62    | 640.08  |  640.92 |506   | 603    | 
|  |220717 |03:49:40| 00:02:31  |           |  Tree      |  642.11    | 640.08  |  640.08 |521.2 | 366.2  | 
|   |220717 |03:49:41| 00:02:32  |   Parallel    |  Parallel |  487.68    | 640.08  |  640.08 |433   | 616.333| 
|  |220717 |03:49:42| 00:02:33  |               |  Car Stop  |  148.59    | 640.71  |  641.35 |114.5 | 943.5  | 
|  |220717 |03:49:43| 00:02:34  |               |  Car Stop  |  241.93    | 640.08  |  641.35 |744.5 | 770    | 


## Inter-Reliability Test

#### Two coders
Classifying process was conducted by two members of our team separately. They followed the same steps without discussing their findings between each other. The only thing they discussed was the classifier labels so they have a same label for the same object. After the two coders clssified all the data in the CSV file, the inter-reliability scores were calculated based on the agreement rate.   
| LS Classifier | RS Classifier       
| :--------: |:-------:| 
|   81%         | 64%|


Since the inter-reliability score for the RS classifier was not satisfactory, both coders discussed the criterion in classfing objects, and repeated the process. In the second interation, the scores increased as follows:

| LS Classifier | RS Classifier       
| :------: |:-------------:| 
|   86%            | 76%|

We cannot say these scores are perfect, but reasonable at this time for doing some analysis. Special attention should be put on the labels of the classifiers. Different labels for a same object can be a cause of a low inter-reliabilty score. These are the list of our classifiers in the first iteration: **Tree**, **Bike**, **Parallel**, **Car Stop**, **Car**, **Trash Can**, **Wall**, **Cone**, **Bike racks**, **Tunnel**, **Person**, and, **Road sign** 


## Sensor Data Processing (1): Converting to the Distance Domain 

## Sensor Data Processing (2): Interpolation

## Sensor Data Processing (3): Resampling

## Sensor Data Processing (4): Gaussian Smoothing

## Sensor Data Processing (5): Feature Generation using DCT

## Predictions using SVM and Random Forest



## Future Work





