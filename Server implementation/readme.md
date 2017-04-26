# Instructions on setting up the server and Matrix

* We will be using the MALOS abstracted layer on Matrix, here: https://matrix-io.github.io/matrix-documentation/MALOS/overview/ 
* Python Flask runs as the server, and accepts a JSON payload
* The server automatically time-stamps POSTed data and appends the sensor name based on what endpoint was contacted.

# Server endpoints
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

# Data store
Data received by the server is stored in this format:
```{
 ‘sensor’: ‘sensor_name’,
 ‘timestamp’: ‘YYYY-MM-DD HH:MM:SS.ssssss’,
 ‘data’: {sensor_payload}
 }
 ```

# Future work
* Send data to MongoDB instead of plain text file (better size and filtering)
* Write services to retrieve data based on filters
* Conditionally write data based on GPIO wire
* Only write data if it is important (for example, the surface mic or accelerometer exceeds a certain threshold. 