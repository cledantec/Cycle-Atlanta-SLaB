package com.woodruff.SLaB;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.media.MediaRecorder;
import android.os.Build;
import android.os.Bundle;
import android.os.Looper;
import android.view.KeyEvent;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Calendar;
import java.util.Date;
import java.time.Instant;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import static android.hardware.Sensor.TYPE_GYROSCOPE;


public class MainActivity extends AppCompatActivity{
    private int k = 1;
    private FusedLocationProviderClient fusedLocationClient;
    private LocationCallback locationCallback;
    private String logFileName = null;
    private String sensorDataAccel = "NULL";
    private String sensorDataGyro = "NULL";
    private int buttonCounter = 0;
    private MediaRecorder myAudioRecorder;
    private LocationRequest locationRequest;
    private String fileDir;

    private boolean recordAudio = false;
    private boolean writeHeader = false;
    private boolean writeHeaderFLC = false;
    private boolean isRecording = false;
    private String headerText = "Time,Latitude,Longitude,Dist_Acc,Speed,Speed_Acc,Altitude,Alt_Acc,Gyro_X,Gyro_Y,Gyro_Z,Accel_X,Accel_Y,Accel_Z";

    private SensorManager mSensorManager;
    private Sensor mAccelerometer;
    private Sensor mGyro;


    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Initialize sensor manager
        mSensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        //Create location request for FLC
        locationRequest = LocationRequest.create();
        locationRequest.setInterval(0);
        locationRequest.setFastestInterval(0);
        locationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        //Create location callback for FLC
        locationCallback = new LocationCallback(){
            @RequiresApi(api = Build.VERSION_CODES.O)
            @Override
            public void onLocationResult(LocationResult locationResult) {
                if(locationRequest==null){
                    return;
                }
                for (Location location: locationResult.getLocations()) {
                    double FLCLat = location.getLatitude();
                    double FLCLong = location.getLongitude();
                    double FLCSpeed = location.getSpeed()*2.23694;
                    double FLCAlt = location.getAltitude()*3.281;
                    double FLCRadialAcc = location.getAccuracy()*3.281;
                    double FLCSpeedAcc = location.getSpeedAccuracyMetersPerSecond()*2.23694;
                    double FLCVertAcc = location.getVerticalAccuracyMeters()*3.281;
                    Date currentTime = Calendar.getInstance().getTime();

                    logFLCData(FLCLat,FLCLong,FLCSpeed,FLCAlt,FLCRadialAcc,FLCVertAcc,FLCSpeedAcc);
                    TextView FLCText = (TextView)findViewById(R.id.fusedLoc);
                    FLCText.setText("Time: " + currentTime + "\nLatitude: " + Double.toString(FLCLat) + "\nLongitude: " + Double.toString(FLCLong) + "\nSpeed: " + Double.toString(FLCSpeed)
                    + " mph" + "\nAlt: " + Double.toString(FLCAlt) + " ft" +"\nCounter: " + Integer.toString(k));
                    k = k+1;
                }
            }
        };

        Switch audioSwitch = (Switch) findViewById(R.id.recordAudio);
        audioSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked){
                    recordAudio = true;
                }else{
                    recordAudio = false;
                }
            }
        });
        audioSwitch.setEnabled(true);
        Button logDataButton = (Button)findViewById(R.id.logData);
        logDataButton.setEnabled(true);
        TextView debugText = (TextView)findViewById(R.id.debugMode);
        debugText.setEnabled(true);
        debugText.setTextColor(Color.BLUE);

        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    Activity#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for Activity#requestPermissions for more details.
            return;
        }

        //Fused Location Client
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
    }

    //Display counter for button presses
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        switch (keyCode) {
            case KeyEvent.KEYCODE_VOLUME_UP:
                TextView textView = (TextView) findViewById(R.id.buttonStatus);
                textView.setText(Integer.toString(buttonCounter));
                buttonCounter+=1;
        }
        return super.onKeyDown(keyCode, event);
    }
    @Override
    public boolean onKeyUp(int keyCode, KeyEvent event) {
        switch (keyCode) {
            case KeyEvent.KEYCODE_VOLUME_UP:
                TextView textView = (TextView) findViewById(R.id.buttonStatus);
                textView.setText(Integer.toString(buttonCounter));
        }
        return super.onKeyDown(keyCode, event);
    }

    //Function to log FLC data
    @RequiresApi(api = Build.VERSION_CODES.O)
    public void logFLCData(double Lat, double Long, double Speed, double Alt, double DistAcc, double AltAcc, double SpeedAcc) {
        // Do something in response to button
        File logFLCFile;
        if(logFileName!=null)
        {
            logFLCFile = new File(getExternalFilesDir("FLC Trip Data"),"FLC_"+logFileName);

        }
        else
        {
            logFLCFile = new File(getExternalFilesDir("FLC Trip Data"),"Undated.txt");
        }

        if (!logFLCFile.exists())
        {
            try
            {
                boolean fileStatus = logFLCFile.createNewFile();
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }

        }
        if(logFLCFile.exists())
        {
            fileDir = getFilesDir().toString();
        }
        try
        {
            Instant instant = Instant.ofEpochMilli(Calendar.getInstance().getTimeInMillis());
            BufferedWriter buf = new BufferedWriter(new FileWriter(logFLCFile,true));
            if(writeHeaderFLC){
                buf.append(headerText);
                buf.newLine();
                writeHeaderFLC = false;
            }
            buf.append(instant.toString() + "," + Lat + "," + Long + "," + DistAcc + "," + Speed + "," + SpeedAcc +"," + Alt + ","+ AltAcc +"," + sensorDataGyro + "," + sensorDataAccel);
            buf.newLine();
            buf.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }

    }

    public void startDebugMode(View v){
        Toast.makeText(MainActivity.this,"Developer Mode",Toast.LENGTH_SHORT).show();
        Intent intent = new Intent(this, DebugModeActivity.class);
        intent.putExtra("FILE_LOCATION",fileDir);
        startActivity(intent);
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    public void startDataLogging(View view) {
        if(!isRecording){
            TextView textView = (TextView) findViewById(R.id.statusDisp);
            textView.setText("Data Is Logging");
            textView.setTextColor(Color.GREEN);
            isRecording = true;

            Date currentTime = Calendar.getInstance().getTime();
            logFileName = currentTime.toString()+".txt";
            writeHeader = true;
            writeHeaderFLC = true;

            fusedLocationClient.requestLocationUpdates(locationRequest,locationCallback, Looper.getMainLooper());
            Switch audioSwitch = (Switch) findViewById(R.id.recordAudio);
            audioSwitch.setEnabled(false);
            Button logDataButton = (Button)findViewById(R.id.logData);
            logDataButton.setText("Stop Data Log");
            TextView debugText = (TextView)findViewById(R.id.debugMode);
            debugText.setEnabled(false);
            debugText.setTextColor(Color.GRAY);

            //Create sensors and register listeners
            mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            mGyro = mSensorManager.getDefaultSensor(TYPE_GYROSCOPE);
            mSensorManager.registerListener(accelListener, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
            mSensorManager.registerListener(gyroListener, mGyro,SensorManager.SENSOR_DELAY_NORMAL);

            //Record Audio if enabled
            if(recordAudio){
                File audioOutputFile = new File(getExternalFilesDir("FLC Trip Data"),currentTime.toString()+".m4a");
                myAudioRecorder = new MediaRecorder();
                myAudioRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
                myAudioRecorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
                myAudioRecorder.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB);
                myAudioRecorder.setOutputFile(audioOutputFile);
                try {
                    myAudioRecorder.prepare();
                    myAudioRecorder.start();
                } catch (IllegalStateException ise){
                    return;

                }catch (IOException e) {
                    e.printStackTrace();
                    return;
                }
            }
        }else{
            isRecording = false;
            fusedLocationClient.removeLocationUpdates(locationCallback);
            mSensorManager.unregisterListener(accelListener);
            mSensorManager.unregisterListener(gyroListener);
            Switch audioSwitch = (Switch) findViewById(R.id.recordAudio);
            audioSwitch.setEnabled(true);
            Button logDataButton = (Button)findViewById(R.id.logData);
            logDataButton.setText("Log Data");
            TextView debugText = (TextView)findViewById(R.id.debugMode);
            debugText.setEnabled(true);
            debugText.setTextColor(Color.BLUE);

            TextView textView = (TextView) findViewById(R.id.statusDisp);
            textView.setText("Data is NOT Logging");
            textView.setTextColor(Color.RED);

            if(recordAudio) {
                if(myAudioRecorder != null){
                    //Stop Audio Recording
                    myAudioRecorder.stop();
                    myAudioRecorder.release();
                    myAudioRecorder = null;
                }
            }
        }
    }


    public SensorEventListener accelListener = new SensorEventListener() {
        @Override
        public void onSensorChanged(SensorEvent event) {
            String sensorName = event.sensor.getName();
            sensorDataAccel = (event.values[0] + "," + event.values[1] + "," + event.values[2]);
        }
        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
        }
    };
    public SensorEventListener gyroListener = new SensorEventListener() {
        @Override
        public void onSensorChanged(SensorEvent event) {
            String sensorName = event.sensor.getName();
            sensorDataGyro = (event.values[0] + "," + event.values[1] + "," + event.values[2]);
        }
        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
        }
    };
}
