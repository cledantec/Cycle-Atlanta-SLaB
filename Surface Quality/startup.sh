#! /bin/bash

cd ~/matrix-creator-malos/src/js_test/
python -m server.py &
sleep(5)
node test_imu_server & node test_humidity_server & test_pressure_server & test_uv_server && test_everloop_server


### Reference this file in ~.config/lxsession/LXDE-pi/autostart file as ###
### @bash ~/startup.sh ###