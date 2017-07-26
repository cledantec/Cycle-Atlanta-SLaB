System Oveview
========
As of July 26, 2017

## High-level Architecture
The sensing system consists of two parts: a *master unit* and *slave unit*.<br>
The master unit runs a Linux server (i.e., Raspbian Jessie) that provides RestAPIs and a socket application that deals with the serial communication with Arduino. <br>
The slave unit runs on an Arudino board and it sends out sensor data to the master unit following the commands from the master. 

## Master Unit 
#### Raspberry Pi + Matrix Creator + GPS
Matrix Creator is a collection of built-in sensors such as gyroscope, accelerometer and thermometer. This is attached to the Raspberry Pi through GPIO pins. Besides, Pi has four USB ports, one ethernet port, and two different power ports. A custom GPS device communicates with the Pi through a USB port. Another USB port is connected to the Arduino. Also, the flat power port is used to connect to the battery on the back side. Overall, two lines are going out to the sensor box from the master unit.

![](http://myeong.github.io/template.jpg)

Raspberry Pi runs "Raspbian Jessie Desktop" for its operating system. For saving the energy, 

## Slave Unit
#### Arduino + 1 Gas Sensor Board + 2 Lidars + 3 Sonars + 1 PM Sensor + Battery

## Communication


