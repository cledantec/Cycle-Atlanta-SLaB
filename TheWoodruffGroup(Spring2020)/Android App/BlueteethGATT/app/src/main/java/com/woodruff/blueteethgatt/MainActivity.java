package com.woodruff.blueteethgatt;

import androidx.appcompat.app.AppCompatActivity;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;

import java.util.List;
import java.util.Set;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {
    private BluetoothAdapter bluetoothAdapter;
    private BluetoothDevice device;
    private Set<BluetoothDevice> pairedDevices;
    public List<String> dataList;
    public String dataString = "Data: ";




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView statusBox = (TextView)findViewById(R.id.status);


        // Initializes Bluetooth adapter.
        final BluetoothManager bluetoothManager = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
        bluetoothAdapter = bluetoothManager.getAdapter();

        // Ensures Bluetooth is available on the device and it is enabled. If not,
        // displays a dialog requesting user permission to enable Bluetooth.
        if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, 0);
        }

        pairedDevices = bluetoothAdapter.getBondedDevices();
        if (pairedDevices.size() > 0) {
            for (BluetoothDevice device : pairedDevices) {
                if(device.getName().equals("Adafruit Bluefruit LE")){
                    statusBox.setText(device.getName());
                    BluetoothGatt BTGatt = device.connectGatt(this, true, gattCallback);

                    //BTGatt.discoverServices();

                    //BluetoothGattService BTservice = BTGatt.getService(UUID.fromString("6e400001-b5a3-f393-e0a9-e50e24dcca9e"));
                    //BluetoothGattCharacteristic WriteCharacteristic = BTservice.getCharacteristic(UUID.fromString("6e400002-b5a3-f393-e0a9-e50e24dcca9e"));
                    //WriteCharacteristic.setValue("ASDFJKL");
                    //BTGatt.writeCharacteristic(WriteCharacteristic);

                }
                else{
                    statusBox.setText("Plz Connect to Bluefruit");
                }
            }
        }
        else{
            statusBox.setText("No Connected Devices");
        }

    }


    private BluetoothGattCallback gattCallback = new BluetoothGattCallback() {
        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            super.onConnectionStateChange(gatt, status, newState);
            TextView statusBox = (TextView)findViewById(R.id.status);
            statusBox.setText("Connection Changed");
            int test = 2;
            if(status == BluetoothGatt.GATT_SUCCESS && newState == BluetoothProfile.STATE_CONNECTED){
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                gatt.discoverServices();
                statusBox.setText("Trying to Discover Services");
            }else if(status != BluetoothGatt.GATT_SUCCESS){
                gatt.disconnect();
                statusBox.setText("Gatt Disconnected");
            }
        }
        public void onServicesDiscovered(BluetoothGatt gatt,int status){
            TextView statusBox = (TextView)findViewById(R.id.status);
            statusBox.setText("Services Discovered!");
            BluetoothGattService BTservice = gatt.getService(UUID.fromString("6e400001-b5a3-f393-e0a9-e50e24dcca9e"));
            BluetoothGattCharacteristic WriteCharacteristic = BTservice.getCharacteristic(UUID.fromString("6e400002-b5a3-f393-e0a9-e50e24dcca9e"));
            BluetoothGattCharacteristic ReadCharacteristic = BTservice.getCharacteristic(UUID.fromString("6e400003-b5a3-f393-e0a9-e50e24dcca9e"));
            WriteCharacteristic.setValue("ASDFJKL");
            gatt.setCharacteristicNotification(ReadCharacteristic,true);
            BluetoothGattDescriptor descriptor = ReadCharacteristic.getDescriptor(UUID.fromString("00002902-0000-1000-8000-00805f9b34fb"));
            descriptor.setValue(BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
            gatt.writeDescriptor(descriptor);
            gatt.writeCharacteristic(WriteCharacteristic);
            //gatt.readCharacteristic(ReadCharacteristic);
            //writeToBT(gatt,WriteCharacteristic);
            //gatt.readCharacteristic(ReadCharacteristic);

        }

        public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic){
            byte[] dataInput = characteristic.getValue();
            TextView statusBox = (TextView)findViewById(R.id.read);
            TextView dataBox = (TextView) findViewById(R.id.dataText);
            String inputText = characteristic.getStringValue(0);
            dataString = dataString + inputText;
            statusBox.setText(inputText);
            dataBox.setText(dataString);
            dataList.add(inputText);
            //statusBox.setText(inputText);

        }
        public void onCharacteristicRead(BluetoothGatt gatt,BluetoothGattCharacteristic readChar,int status){
            TextView statusBox = (TextView)findViewById(R.id.read);
            statusBox.setText("LMAO READ CHAR");

        }


    };


}
