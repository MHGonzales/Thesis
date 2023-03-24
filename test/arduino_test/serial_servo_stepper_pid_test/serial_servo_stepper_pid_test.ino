#include <VarSpeedServo.h>
#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

VarSpeedServo servo_1,servo_2,grip;

#define MOTOR_STEPS 200
#define RPM 30

#define DIR 2
#define STEP 3
#define SLEEP 4

#define DIR1 5
#define STEP1 6
#define SLEEP 4


#include "A4988.h"
#define MS1 7
#define MS2 8
#define MS3 9
A4988 stepper_roll(MOTOR_STEPS, DIR, STEP, SLEEP, MS1, MS2, MS3);
A4988 stepper_knob(MOTOR_STEPS, DIR1, STEP1, SLEEP, MS1, MS2, MS3);

float set_j1,set_j2,set_j3,set_j4 = 90;
float new_step,old_step,new_step2,old_step2;
int pos_1= 90,pos_2= 90,pos_3 = 90;

double i_pitch,i_roll,i_yaw;
double e_1,e_2,e_3;
unsigned long timer,currentTime,previousTime;


double elapsedTime;
double lastError1,lastError2,lastError3;
double cumError1,cumError2,cumError3, rateError1,rateError2,rateError3;
float out1,out2,out3=0;

double kp = .5;
double ki = 0.000000000001;
double kd = 100;

void setup() {
  // put your setup code here, to run once:
  servo_1.attach(11,544,2520);
  servo_2.attach(10,544,2500);
  //grip.attach(11,544,2500);

  Serial.begin(9600); // start serial monitor
  Wire.begin();

  servo_1.write(90);
  servo_2.write(90);
  grip.write(pos_3); 

  stepper_roll.begin(RPM);
  stepper_roll.enable();
  stepper_roll.setMicrostep(1);

  stepper_knob.begin(RPM);
  stepper_knob.enable();
  stepper_knob.setMicrostep(1);

  delay(1000);
  Serial.println("Positioned at Home Position");
  
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){
    Serial.print("MPU not connected!!!");
   }
  
  //Calculates MPU 6050 offsets
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  // mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available())
  {
    //unsigned long progress = millis() - moveStartTime;
    String rxString = "";
    String strArr[4];
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
     set_j1 = strArr[0].toFloat();
    new_step = strArr[1].toFloat();
    set_j3 = strArr[2].toFloat();
    new_step2  = strArr[3].toFloat();

    set_j2 = new_step - old_step;
    set_j4 = new_step2 - old_step2;
    
    servo_1.slowmove(set_j1,13); 
    servo_2.slowmove(set_j3,13);
    grip.write(set_j4);
    stepper_roll.rotate(set_j2); 
    stepper_knob.rotate(set_j4*2/3);

    old_step = new_step;
    old_step2 = new_step2;
    
  }
  mpu.update();
  i_pitch = mpu.getAngleX();
  i_roll = mpu.getAngleY();
  i_yaw = mpu.getAngleZ();
  Serial.print("Sensor Angle:");
  Serial.print(i_pitch);
 
  //Computes PID
  if(e_3 > 5){
    comp_pid( i_pitch, i_roll, i_yaw, set_j1,  set_j2, set_j3, &out1, &out2, &out3);
  }
 

  //Writes output from PID
  //servo_1.write(set_j1); 
      //delay(15);
  //stepper.rotate(out2);
      //delay(15);
  servo_2.write(set_j3+out3); 
  Serial.print(" Servo Angle Error:");
  Serial.println(out3);

 
}

double comp_pid(double i_pitch,double i_roll,double i_yaw,double set_j1, double set_j2,double set_j3,float *output1,float *output2,float *output3){
  currentTime = millis();

  elapsedTime = (double)(currentTime - previousTime);
  
  //Errors

  // e_1 = set_j1 - i_yaw;
  // e_2 = set_j2 - i_roll;
  e_3 = set_j3 - i_pitch;

  //Integral Errors
  // cumError1 += e_1 *elapsedTime;
  // cumError2 += e_2 * elapsedTime;
  cumError3 += e_3 * elapsedTime;


  //Derivative Errors
  // rateError1 = (e_1-lastError1)/elapsedTime;
  // rateError2 = (e_2-lastError2)/elapsedTime;
  rateError3 = (e_3-lastError3)/elapsedTime;

  //New call by reference output
  // *output1 = kp*e_1 + ki*cumError1 + kd*rateError1;
  // *output2  = kp*e_2 + ki*cumError2 + kd*rateError2;
  *output3  = kp*e_3 + ki*cumError3 + kd*rateError3;

  // Saves last error
  // lastError1 = e_1;
  // lastError2 = e_2;
  lastError3 = e_3;

  previousTime = currentTime;
  //saves previous time
}
