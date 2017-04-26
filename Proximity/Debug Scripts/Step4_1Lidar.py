#This code uses the I2C input to read value sent by a LIDAR Module

from lidar_lite import Lidar_Lite 
#lidar_lite library included with the instructable must be copied to the working folder for above step to work

lidar = Lidar_Lite()
connected = lidar.connect(1)

if connected < -1:
  print "Not Connected"

print lidar.getDistance()
