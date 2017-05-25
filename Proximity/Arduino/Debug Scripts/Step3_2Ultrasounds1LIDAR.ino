/*
This code reads the Analog Voltage output from the LV-MaxSonar sensors and LIDAR */

//libraries necessary for LIDAR
#include <Wire.h>a
#include <LIDARLite.h>

LIDARLite myLidarLite;
//Each US sensor is connected to AN0 and AN1 on the Arduino
const int anPin1 = 0;
const int anPin2 = 1;
//The RX of US sensor 1 is connected to Pin 13 on the Arduino
int triggerPin1 = 13;
long distance1, distance2;

void setup() 
{
 Serial.begin(4800);
 pinMode(triggerPin1, OUTPUT);
 // Set configuration to default and I2C to 400 kHz
 myLidarLite.begin(0, true);
 myLidarLite.configure(0);
}

void start_sensor()
{
 digitalWrite(triggerPin1,HIGH);
 delay(1);
 digitalWrite(triggerPin1,LOW);
}
void read_sensors()
{
 /*
 Scale factor is (Vcc/512) per inch. A 5V supply yields ~9.8mV/in
 Arduino analog pin goes from 0 to 1024, so the value has to be divided by 2 to get the actual inches
 */
 distance1 = analogRead(anPin1)/2;
 distance2 = analogRead(anPin2)/2;
}

void print_all()
{
 Serial.print(distance1*2.54);
 Serial.print(“ “);
 Serial.print(distance2*2.54);
}

void loop() 
{
 start_sensor();
 read_sensors();
 print_all();
 long dLidar=myLidarLite.distance();
 Serial.print(“ “);
 Serial.println(dLidar);
 delay(100);
}
