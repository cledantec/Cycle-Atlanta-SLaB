package com.example.SLaB;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
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

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Instant;
import java.util.Calendar;
import java.util.Date;

import static android.hardware.Sensor.TYPE_GYROSCOPE;

public class DebugModeActivity extends AppCompatActivity {
    private int k = 1;
    private int buttonCounter = 0;

    private SensorManager mSensorManager;
    private Sensor mAccelerometer;
    private Sensor mGyro;
    private LocationCallback locationCallback;
    private MediaRecorder myAudioRecorder;
    private LocationRequest locationRequest;

    private String gyroData;
    private String accelData;
    private String logFileName = null;
    private String sensorDataAccel = "NULL";
    private String sensorDataGyro = "NULL";
    private String fileDir;

    private boolean startDataLogging;
    private boolean recordAudio = false;
    private boolean writeHeader = false;
    private boolean writeHeaderFLC = false;
    private boolean isRecording = false;
    private boolean isStressful = false;
    private String headerText = "Time,Latitude,Longitude,Dist_Acc,Speed,Speed_Acc,Altitude,Alt_Acc,Gyro_X,Gyro_Y,Gyro_Z,Accel_X,Accel_Y,Accel_Z,Stress_Status";

    private FusedLocationProviderClient fusedLocationClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_debug_mode);

        //Initialize sensor manager
        mSensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);

        //Create sensors and register listeners
        mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        mGyro = mSensorManager.getDefaultSensor(TYPE_GYROSCOPE);
        mSensorManager.registerListener(accelListener, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        mSensorManager.registerListener(gyroListener, mGyro,SensorManager.SENSOR_DELAY_NORMAL);

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

                    logFLCData(FLCLat,FLCLong,FLCSpeed,FLCAlt,FLCRadialAcc,FLCVertAcc,FLCSpeedAcc,isStressful);
                    TextView FLCText = (TextView)findViewById(R.id.FLCData_debug);
                    FLCText.setText("Time: " + currentTime + "\nLat: " + Double.toString(FLCLat) + "\nLong: " + Double.toString(FLCLong) + "\nSpeed(mph): " + Double.toString(FLCSpeed)
                            + "\nAlt(ft): " + Double.toString(FLCAlt) + "\nDist Acc(ft): " + Double.toString(FLCRadialAcc) + "\nSpeed Acc(mph): " + Double.toString(FLCSpeedAcc)
                            + "\nVert Acc(ft): +/-" + Double.toString(FLCVertAcc) + "\nStressful? "+ isStressful + "\nCounter: " + Integer.toString(k));
                    k = k+1;
                }
            }
        };

        Switch audioSwitch = (Switch) findViewById(R.id.recordAudioSwitch_debug);
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
        Button logDataButton = (Button)findViewById(R.id.startDataLog_debug);
        logDataButton.setEnabled(true);
        Button stopLogButton = (Button)findViewById(R.id.stopDataLog_debug);
        stopLogButton.setEnabled(false);

        Intent intent = getIntent();
        String fileLocation = intent.getStringExtra("FILE_LOCATION");

        TextView fileText = (TextView)findViewById(R.id.fileLocation_debug);
        fileText.setText("File Location: " + fileDir);

        //Fused Location Client
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this);

    }

    //Function to log FLC data
    @RequiresApi(api = Build.VERSION_CODES.O)
    public void logFLCData(double Lat, double Long, double Speed, double Alt, double DistAcc, double AltAcc, double SpeedAcc, boolean stressStat) {
        // Do something in response to button
        File logFLCFile;
        if(logFileName!=null)
        {
            logFLCFile = new File(getExternalFilesDir("FLC Trip Data_Debug"),"FLC_"+logFileName);

        }
        else
        {
            logFLCFile = new File(getExternalFilesDir("FLC Trip Data_Debug"),"Undated.txt");
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
            TextView textView = (TextView) findViewById(R.id.fileLocation_debug);
            //textView.setText("File Exists");
            textView.setText(getFilesDir().toString());
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
            buf.append(instant.toString() + "," + Lat + "," + Long + "," + DistAcc + "," + Speed + "," + SpeedAcc + "," + Alt + "," + AltAcc + "," + sensorDataGyro + "," + sensorDataAccel
            + "," + isStressful);
            buf.newLine();
            buf.close();
            TextView textView = (TextView) findViewById(R.id.writeStatus_debug);
            textView.setText("Writing to Log");
            textView.setTextColor(Color.GREEN);
        }
        catch (IOException e)
        {
            e.printStackTrace();
            TextView textView = (TextView) findViewById(R.id.writeStatus_debug);
            textView.setText("Not Writing to Log");
            textView.setTextColor(Color.RED);
        }

    }

    @Override
    protected void onStop() {
        super.onStop();
        mSensorManager.unregisterListener(accelListener);
        mSensorManager.unregisterListener(gyroListener);
        isRecording = false;
        startDataLogging = false;
        fusedLocationClient.removeLocationUpdates(locationCallback);
        if(recordAudio) {
            //Stop Audio Recording
            myAudioRecorder.stop();
            myAudioRecorder.release();
            myAudioRecorder = null;
            /*
            TextView textView = (TextView) findViewById(R.id.micStatus);
            textView.setText("MIC NOT RECORDING :((((");
            textView.setTextColor(Color.RED);
             */
        }
    }
    protected void onRestart() {
        super.onRestart();
        mSensorManager.registerListener(accelListener, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        mSensorManager.registerListener(gyroListener, mGyro,SensorManager.SENSOR_DELAY_NORMAL);
    }

    public SensorEventListener accelListener = new SensorEventListener() {
        @Override
        public void onSensorChanged(SensorEvent event) {
            String sensorName = event.sensor.getName();
            accelData = (sensorName + ":\nX: " + event.values[0] + "\nY: " + event.values[1] + "\nZ: " + event.values[2]);
            sensorDataAccel = (event.values[0] + "," + event.values[1] + "," + event.values[2]);
            TextView accelText = (TextView)findViewById(R.id.accelData_debug);
            accelText.setText("Accel Data: " + accelData);
        }
        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
        }
    };
    public SensorEventListener gyroListener = new SensorEventListener() {
        @Override
        public void onSensorChanged(SensorEvent event) {
            String sensorName = event.sensor.getName();
            gyroData = (sensorName + ":\nX: " + event.values[0] + "\nY: " + event.values[1] + "\nZ: " + event.values[2]);
            sensorDataGyro = (event.values[0] + "," + event.values[1] + "," + event.values[2]);
            TextView gyroText = (TextView)findViewById(R.id.gyroData_debug);
            gyroText.setText("Gyro Data: " + gyroData);
        }
        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
        }
    };

    @RequiresApi(api = Build.VERSION_CODES.O)
    public void startDataLogging(View view) {
        if(!isRecording){
            isRecording = true;
            // Do something in response to button
            startDataLogging = true;
            Date currentTime = Calendar.getInstance().getTime();
            logFileName = currentTime.toString()+".txt";
            writeHeader = true;
            writeHeaderFLC = true;

            fusedLocationClient.requestLocationUpdates(locationRequest,locationCallback, Looper.getMainLooper());
            Switch audioSwitch = (Switch) findViewById(R.id.recordAudioSwitch_debug);
            audioSwitch.setEnabled(false);
            Button logDataButton = (Button)findViewById(R.id.startDataLog_debug);
            logDataButton.setEnabled(false);
            Button stopLogButton = (Button)findViewById(R.id.stopDataLog_debug);
            stopLogButton.setEnabled(true);

            //Create sensors and register listeners
            mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            mGyro = mSensorManager.getDefaultSensor(TYPE_GYROSCOPE);
            mSensorManager.registerListener(accelListener, mAccelerometer, SensorManager.SENSOR_DELAY_NORMAL);
            mSensorManager.registerListener(gyroListener, mGyro,SensorManager.SENSOR_DELAY_NORMAL);

            TextView textView = (TextView) findViewById(R.id.recordStatus_debug);
            textView.setText("DATA IS RECORDING");
            textView.setTextColor(Color.GREEN);

            //Record Audio if enabled
            if(recordAudio){
                File audioOutputFile = new File(getExternalFilesDir("FLC Trip Data_Debug"),currentTime.toString()+".m4a");
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
        }
    }

    public void stopDataLogging(View view) {
        // Do something in response to button
        isRecording = false;
        startDataLogging = false;
        fusedLocationClient.removeLocationUpdates(locationCallback);
        mSensorManager.unregisterListener(accelListener);
        mSensorManager.unregisterListener(gyroListener);
        Switch audioSwitch = (Switch) findViewById(R.id.recordAudioSwitch_debug);
        audioSwitch.setEnabled(true);
        Button logDataButton = (Button)findViewById(R.id.startDataLog_debug);
        logDataButton.setEnabled(true);
        Button stopLogButton = (Button)findViewById(R.id.stopDataLog_debug);
        stopLogButton.setEnabled(false);
        TextView textView = (TextView) findViewById(R.id.recordStatus_debug);
        textView.setText("DATA IS NOT LOGGING");
        textView.setTextColor(Color.RED);
        TextView writeText = (TextView) findViewById(R.id.writeStatus_debug);
        writeText.setText("Not Logging");
        writeText.setTextColor(Color.RED);
        if(recordAudio) {
            if(myAudioRecorder != null){
                //Stop Audio Recording
                myAudioRecorder.stop();
                myAudioRecorder.release();
                myAudioRecorder = null;
            }
        }
    }
    //Display counter for button presses
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        switch (keyCode) {
            case KeyEvent.KEYCODE_VOLUME_UP:
                TextView textView = (TextView) findViewById(R.id.buttonStatus_debug);
                textView.setText(Integer.toString(buttonCounter));
                isStressful = true;
                buttonCounter+=1;
        }
        return super.onKeyDown(keyCode, event);
    }
    @Override
    public boolean onKeyUp(int keyCode, KeyEvent event) {
        switch (keyCode) {
            case KeyEvent.KEYCODE_VOLUME_UP:
                TextView textView = (TextView) findViewById(R.id.buttonStatus_debug);
                textView.setText(Integer.toString(buttonCounter));
                isStressful = false;
        }
        return super.onKeyDown(keyCode, event);
    }
}
