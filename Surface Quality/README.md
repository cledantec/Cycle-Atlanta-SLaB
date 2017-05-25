# Surface Quality Sensor readme

Code for running surface and environmental sensors from the Matrix.

Installation
============
Copy all files in the RaspberryPi directory to the home directory of the Raspberry Pi. Follow installation instruction of the Server—this runs on the same mdule.

To run:

```
node test_imu_server & node test_humidity_server & node test_pressure_server & node test_uv_server & node test_everloop_server
```

For auto start, edit thee ~.config/lxsession/LXDE-pi/autostart file to include: 

```
@bash /home/pi/startup.sh
```

Note: startup.sh also starts the Server.