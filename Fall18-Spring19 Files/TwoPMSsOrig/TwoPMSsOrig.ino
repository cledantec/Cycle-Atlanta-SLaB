// On Leonardo/Micro or others with hardware serial, use those!
// uncomment this line:
// #define pmsSerial Serial1
 
// For UNO and others without hardware serial, we must use software serial...
// pin #2 is IN from sensor (TX pin on sensor), leave pin #3 disconnected
// comment these two lines if using hardware serial
#include <SoftwareSerial.h>
SoftwareSerial one(10, 3);
SoftwareSerial two(11,4);
uint16_t curr = 0;
//change to true if you would like to see adafruit's original output
boolean debug = false;
 
void setup() {

  // our debugging output
  Serial.begin(115200);
  //TAKE OUT BEFORE IMPLEMENTING
  while (!Serial) {
    ;
  }
  
  //TAKE OUT ABOVE BEFORE IMPLEMENTING
  // sensor baud rate is 9600
  one.begin(9600);
  two.begin(9600);

}
 
struct pms5003data {
  uint16_t framelen;
  uint16_t pm10_standard, pm25_standard, pm100_standard;
  uint16_t pm10_env, pm25_env, pm100_env;
  uint16_t particles_03um, particles_05um, particles_10um, particles_25um, particles_50um, particles_100um;
  uint16_t unused;
  uint16_t checksum;
};
 
struct pms5003data data;
struct pms5003data firstData;
    
void loop() {
  //Serial.println("Curr:");
  //Serial.print(curr);
  if (curr == 0){
    one.listen();
  }
  if (readPMSdata(&one)) {
    if (debug) {
        Serial.println();
        Serial.println("---------------------------------------");
        Serial.println("------------PMS@Pin10------------------");
        Serial.println("Concentration Units (standard)");
        Serial.print("PM 1.0: "); Serial.print(data.pm10_standard);
        Serial.print("\t\tPM 2.5: "); Serial.print(data.pm25_standard);
        Serial.print("\t\tPM 10: "); Serial.println(data.pm100_standard);
        Serial.println("---------------------------------------");
        Serial.println("Concentration Units (environmental)");
        Serial.print("PM 1.0: "); Serial.print(data.pm10_env);
        Serial.print("\t\tPM 2.5: "); Serial.print(data.pm25_env);
        Serial.print("\t\tPM 10: "); Serial.println(data.pm100_env);
        Serial.println("---------------------------------------");
        Serial.print("Particles > 0.3um / 0.1L air:"); Serial.println(data.particles_03um);
        Serial.print("Particles > 0.5um / 0.1L air:"); Serial.println(data.particles_05um);
        Serial.print("Particles > 1.0um / 0.1L air:"); Serial.println(data.particles_10um);
        Serial.print("Particles > 2.5um / 0.1L air:"); Serial.println(data.particles_25um);
        Serial.print("Particles > 5.0um / 0.1L air:"); Serial.println(data.particles_50um);
        Serial.print("Particles > 50 um / 0.1L air:"); Serial.println(data.particles_100um);
        Serial.println("---------------------------------------");
     }
     curr = 1;
     firstData = data;
  }
  if (curr == 1) {
    two.listen();
  }
  if (readPMSdata(&two)) {
      // reading data was successful!
      if (debug) {
        Serial.println();
        Serial.println("---------------------------------------");
        Serial.println("------------PMS@Pin11------------------");
        Serial.println("Concentration Units (standard)");
        Serial.print("PM 1.0: "); Serial.print(data.pm10_standard);
        Serial.print("\t\tPM 2.5: "); Serial.print(data.pm25_standard);
        Serial.print("\t\tPM 10: "); Serial.println(data.pm100_standard);
        Serial.println("---------------------------------------");
        Serial.println("Concentration Units (environmental)");
        Serial.print("PM 1.0: "); Serial.print(data.pm10_env);
        Serial.print("\t\tPM 2.5: "); Serial.print(data.pm25_env);
        Serial.print("\t\tPM 10: "); Serial.println(data.pm100_env);
        Serial.println("---------------------------------------");
        Serial.print("Particles > 0.3um / 0.1L air:"); Serial.println(data.particles_03um);
        Serial.print("Particles > 0.5um / 0.1L air:"); Serial.println(data.particles_05um);
        Serial.print("Particles > 1.0um / 0.1L air:"); Serial.println(data.particles_10um);
        Serial.print("Particles > 2.5um / 0.1L air:"); Serial.println(data.particles_25um);
        Serial.print("Particles > 5.0um / 0.1L air:"); Serial.println(data.particles_50um);
        Serial.print("Particles > 50 um / 0.1L air:"); Serial.println(data.particles_100um);
        Serial.println("---------------------------------------");
      }
      curr = 0;
      printJSON();
  }
}

void printJSON(){

  Serial.print("{'PMS1' : {'pm10_standard' : '"); Serial.print(firstData.pm10_standard); Serial.println("',");
  Serial.print(" 'pm25_standard' : '"); Serial.print(firstData.pm25_standard); Serial.println("',");
  Serial.print(" 'pm100_standard' : '"); Serial.print(firstData.pm100_standard); Serial.println("',");

  Serial.print(" 'pm10_env' : '"); Serial.print(firstData.pm10_env); Serial.println("',");
  Serial.print(" 'pm25_env' : '"); Serial.print(firstData.pm25_env); Serial.println("',");
  Serial.print(" 'pm100_env' : '"); Serial.print(firstData.pm100_env); Serial.println("',");

  Serial.print(" 'particles_03um' : '"); Serial.print(firstData.particles_03um); Serial.println("',");
  Serial.print(" 'particles_05um' : '"); Serial.print(firstData.particles_05um); Serial.println("',");
  Serial.print(" 'particles_10um' : '"); Serial.print(firstData.particles_10um); Serial.println("',");
  Serial.print(" 'particles_25um' : '"); Serial.print(firstData.particles_25um); Serial.println("',");
  Serial.print(" 'particles_50um' : '"); Serial.print(firstData.particles_50um); Serial.println("',");
  Serial.print(" 'particles_100um' : '"); Serial.print(firstData.particles_100um); Serial.println("'},");
      
  Serial.print("'PMS2' : {'pm10_standard' : '"); Serial.print(data.pm10_standard); Serial.println("',");
  Serial.print(" 'pm25_standard' : '"); Serial.print(data.pm25_standard); Serial.println("',");
  Serial.print(" 'pm100_standard' : '"); Serial.print(data.pm100_standard); Serial.println("',");

  Serial.print(" 'pm10_env' : '"); Serial.print(data.pm10_env); Serial.println("',");
  Serial.print(" 'pm25_env' : '"); Serial.print(data.pm25_env); Serial.println("',");
  Serial.print(" 'pm100_env' : '"); Serial.print(data.pm100_env); Serial.println("',");

  Serial.print(" 'particles_03um' : '"); Serial.print(data.particles_03um); Serial.println("',");
  Serial.print(" 'particles_05um' : '"); Serial.print(data.particles_05um); Serial.println("',");
  Serial.print(" 'particles_10um' : '"); Serial.print(data.particles_10um); Serial.println("',");
  Serial.print(" 'particles_25um' : '"); Serial.print(data.particles_25um); Serial.println("',");
  Serial.print(" 'particles_50um' : '"); Serial.print(data.particles_50um); Serial.println("',");
  Serial.print(" 'particles_100um' : '"); Serial.print(data.particles_100um); Serial.println("'}}");
  Serial.println("");
}
 
boolean readPMSdata(Stream *s) {
  if (! s->available()) {
    //Serial.println("but false.");
    return false;
  }
  
  // Read a byte at a time until we get to the special '0x42' start-byte
  if (s->peek() != 0x42) {
    s->read();
    return false;
  }
 
  // Now read all 32 bytes
  if (s->available() < 32) {
    return false;
  }
    
  uint8_t buffer[32];    
  uint16_t sum = 0;
  s->readBytes(buffer, 32);
 
  // get checksum ready
  for (uint8_t i=0; i<30; i++) {
    sum += buffer[i];
  }
 
  /* debugging
  for (uint8_t i=2; i<32; i++) {
    Serial.print("0x"); Serial.print(buffer[i], HEX); Serial.print(", ");
  }
  Serial.println();
  */
  
  // The data comes in endian'd, this solves it so it works on all platforms
  uint16_t buffer_u16[15];
  for (uint8_t i=0; i<15; i++) {
    buffer_u16[i] = buffer[2 + i*2 + 1];
    buffer_u16[i] += (buffer[2 + i*2] << 8);
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


