
/* This code reads Analog input from 2 Chained ultrasound sensors*/

const int anPin1 = 0;
const int anPin2 = 1;
int triggerPin1 = 13;
long distance1, distance2;

void setup() 
{
 Serial.begin(9600);  // sets the serial port to 9600
 pinMode(triggerPin1, OUTPUT);
}

void start_sensor()
{
 digitalWrite(triggerPin1,HIGH);
 delay(1);
 digitalWrite(triggerPin1,LOW);
}

void read_sensors()
{
 /*Scale factor is (Vcc/512) per inch. A 5V supply yields ~9.8mV/in
 Arduino analog pin goes from 0 to 1024, so the value has to be divided by 2 to get the actual inches*/
 distance1 = analogRead(anPin1)/2;
 distance2 = analogRead(anPin2)/2;
}

void print_all()
{
 Serial.print(distance1*2.54);
 Serial.print(" ");
 Serial.println(distance2*2.54);
}

void loop() 
{
 start_sensor();
 read_sensors();
 print_all();
 delay(100); //This is the equivant of the amount of sensors times 50.  If you changed this to 5 sensors the delay would be 250.
}


