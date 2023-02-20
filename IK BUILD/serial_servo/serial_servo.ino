#include <VarSpeedServo.h>
#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
                                        
VarSpeedServo servo_1,servo_2,servo_3,grip;

 // servo controller (multiple can exist)
  // servo starting position
int j1,j2,j3 = 0;
int pos_1 = 90;
int pos_2 = 90;
int pos_3 = 85;
unsigned long timer = 0;

void setup() {

 

  servo_1.attach(9,500,2460);
  servo_2.attach(10,544,2400);
  servo_3.attach(6,500,2400); // start servo control
  Serial.begin(9600); // start serial monitor
  Wire.begin();

  servo_1.write(pos_1);
  servo_2.write(pos_2);
  servo_3.write(pos_3); 
  
  // move servo to 0 degrees
  delay(5000);
  Serial.println("Positioned at Home Position");

  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ }
  
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  // mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");

 
}



void loop() {
  
  
  while (Serial.available())
  {
    //unsigned long progress = millis() - moveStartTime;
    String rxString = "";
    String strArr[3];
  //Keep looping until there is something in the buffer.
    while (Serial.available()) {
      //Delay to allow byte to arrive in input buffer.
      delay(2);
      //Read a single character from the buffer.
      char ch = Serial.read();
      //Append that single character to a string.
      rxString+= ch;
    }
    int stringStart = 0;
    int arrayIndex = 0;
    for (int i=0; i < rxString.length(); i++){
      //Get character and check if it's our "special" character.
      if(rxString.charAt(i) == ','){
        //Clear previous values from array.
        strArr[arrayIndex] = "";
        //Save substring into array.
        strArr[arrayIndex] = rxString.substring(stringStart, i);
        //Set new string starting point.
        stringStart = (i+1);
        arrayIndex++;
      }
    }


   
    j1 = strArr[0].toInt();
    j2 = strArr[1].toInt();
    j3 = strArr[2].toInt();
    
    

    servo_1.slowmove(j1+90,12); 
      //delay(15);
    servo_2.slowmove(j2+90,12);
      //delay(15);
    servo_3.slowmove(j3+90,12);             // tell servo to go to position in variable 'j1'
    //delay(15);
    
    
  }
  mpu.update();
  if((millis()-timer)>10){ // print data every 10ms
    Serial.print("X : ");
    Serial.print(mpu.getAngleX());
    Serial.print("\tY : ");
    Serial.print(mpu.getAngleY());
    Serial.print("\tZ : ");
    Serial.println(mpu.getAngleZ());
    timer = millis();
  }
  
}
