#include "Wire.h"       
#include "I2Cdev.h"     
#include "MPU6050.h"    

MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;

float RateRoll, RatePitch, RateYaw;
float RCRoll, RCPitch, RCYaw;
int RCNum;

void gyro_signals(void){
  Wire.beginTransmission(0x68);
  Wire.write(0x1A); //1A == LPF
  Wire.write(0x05); //DLPF 5 = 10Hz
  Wire.endTransmission();

  Wire.beginTransmission(0x68);
  Wire.write(0x1B); //1B == Sensitivity scale factor
  Wire.write(0x8);  //binary ng fs_sel = 1  with 66.5 rate
  Wire.endTransmission();

  Wire.beginTransmission(0x68);
  Wire.write(0x43); //gyro measurements
  Wire.endTransmission();

  Wire.requestFrom(0x68,6); 

  int16_t GyroX = Wire.read() << 8 | Wire.read(); 
  int16_t GyroY = Wire.read() << 8 | Wire.read();
  int16_t GyroZ = Wire.read() << 8 | Wire.read();

  RateRoll = (float)GyroX/65.5;
  RatePitch = (float)GyroY/65.5;
  RateYaw = (float)GyroZ/65.5;
}

struct MyData {
  float X;
  float Y;
  float Z;
};

MyData data;

void setup()
{
  Serial.begin(57600);

  Wire.setClock(4000000);
  Wire.begin();
  delay(100);

  Wire.beginTransmission(0x68);
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission();
  
  for(RCNum=0;RCNum<2000;RCNum++){
    gyro_signals();
    RCRoll+=RateRoll;
    RCPitch+=RatePitch;
    RCYaw+=RateYaw;
    delay(1);
  }

  RCRoll/=2000;
  RCPitch/=2000;
  RCYaw/=2000;
}

void loop()
{
  gyro_signals();
  RateRoll-=RCRoll;
  RatePitch-=RCPitch;
  RateYaw-=RCYaw;
  Serial.print("Roll rate =");
  Serial.print(RateRoll);
  delay(50);
  Serial.print("  Pitch rate =");
  Serial.print(RatePitch);
  delay(50);
  Serial.print("  Yaw rate =");
  Serial.println(RateYaw);
  delay(50);

  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  data.X = map(ax, -17000, 17000, 0, 255 ); // X axis data
  data.Y = map(ay, -17000, 17000, 0, 255); 
  data.Z = map(az, -17000, 17000, 0, 255);  // Y axis data
  delay(50);
  Serial.print("Axis X = ");
  Serial.print(data.X);
  Serial.print("  Axis Y = ");
  Serial.print(data.Y);
  Serial.print("    Axis Z  = ");
  Serial.println(data.Z);
  
}
