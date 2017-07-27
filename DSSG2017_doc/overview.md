System Oveview
========
As of July 26, 2017

## High-level Architecture
The sensing system consists of two parts: a *master unit* and *slave unit*.<br>
This architecture is a result of reverse engineering and optimization based on the initial prototypes from the LMC6650 class project. 
The master unit runs a Linux server (i.e., Raspbian Jessie) that provides RestAPIs and a socket application that deals with the serial communication with Arduino. <br>
The slave unit runs on an Arudino board and it sends out sensor data to the master unit following the commands from the master. 

## Master Unit 
#### Raspberry Pi + Matrix Creator + GPS
Matrix Creator is a collection of built-in sensors such as gyroscope, accelerometer and thermometer. This is attached to the Raspberry Pi through GPIO pins. Besides, Pi has four USB ports, one ethernet port, and two different power ports. A custom GPS device communicates with the Pi through a USB port. Another USB port is connected to the Arduino. Also, the flat power port (USB-C type) is used to connect to the battery on the back side. Overall, two lines are going out from the master unit to the sensor box.

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/matrix.jpg?raw=true" style="width: 700px;"/>

Raspberry Pi runs "Raspbian Jessie Desktop" for its operating system. For saving the energy consumption, the command-line mode was used instead of the Windows mode. Since some OS-level configurations such as auto-start and auto-login change depending on the booting mode, it is required to configure at the right places for each feature. Also, collected data from the Matrix, GPS, and the Arduino board are stored in the "data" folder in the Linux system. The details about the software configurations and folder structures are presented in the [Software Systems](software.md) document. 

Also, to minimize the effect of physical shocks and vibrations on the Pi operations, we added some protection mechanicsms. These physical designs are explained in the [Case Design](cases.md) part. 

Finally, the custom GPS design is presented at the [Hardware Systems](hardware.md) document. 

## Slave Unit
#### Arduino + a Gas Sensor Board + two Lidars + three Sonars + a PM Sensor + a Battery
Arduino has a type-B USB port, a power port, and mutiple pins for GPIOs and Digital inputs. Since many sensors had to be attached to a signle Arduino board, we made use of all the pins available for different connections. For example, the type-B USB port was used only for supplying power, while actual serial communications were implemented through making use of serial pins. The original power jack was not used since it required a higher voltage as input that was not available from our battery. The details about sensor connections will be discussed in the Hardware Systems](hardware.md) document. Since there is no operating systems for Arduino (but only a thin layer of firmware), there is no starting/stopping mechanism in the codee, but it starts working as power is on.

<img src="https://github.com/cledantec/Cycle-Atlanta-SLaB/blob/master/images/sensorbox.jpg?raw=true" style="width: 500px;"/>


## Communications
The master unit and slave unit communicate through a USB-based serial cable using a basic protocol. The master unit sends out commands to the slave unit regularly depending on the behavior of the slave. The slave unit either sends a line of sensory data to the master unit or resets itself. The details are presented in the [Software Systems](software.md) document. 

****
#### NEXT PAGE: [Hardware Systems](hardware.md)
