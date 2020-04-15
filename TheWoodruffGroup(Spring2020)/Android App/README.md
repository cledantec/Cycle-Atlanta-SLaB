# Android App
The Android app is responsible for collecting location data, speed, and other phone sensor data. Several methods of obtaining a 
phone’s location were tested. For Android devices, the two main ways of obtaining device location are through using 
Android Location Manager (ALM) or Google Play Services’ Fused Location Client (FLC). ALM utilizes GPS, network providers, and 
passive providers. This includes using satellites, cell towers, and locations determined by other applications. FLC is built on 
top of ALM. FLC automatically chooses the best provider for the device’s location and is in turn much quicker to update and log a 
device’s location. Comparing the two, FLC provided more accurate data with less lag. The current app utilizes FLC to report the 
phone's location and speed. The app has been tested on a Samsung Galaxy S10.

The app features two modes which both record data. The main screen is meant to be utilized during experiments and test rides. This
screen displays the essentials for the app:
- Data Logging Status: Reports whether the app is currently able to write data to a text file.
- Audio Recording Switch: Switch to enable or disable optional audio recording. Must be set before logging data.
- Button Counter: Senses when the volume-up button is pressed.
- Relevant Location Data: Displays time, latitude, longitude, speed(mph), and altitude(ft).
- Counter: Counts the number of data points that have been recorded. Used to determine if data is being written to text file.
- Log Data Button: Large button pressed to being data logging. Disables audio recording switch and developer mode button.
- Developer Mode Button: Text that shows developer mode when pressed.

Developer mode has the same functionalities as the main screen but displays all data that is recorded. This extra data includes:
- Gyro Data
- Accelerometer Data
- File location
- Location accuracy data

While the main screen does not display these, they are still recorded and written to the stored text file.

## Build Environment
- The current app was developed using Android Studio 3.5.3. 
- The app has been tested on a Samsung Galaxy S10 with Android verison 10.
- Compile SDK version: 29
- Build Tools version: 29.0.3
- Application Min SDK version: 15
- Application Target SDK version: 29
- Application ID: "com.woodruff.SLaB"

## Dependencies
- implementation 'com.google.android.gms:play-services-games:19.0.0'
- implementation 'com.google.android.gms:play-services-location:17.0.0'

## Permissions
- "android.permission.BLUETOOTH"
- "android.permission.BLUETOOTH_ADMIN"
- "android.permission.INTERNET"
- "android.permission.ACCESS_FINE_LOCATION"
- "android.permission.ACCESS_COARSE_LOCATION"
- "android.permission.RECORD_AUDIO"

## Data Collected
Currently, the data collected includes:
- GPS Location - Longitude and latitude coordinates
- GPS Speed - Speed data as reported by the phone GPS, currently in mph
- GPS Altitude - Altitude data as reported by the phone GPS, currently in ft above the WGS 84 reference ellipsoid
- Accelerometer Data - Acceleration force in x, y, and z directions, currently in m/s<sup>2</sup>
- Gyroscope Data - Rate of rotation around x, y, and z axes, currently in rad/s
- Location Accuracy - Estimated horizontal accuracy of the location reported, currently in ft radially
- Speed Accuracy - Estimated speed accuracy as reported by the phone, currently in mph
- Altitude Accuracy - Estimated accuracy of the altitude reported, currently in ft
- Time - The time at which each data point was collected [yyyy-MM-ddTHH:mm:ss.SSS]

## File Location and Data Storage Format 
### File Location
The data collected by the app is written to a text file that is time stamped for when the file is created, or when data collection began.
Currently, the files are stored on the phone within the app's data folder in internal storage. To access the files, the "MyFiles" app on an Android phone 
can be used, or the phone can be connected to a computer and the file opened on a computer.

The files is located at: **Interal storage\Android\data\com.woodruff.SLaB**. Within the files folder, there are two folders for 
which data collected on the main mode and debug mode are stored. The folder "FLC Trip Data" contains data collected on the main screen,
while the folder "FLC Trip Data_Debug" contains data collected while in developer mode. Optional audio recordings are also stored
in these folders depending on which screen they are recorded from.

### Data Format in File
The data log file is a .txt file. The first line of the text file is a header which describes what data is collected and in what 
order the data is written to the text file. The data is comma-delimited, with each data point being time-stamped. Currently, 
the format is (Time,Latitude,Longitude,Dist_Acc,Speed,Speed_Acc,Altitude,Alt_Acc,Gyro_X,Gryo_Y,Gyro_Z,Accel_X,Accel_Y,Accel_Z).
The optional recordings are stored as mpeg4.
