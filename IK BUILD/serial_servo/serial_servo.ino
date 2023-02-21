#include <VarSpeedServo.h>
#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
                                        
VarSpeedServo servo_1,servo_2,servo_3,grip;

 // servo controller (multiple can exist)
  // servo starting position
double set_j1,set_j2,set_j3 = 0;
double pos_1,pos_2,pos_3 =90;
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

  servo_1.write(pos_1);
  servo_2.write(pos_2);
  servo_3.write(pos_3); 
  
  // move servo to 0 degrees
  delay(5000);
  Serial.println("Positioned at Home Position");

  //Initializes MPU 6050
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ }
  
  //Calculates MPU 6050 offsets
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  // mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");

 
}



void loop() {
  
  //Reads any serial input
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


   //stores servo motor setpoints
    set_j1 = strArr[0].toFloat()+90;
    set_j2 = strArr[1].toFloat()+90;
    set_j3 = strArr[2].toFloat()+90;
    
    
  }
  // Read and stores MPU 6050 angle and position values (still noisy)
  mpu.update();
  i_pitch = mpu.getAngleX();
  i_roll = mpu.getAngleY();
  i_yaw = mpu.getAngleZ();
 
  //Computes PID
  comp_pid( i_pitch, i_roll, i_yaw, set_j1,  set_j2, set_j3, &out1, &out2, &out3);

  //Writes output from PID
  servo_1.slowmove(out1,12); 
      //delay(15);
  servo_2.slowmove(out2,12);
      //delay(15);
   servo_3.slowmove(out3,12);  
  
}
//function to calculate PID
//Can change to PID Library in the future
double comp_pid(double i_pitch,double i_roll,double i_yaw,double set_j1, double set_j2,double set_j3,double *output1,double *output2,double *output3){
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

  //New call by reference output
  *output1 = kp*e_1 + ki*cumError1 + kd*rateError1;
  *output2  = kp*e_2 + ki*cumError2 + kd*rateError2;
  *output3  = kp*e_3 + ki*cumError3 + kd*rateError3;

  // Saves last error
  lastError1 = e_1;
  lastError2 = e_2;
  lastError3 = e_3;

  previousTime = currentTime;
  //saves previous time
}

