Data Analysis
=======
Erica Pantoja

# Classifier Generation

Our long term goal is to refine and complement the LTS model by supplementing valuable sensor data. Sensors are great to detect environmental factors, However, if we want to detect urban infrastructure by making use of sensors it is hard to detect what is there since sensors do not distinguish what object is what. So, in order to solve this, we recurred to machine learning techniques.  

##Process

First of all, by watching the video from the ride, we recorded per second the objects found to the left and right side of the bike, and classified them under specific labels. So every different object found to the left or right side of the bike was consider a **classifier**

Since the stress level of the riders can be affected differently by different type of objects, we tried to have an specific classification of objects. For instance, our classifiers for a car are in the following table.

|     Object   | Classifier       
| ------------- |:-------------:| 
| parked car    | Car Stop|
| moving car     | Car |   
| parallel: cars in both sides  | Parallel| 

Documenting the objects in the left and right side of the bike from the video was a long process since we had to pause the video every second to write down the objects found. Once we had documented our findings, we added them to a csv file containing the data captured by the sensors. The following table is an example of one of our csv files. 

|   course      | speed         | day   | time  | video_time | LS Classifier | RS Classifier | lon     | lat      | seq | way |   USRight  |  USLeft |  USRear| LidarR| LidarL | more...| 
| ------------- |:-------------:| -----:| -----:| ----------:| ------------: | -------------:| -------:|---------:| ---:| ---:| ----------:| -------:| -------:|------:| ------:| --------:|      
| 265.42        | 9.69           |220717 |03:49:37| 00:02:28  |    Parallel   |  Parallel     | -84.3895| 33.77709 | 167 | go  |  308.18    | 640.08  |  640.08 |619.333| 1778.66| 
| 266.82        | 9.69           |220717 |03:49:38| 00:02:29  |               |  Tree         | -84.3895| 33.77709 | 168 | go  |  589.91    | 640.08  |  640.08 |832.25| 1      | 
| 266.33        | 10.32          |220717 |03:49:39| 00:02:30  |               |  Tree         | -84.3896| 33.77709 | 169 | go  |  642.62    | 640.08  |  640.92 |506   | 603    | 
| 272.07        | 10.13          |220717 |03:49:40| 00:02:31  |               |  Tree         | -84.3896| 33.7771  | 170 | go  |  642.11    | 640.08  |  640.08 |521.2 | 366.2  | 
| 269.77        | 10.08          |220717 |03:49:41| 00:02:32  |   Parallel    |  Parallel     | -84.3897| 33.77710 | 171 | go  |  487.68    | 640.08  |  640.08 |433   | 616.333| 
| 233.86        | 11.47          |220717 |03:49:42| 00:02:33  |               |  Car Stop     | -84.3897| 33.77709 | 172 | go  |  148.59    | 640.71  |  641.35 |114.5 | 943.5  | 
| 220.14        | 13.39          |220717 |03:49:43| 00:02:34  |               |  Car Stop     | -84.3895| 33.77705 | 173 | go  |  241.93    | 640.08  |  641.35 |744.5 | 770    | 

###Inter-Reliability
**Two coders** 

This process was ejected by two remembers of our team individually, the followed the same steps without discussing their findings to each other. The only thing they discussed was the classifier labels so they do have same label for same object. After the two coders documented their findings in the CSV file individually, we were able to find the similarity percentage between them by using R studio. And this were the results:  

| LS Classifier | RS Classifier       
| ------------- |:-------------:| 
|   81%            | 64%|


The similarities percent in the RS classifier was so bad so both coders repeated the process and after that, and after reviewing their classifier labels we got the follow similarities percentage


| LS Classifier | RS Classifier       
| ------------- |:-------------:| 
|   86%            | 76%|

This new percentage is not good but not bad at this time, we believe that by analyzing more data this percentage will increase percentage will increase. Special attention should be put on the labels of the classifiers. Different labels for same objects can be the first cause of a low similarities percentage. 

This are some of our classifiers - **Tree**, **Bike**, **Parallel**, **Car Stop**, **Car**, **Trash Can**, **Wall**, **Cone**, **Bike racks**, **tunnel**, **Person**, and, **Road sign** 







