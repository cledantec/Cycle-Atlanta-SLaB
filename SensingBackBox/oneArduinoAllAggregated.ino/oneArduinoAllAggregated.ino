//SDS011 Nova PM sensor 

#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <stdio.h>
#include <LIDARLite.h>
LIDARLite myLidarLite;
#include <SDS011.h> //for Nova PM Sensor
SDS011 my_sds;

//init for Lidar sensors. Reassigning memory addresses.
int sensorPins[] = {2,4}; // Array of pins connected to the sensor Power Enable lines
unsigned char addresses[] = {0x66,0x68};
long dLidar01;
long dLidar02;

//for Sonar init
const int anPin0 = 0;
const int anPin1 = 1;
const int anPin2 = 2;
int triggerPin1 = 13;
long distance0, distance1, distance2;

//for Gases sensor init
Adafruit_ADS1015 ads;    // Construct an ads1015 at the default address: 0x48
int Vx[4];
float Ix[4];
int values[4];

//init for Nova PM sensor
float p10,p25;
int error;

void setup() {
  Wire.begin();       //join i2c bus
  my_sds.begin(10, 11);   //start Nova PM sensor with digital pins 10 and 11
  Serial.begin(9600); //start serial for output
  ads.begin();
  ads.setGain(GAIN_ONE);
  myLidarLite.begin();
  myLidarLite.changeAddressMultiPwrEn(2,sensorPins,addresses);
  pinMode(triggerPin1, OUTPUT);
}


//LIDAR SENSORS
void lidar_distance(){
  dLidar01 = myLidarLite.distance(true,true,0x66);
  dLidar02  = myLidarLite.distance(true,true,0x68);
}

//SONAR SENSORS
void start_sensor(){
  digitalWrite(triggerPin1,HIGH);
  delay(1);
  digitalWrite(triggerPin1,LOW);
}

void read_sensors(){
  /*
  Scale factor is (Vcc/512) per inch. A 5V supply yields ~9.8mV/in
  Arduino analog pin goes from 0 to 1024, so the value has to be divided by 2 to get the actual inches
  */
  distance0 = analogRead(anPin0)/2;
  distance1 = analogRead(anPin1)/2;
  distance2 = analogRead(anPin2)/2;
}

//GASES SENSORS
void read_gasarray() {
  for (int i=0; i<4; i++) {
    values[i] = ads.readADC_SingleEnded(i);  
  }
  //initialising base voltage and current values for each gas
  Vx[0] =818;
  Vx[1] =823;
  Vx[2] =812;
  Vx[3] =810;
  Ix[0] =0.00000000475;
  Ix[1] =0.000000025;
  Ix[2] =0.000000032;
  Ix[3] =0.0000000040;
  
  //adjusting sensor values
  for (int i=0; i<4; i++){
    values[i] = (values[i] - Vx[i])/(500000*Ix[i]);
  }
}

//PRINTING
void print_lidar(){
  Serial.print("Lidar1:  ");
  Serial.println(dLidar01);
  Serial.print("Lidar2:  ");
  Serial.println(dLidar02);
  delay(1000);
}

void print_sonar(){
  Serial.print("SONAR 0: ");
  Serial.println(distance0*2.54);
  Serial.print("SONAR 1:  ");
  Serial.println(distance1*2.54);
  Serial.print("SONAR 2:  ");
  Serial.println(distance2*2.54);
}

void print_gas(){
  String gas[4];
  gas[0] = "CO:  ";
  gas[1] = "SO:  ";
  gas[2] = "O:  ";
  gas[3] = "NO:  ";
  for(int i=0; i<4; i++){
    Serial.println(gas[i] + values[i]);
  }
  Serial.println(); 
}

void print_pm() {
  error = my_sds.read(&p25,&p10);
  if (! error) {
    Serial.println("P2.5: "+String(p25));
    Serial.println("P10:  "+String(p10));
  }
  delay(100);
}

//MAIN LOOP
//counter for distinguishing 1 second rate for lidar and sonar sensors
//and 5 second rate for gases sensors
int c=1;
void loop(){
  if (c!=5){
    lidar_distance();
    print_lidar();
    start_sensor();
    read_sensors();
    print_sonar();
    Serial.println("END");
    Serial.println();
    c++;
  }    
  else{
    lidar_distance();
    print_lidar();
    start_sensor();
    read_sensors();
    print_sonar();
    read_gasarray();
    print_gas();
    print_pm();
    Serial.println("END");
    Serial.println();
    c=1;       
  }
}
