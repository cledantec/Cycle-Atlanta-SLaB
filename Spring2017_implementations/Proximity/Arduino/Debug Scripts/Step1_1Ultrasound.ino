/* This code reads the Analog Voltage output from theLV-MaxSonar sensor*/

//Sensor is connected to AN0 on the Arduino
const int anPin1 = 0;
long distance1;

void setup() {
Serial.begin(9600);
}

void read_sensors(){
/*
Scale factor is (Vcc/512) per inch. A 5V supply yields ~9.8mV/in
Arduino analog pin goes from 0 to 1024, so the value has to be divided by 2 to get the actual inches
*/
distance1 = analogRead(anPin1)/2;
}

void print_all(){
Serial.print(distance1*2.54);
Serial.println();
}

void loop() {
read_sensors();
print_all();
delay(100);
}
