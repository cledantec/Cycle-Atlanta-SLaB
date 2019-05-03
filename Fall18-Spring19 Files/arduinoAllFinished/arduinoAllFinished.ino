//Includes code from: https://learn.adafruit.com/pm25-air-quality-sensor/arduino-code
//Upload to SLAB box arduinos to take in data from sensors and print
//in a format understandable to the pi

#include <NeoSWSerial.h>
#include <Wire.h>
#include <Adafruit_ADS1015.h>
#include <stdio.h>
#include <LIDARLite.h>


//PMS sensor 1 is at pin 10 and PMS sensor 2 is at pin 11
LIDARLite myLidarLite;
NeoSWSerial one(10, 7);
NeoSWSerial two(11,8);
uint16_t curr = 0;
boolean JSONready = false;

//init for Lidar sensors. Assigning memory addresses.
int sensorPins[] = {2, 4}; // Array of pins connected to the sensor Power Enable lines
unsigned char addresses[] = {0x66, 0x68};

//for Sonar init
const int anPin1 = 0;
const int anPin2 = 1;
const int anPin3 = 2;
const int triggerPin1 = 13;

//for Gases sensor init
// ADS address needs to be set appropriately based on the gas sensor number (among 0x48, 0x49, 0x4A, 0x4B)
Adafruit_ADS1015 ads;    

// PM
float p10, p25;
int error;

// Reset Pin
int resetPin = 12;

void setup() {
  
  digitalWrite(resetPin, HIGH);
  delay(200);
  pinMode(resetPin, OUTPUT);     
  Wire.begin();       //join i2c bus
  //Serial.begin(9600, SERIAL_7E1); //start serial for output
  Serial.begin(9600, SERIAL_8N1);
  ads.begin();
  //begin the two PMS sensors
  one.begin(9600);
  two.begin(9600);
//  ads.setGain(GAIN_ONE);
  myLidarLite.begin();
  myLidarLite.changeAddressMultiPwrEn(2, sensorPins, addresses);
  pinMode(triggerPin1, OUTPUT); 
}

//creates struct to put PMS data in
struct pms5003data {
  uint16_t framelen;
  uint16_t pm10_standard, pm25_standard, pm100_standard;
  uint16_t pm10_env, pm25_env, pm100_env;
  uint16_t particles_03um, particles_05um, particles_10um, particles_25um, particles_50um, particles_100um;
  uint16_t unused;
  uint16_t checksum;
};

//firstData holds data from sensor 1 until 2 is ready
struct pms5003data data;
struct pms5003data firstData;

//SONAR SENSORS
void start_sensor() {
  digitalWrite(triggerPin1, HIGH);
  delay(1);
  digitalWrite(triggerPin1, LOW);
}

//GASES SENSORS
float *get_gas_values() {
  static float values[4];
  int Vx[4];
  float Ix[4];
  
  //initialising base voltage and current values for each gas
  Vx[0] = 818;
  Vx[1] = 823;
  Vx[2] = 812;
  Vx[3] = 810;
  Ix[0] = 0.00000000475;
  Ix[1] = 0.000000025;
  Ix[2] = 0.000000032;
  Ix[3] = 0.0000000040;

  //adjusting sensor values
  for (int i = 0; i < 4; i++) {
    //values[i] = (ads.readADC_SingleEnded(i) - Vx[i]) / (500000 * Ix[i]);
    values[i] = ads.readADC_SingleEnded(i);
    delay(10);
  }
  return values;
}

void print_gas() {
  String gas[4];
  gas[0] = "CO";
  gas[1] = "SO";
  gas[2] = "O3";
  gas[3] = "NO";
  float *v = get_gas_values();
  
  for (int i = 0; i < 4; i++) {
    Serial.print(gas[i] + " ");
    Serial.print(v[i]);
    Serial.print(" ");
  }
}

//LIDAR SENSORS
float* get_lidar_distance() {
  static float lidars[2];
  lidars[0] = myLidarLite.distance(true, true, 0x66);
  lidars[1]  = myLidarLite.distance(true, true, 0x68);
  return lidars;
}

void print_lidar() {
  float *lidars = get_lidar_distance();
  Serial.print("Lidar1 ");
  Serial.print(lidars[0]);
  Serial.print(" ");
  Serial.print("Lidar2 ");
  Serial.print(lidars[1]);
  Serial.print(" ");
}


float *get_sonar_values() {
  /*
    Scale factor is (Vcc/512) per inch. A 5V supply yields ~9.8mV/in
    Arduino analog pin goes from 0 to 1024, so the value has to be divided by 2 to get the actual inches
  */
  static float distance[3];
  distance[0] = analogRead(anPin1) / 2;
  distance[1] = analogRead(anPin2) / 2;
  distance[2] = analogRead(anPin3) / 2;
  
  return distance;
}

void print_sonar() {
  float *dists = get_sonar_values();
  Serial.print("SONAR1 ");
  Serial.print(dists[0] * 2.54);
  Serial.print(" SONAR2 ");
  Serial.print(dists[1] * 2.54);
  Serial.print(" SONAR3 ");
  Serial.print(dists[2] * 2.54);
  Serial.print(" ");
}

//prints the PM data from both PM sensors
void printJSON(){
  JSONready = false;
  Serial.print("PMS1 {pm10_standard:"); Serial.print(firstData.pm10_standard); Serial.print(",");
  Serial.print("pm25_standard:"); Serial.print(firstData.pm25_standard); Serial.print(",");
  Serial.print("pm100_standard:"); Serial.print(firstData.pm100_standard); Serial.print(",");

  Serial.print("pm10_env:"); Serial.print(firstData.pm10_env); Serial.print(",");
  Serial.print("pm25_env:"); Serial.print(firstData.pm25_env); Serial.print(",");
  Serial.print("pm100_env:"); Serial.print(firstData.pm100_env); Serial.print(",");

  Serial.print("particles_03um:"); Serial.print(firstData.particles_03um); Serial.print(",");
  Serial.print("particles_05um:"); Serial.print(firstData.particles_05um); Serial.print(",");
  Serial.print("particles_10um:"); Serial.print(firstData.particles_10um); Serial.print(",");
  Serial.print("particles_25um:"); Serial.print(firstData.particles_25um); Serial.print(",");
  Serial.print("particles_50um:"); Serial.print(firstData.particles_50um); Serial.print(",");
  Serial.print("particles_100um:"); Serial.print(firstData.particles_100um); Serial.print("} ");
      
  Serial.print("PMS2 {pm10_standard:"); Serial.print(data.pm10_standard); Serial.print(",");
  Serial.print("pm25_standard:"); Serial.print(data.pm25_standard); Serial.print(",");
  Serial.print("pm100_standard:"); Serial.print(data.pm100_standard); Serial.print(",");

  Serial.print("pm10_env:"); Serial.print(data.pm10_env); Serial.print(",");
  Serial.print("pm25_env:"); Serial.print(data.pm25_env); Serial.print(",");
  Serial.print("pm100_env:"); Serial.print(data.pm100_env); Serial.print(",");

  Serial.print("particles_03um:"); Serial.print(data.particles_03um); Serial.print(",");
  Serial.print("particles_05um:"); Serial.print(data.particles_05um); Serial.print(",");
  Serial.print("particles_10um:"); Serial.print(data.particles_10um); Serial.print(",");
  Serial.print("particles_25um:"); Serial.print(data.particles_25um); Serial.print(",");
  Serial.print("particles_50um:"); Serial.print(data.particles_50um); Serial.print(",");
  Serial.print("particles_100um:"); Serial.print(data.particles_100um); Serial.print("} ");
}

boolean readPMSdata(Stream *s) {
  if (! s->available()) {
    return false;
  }
  
  // Read a byte at a time until we get to the special '0x42' start-byte
  uint16_t first = s->read();
  if (first != 0x42) {
    return false;
  }
 
  // Now read all 32 bytes
  uint16_t avail = s->available();
  if (avail < 30) {
    return false;
  }
  
  uint8_t buffer[31];    
  uint16_t sum = 0;
  s->readBytes(buffer, 31);
  uint8_t bufferTwo[32];
  bufferTwo[0] = first;
  for (uint8_t i=0; i<31; i++) {
    bufferTwo[i+1]=buffer[i];
  }

  //get checksum ready
  for (uint8_t i=0; i<30; i++) {
    sum += bufferTwo[i];
  }
 
  // The data comes in endian'd, this solves it so it works on all platforms
  uint16_t buffer_u16[15];
  for (uint8_t i=0; i<15; i++) {
    buffer_u16[i] = bufferTwo[2 + i*2 + 1];
    buffer_u16[i] += (bufferTwo[2 + i*2] << 8);
  }
  
 
  // put it into a nice struct :)
  memcpy((void *)&data, (void *)buffer_u16, 30);
 
  if (sum != data.checksum) {
    Serial.println("Checksum failure");
    return false;
  }
  
  // success!
  
  return true;
}

int i = 1;

//MAIN LOOP
void loop() {
    int response = Serial.read();

    if (response == 102){ // "f" means fail
      Serial.println("Serial port reset...");
      digitalWrite(resetPin, LOW);
      delay(20);
      digitalWrite(resetPin, HIGH);
      delay(200);
    } else if (response == 103) { // "g" means good
      print_lidar();
      start_sensor();
      print_sonar();

      //PMS sensor code
      if (curr == 0){
        one.listen();
        delay(200);
      }
  //check if the first PM sensor has new data
  if (readPMSdata(&one)) {
     curr = 1;
     //copies sensor data to backup struct
     firstData = data;
  }
  if (curr == 1) {
    two.listen();
    delay(200); 
  }
  //check if the second PM sensor has new data
  if (readPMSdata(&two)) {
      curr = 0;
      JSONready = true;
  }
  
      if (i%5 == 0){
        print_gas();
        //if data from both PM sensors is present go ahead and print it
        if (JSONready) {
          printJSON();
        }
        i=1;
      }
      i++;
      Serial.println();
    } else {
      delay(200);
    }
    delay(20);
}
