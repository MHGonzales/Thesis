#include <VarSpeedServo.h>
#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
                                        
VarSpeedServo servo_1,servo_2,servo_3,grip;

 // servo controller (multiple can exist)
  // servo starting position
double set_j1,set_j2,set_j3 = 90;
double i_pitch,i_roll,i_yaw;
double e_1,e_2,e_3;
unsigned long timer,currentTime,previousTime;


double elapsedTime;
double lastError1,lastError2,lastError3;
double cumError1,cumError2,cumError3, rateError1,rateError2,rateError3;
double out1,out2,out3;

double kp = 2;
double ki = 5;
double kd = 1;

void setup() {

 

  servo_1.attach(9,500,2460);
  servo_2.attach(10,544,2400);
  servo_3.attach(6,500,2400); // start servo control
  Serial.begin(9600); // start serial monitor
  Wire.begin();

  servo_1.write(set_j1);
  servo_2.write(set_j2);
  servo_3.write(set_j3); 
  
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


   
    set_j1 = strArr[0].toFloat()+90;
    set_j2 = strArr[1].toFloat()+90;
    set_j3 = strArr[2].toFloat()+90;
    
    

    servo_1.slowmove(set_j1,12); 
      //delay(15);
    servo_2.slowmove(set_j2,12);
      //delay(15);
    servo_3.slowmove(set_j3,12);             // tell servo to go to position in variable 'j1'
    //delay(15);
    
    
  }
  mpu.update();
  i_pitch = mpu.getAngleX();
  i_roll = mpu.getAngleY();
  i_yaw = mpu.getAngleZ();
  if((millis()-timer)>100
  ){ // print data every 10ms
    Serial.print("pitch : ");
    Serial.print(i_pitch);
    Serial.print("\troll : ");
    Serial.print(i_roll);
    Serial.print("\tyaw : ");
    Serial.println(i_yaw);
    timer = millis();
  }
  
}
double comp_pid(float i_pitch,float i_roll,float i_yaw,float set_j1, float set_j2,float set_j3){
  currentTime = millis();

  elapsedTime = (double)(currentTime - previousTime);
  
  //Errors

  e_1 = set_j1 - i_yaw;
  e_2 = set_j2 - i_roll;
  e_3 = set_j3 - i_pitch;

  //Integral Errors
  cumError1 += e_1 *elapsedTime;
  cumError2 += e_2 * elapsedTime;
  cumError3 += e_3 * elapsedTime;


  //Derivative Errors
  rateError1 = (e_1-lastError1)/elapsedTime;
  rateError2 = (e_2-lastError2)/elapsedTime;
  rateError3 = (e_3-lastError3)/elapsedTime;

  //New output
  double out1 = kp*e_1 + ki*cumError1 + kd*rateError1;
  double out2  = kp*e_2 + ki*cumError2 + kd*rateError2;
  double out3  = kp*e_3 + ki*cumError3 + kd*rateError3;

  lastError1 = e_1;
  lastError2 = e_2;
  lastError3 = e_3;

  previousTime = currentTime;

}

double comp_newangle(){

}