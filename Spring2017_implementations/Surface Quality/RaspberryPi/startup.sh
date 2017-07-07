#! /bin/bash

cd ~/matrix-creator-malos/src/js_test/
echo 'Starting server...'
python -m server.py &
sleep(5)
echo 'getting data from onboard sensors on Matrix...'
node test_imu_server & node test_humidity_server & node test_pressure_server & node test_uv_server & node test_everloop_server


### Reference this file in ~.config/lxsession/LXDE-pi/autostart file as ###
### @bash /home/pi/startup.sh ###