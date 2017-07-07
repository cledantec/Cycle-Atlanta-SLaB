cd /home/pi/matrix-creator-malos/src/js_test
python3 server_opt.py &
sleep 5
node test_imu_server & node test_humidity_server & node test_uv_server & node test_pressure_server & python arduino_receiver.py & node test_everloop_server
