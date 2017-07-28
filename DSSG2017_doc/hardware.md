Hardware Systems
=======
### <span style="color:grey">Table of Contents</span>

1. [Securing Raspberry Pi and Matrix](#matrix)
2. [GPS](#gps)
3. [Pi-to-Arduino Communication](#commo)
4. [Arduino and Sensor Connections](#arduino)
5. [Gas Sensors](#gas)
6. [PM Sensor](#pm)
7. [Lidars](#lidars)
8. [Sonars](#sonars)


## Securing Rapspberry Pi and Matrix

## GPS Fabrication

Our GPS system consists of a GTPA010 GPS, a CP2102 USB, and a small piece of pcv board. As you can appreciate in the picture below, we connected the gps to the CP2102 USB by using the pcv board as intermediate. It is easy to make mistakes when connecting the pins and it is so hard to unsold them specailly when you have already finished it, so put attention to the connection during all the time of soldering. 


![gps](https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/gps2.jpg?raw=true)

###The **connection of pins** is the folowing:

![alt gps structure](https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/gpsStructure4.png?raw=true)

The code uses the default settings of the GPS and returns the following data: **course**, **longitud**, **latitude**, **speed**, **day**, and, **utc_time**

    

## Pi-to-Arduino Communication

## Arduino and Sensor Connections


## Gas Sensors
We made use of the following gas sensor custom desing from spring 2017 team.

![gps](https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/gasSensor.png?raw=true)

We engineered seven of them and these are our observations from try-and-error testing. 

1. The holes for resistors in the gas sensor boards are small and different sizes, it was so hard to push the lead of the resistors down, and for those resistors which did not fit into the holes we replace them with smaller resistors different in voltage. For instance, we replaced the 560 K Ohms resitor with 470 K Ohms resitor. This replacement worked fine. 

2. Gas sensor board's behaviour are not consistent. 

Detailed information about each of the seven sensor boards is found [here](https://docs.google.com/spreadsheets/d/18mLQVb0HjoA-88Tq4y8rYqyIrmJ9yjPXizwVc3SuRZM/edit?usp=sharing).
					













## PM Sensors

## Lidars

## Sonars
