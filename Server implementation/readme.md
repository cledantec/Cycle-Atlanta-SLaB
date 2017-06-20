# SLaB Server & Data store

This component runs the server on a RasPi that accepts data streams from the rear box (proximity and air quality) and the Matrix mounted on the handle-bars.

Installation 
============

Copy all files in the RaspberryPi directory to the home directory of the Raspberry Pi. Install dependencies for the Matrix and Flask (see install.sh):

```
sudo apt-get install python python3 python-pip nodejs
sudo pip install flask
curl https://raw.githubusercontent.com/matrix-io/matrix-creator-quickstart/master/install.sh | sh
```

* We will be using the MALOS abstracted layer on Matrix, here: https://matrix-io.github.io/matrix-documentation/MALOS/overview/ 
* Python Flask runs as the server, and accepts a JSON payload
* The server automatically time-stamps POSTed data and appends the sensor name based on what endpoint was contacted.

To run:

```
sudo python -m <path>/server.python
```

Server endpoints
----------------
| **Endpoint**  | **HTTP Method** | **Data** |
|---|---|---|
| /getstatus | GET | Returns LED status |
| /status | POST | Gets various sensor statuses |
| /proximity | POST | Gets proximity data |
| /inertial | POST | Gets inertial data |
| /humidity | POST | Gets humidity data |
| /uvindex | POST | Gets ultraviolet data |
| /prestempalt | POST | Gets pressure, temperature, altitude data |
| /gas | POST | Gets gas array data |
| /gps | POST | Gets GPS data |

Data store
----------
Data received by the server is stored in this format:
```{
 ‘sensor’: ‘sensor_name’,
 ‘timestamp’: ‘YYYY-MM-DD HH:MM:SS.ssssss’,
 ‘data’: {sensor_payload}
 }
 ```

Future work
-----------
* Send data to MongoDB instead of plain text file (better size and filtering)
* Write services to retrieve data based on filters


Command-line Autostart and Auto Triggering of Shell Scripts
---------
cd /etc/systemd/system/autologin@.service
Change line: ExecStart=-/sbin/agetty --autologin pi --noclear %I $TERM

Auto Triggering Shell Scripts
- Comment out the line in “LXDE-pi” since it works for GUI mode ```sudo nano ~/.config/lxsession/LXDE/autostart```
- In “/etc/rc.local”, put the line ```/home/pi/startup.sh @```