# Android App
The Android app is responsible for collecting location data, speed, and other phone sensor data. Several methods of obtaining a 
phone’s location were tested. For Android devices, the two main ways of obtaining device location are through using 
Android Location Manager (ALM) or Google Play Services’ Fused Location Client (FLC). ALM utilizes GPS, network providers, and 
passive providers. This includes using satellites, cell towers, and locations determined by other applications. FLC is built on 
top of ALM. FLC automatically chooses the best provider for the device’s location and is in turn much quicker to update and log a 
device’s location. Comparing the two, FLC provided more accurate data with less lag. The current app utilizes FLC to report the 
phone's location and speed. The app has been tested on a Samsung Galaxy S10 and is currently named "SLaB".

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

## Bluetooth
Initial testing was done to determine if Bluetooth(BT) could be used to send data between a BT module and a phone. The app created for testing is named "Blueteeth GATT". The BT module used for testing was the [Adafruit Bluefruit LE UART Friend](https://www.adafruit.com/product/2479). This BT module utilizes [Bluetooth Low Energy](https://developer.android.com/guide/topics/connectivity/bluetooth-le) instead of conventional Bluetooth. This involves using a GATT profile to send attributes over a BLE link. 

### Connecting Devices
Normally, the app would need to scan for BLE devices, pair, and connect before sending data. However, for the current app, the module is manually linked in the phone's BT settings before testing. 

### Bluetooth Adapter
A Bluetooth Adapter is required for BLE activity. In the main activity:

`private BluetoothAdapter bluetoothAdapter;`  

And within the onCreate method:

`bluetoothAdapter = bluetoothManager.getAdapter();`

Then app checks that Bluetooth is enabled and that a connection with the BLE module is established. If not, a request should be made for the user to enable BT and connect to the BT module: 

```
if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled()) {
    Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
    startActivityForResult(enableBtIntent, 0);
}
```

### GATT Connection
Next, the app checks that the correct module is connected. If the module is the "Adafruit Bluefruit LE" module, a connection is made to the GATT server on the BLE device and a [BluetoothGattCallback](https://developer.android.com/reference/android/bluetooth/BluetoothGattCallback) is used to perform operations:

```
pairedDevices = bluetoothAdapter.getBondedDevices();
if (pairedDevices.size() > 0) {
    for (BluetoothDevice device : pairedDevices) {
        if(device.getName().equals("Adafruit Bluefruit LE")){
            statusBox.setText(device.getName());
            BluetoothGatt BTGatt = device.connectGatt(this, true, gattCallback);
        }
        else{
            statusBox.setText("Plz Connect to Bluefruit");
        }
    }
}
else{
    statusBox.setText("No Connected Devices");
}
```

### Bluetooth GATT Callback
The GATT callback uses several methods to perform BT operations. The `onConnectionStateChange()` method can be used to check that a successful GATT connection was made and start discovering services:

```
public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
super.onConnectionStateChange(gatt, status, newState);
if(status == BluetoothGatt.GATT_SUCCESS && newState == BluetoothProfile.STATE_CONNECTED){
    try {
        Thread.sleep(500);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    gatt.discoverServices();
}else if(status != BluetoothGatt.GATT_SUCCESS){
    gatt.disconnect();
}
}
```

Sometimes it is useful to have the thread sleep for 500 ms before beginning service discovery to ensure the GATT connection is made.

The `onServicesDiscovered()` method can be used to get the service from the BLE device as well as read and write characteristics using from the service. The service, read characteristic, and write characteristic have different UUIDs that are specific to the BLE module. These UUIDs are used to get the correct service and characteristic in order to communicate and perform operations with the BLE module:

```
BluetoothGattService BTservice = gatt.getService(UUID.fromString("6e400001-b5a3-f393-e0a9-e50e24dcca9e"));
BluetoothGattCharacteristic WriteCharacteristic = BTservice.getCharacteristic(UUID.fromString("6e400002-b5a3-f393-e0a9-e50e24dcca9e"));
BluetoothGattCharacteristic ReadCharacteristic = BTservice.getCharacteristic(UUID.fromString("6e400003-b5a3-f393-e0a9-e50e24dcca9e"));
```

To **send data to** the BLE module, the value of the write characterstic can be set and then written:

```
WriteCharacteristic.setValue("ASDFJKL");
gatt.writeCharacteristic(WriteCharacteristic);
```

To **receive data from** the BLE module, a characterstic notification must be set and enabled with the Bluetooth Descriptor:

```
gatt.setCharacteristicNotification(ReadCharacteristic,true);
BluetoothGattDescriptor descriptor = ReadCharacteristic.getDescriptor(UUID.fromString("00002902-0000-1000-8000-00805f9b34fb"));
descriptor.setValue(BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
gatt.writeDescriptor(descriptor);
```

With the notification set, once a characteristic change is detected, the `onCharacteristicChange` method will be called. The incoming data can then be extracted and displayed or saved. 

```
public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic){
  String inputText = characteristic.getStringValue(0);
 }
```

## Running the App
### Enabling USB Debugging
In order for the app to install on an adroid device from Android Studio, USB debugging must be enabled in the developer options on the phone. Normally, developer options are not shown. 

- If using an Android phone, go to Settings > About phone > Build number. 
- On a Samsung Galaxy device, go to Settings > About phone > Software information > Build number. 
- On an HTC device, go to Settings > About > Software information > More > Build number. 
- On an LG device, go to Settings > About phone > Software info > Build number.

Tap Build number seven times. After a few taps, steps counting down until developer options are unlocked should appear. Once activated, go back to Settings and developer options should be at the bottom of the menu. Under "Debugging" in the developer options, enable "USB debugging".

### Installing the App
To install the app on an Android device, connect the android device to a computer with Android studio running. If the device is connected and developer mode is enabled, the phone should show in a tool bar at the top of Android studio.

Simple click the green "Run" button to install the app on the phone.

### Enabling Permissions
To run the "SLaB app, location and mircophone permissons must be granted for the app. These can granted in the phone settings under apps. For the "Blueteeth GATT" app, make sure Bluetooth for the phone is enabled and the correct Bluetooth module is connected.

### Using the App
Once permissions are granted, the app should be functional. 
- To record data, simple press the "LOG DATA" button. 
- To enable audio recordings, switch the "Audio Record" to the on position before starting data collection. 
- To enter developer mode, press the text at the bottom. 
- To go back to the main screen from developer mode, use the back arrow at the top of the screen.

## Future Work
Future work for the app should focus on integrating Bluetooth functionality into the main "SLaB" app. 

