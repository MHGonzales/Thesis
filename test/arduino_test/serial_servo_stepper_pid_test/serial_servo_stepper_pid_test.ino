#include <VarSpeedServo.h>

VarSpeedServo servo_1,servo_2,servo_3,grip;

#define MOTOR_STEPS 200
#define RPM 30

#define DIR 3
#define STEP 4
#define SLEEP 9

#include "A4988.h"
#define MS1 5
#define MS2 6
#define MS3 7
A4988 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, MS1, MS2, MS3);

float set_j1,set_j2,set_j3 = 90;
float new_step,old_step=90;
int pos_1= 90,pos_2= 90,pos_3 = 90;

void setup() {
  // put your setup code here, to run once:
  servo_1.attach(9,544,2520);
  servo_2.attach(10,544,2500);
  servo_3.attach(11,544,2500);

  Serial.begin(9600); // start serial monitor
  //Wire.begin();

  servo_1.write(90);
  servo_2.write(90);
  servo_3.write(pos_3); 

  stepper.begin(RPM);
  //stepper.enable();
  stepper.setMicrostep(1);

  delay(5000);
  Serial.println("Positioned at Home Position");
}

void loop() {
  // put your main code here, to run repeatedly:
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
    set_j1 = strArr[0].toFloat();
    set_j2 = strArr[1].toFloat();
    new_step = strArr[2].toFloat();

    set_j3 = new_step - old_step;
    
    servo_1.slowmove(set_j1,13); 
    delay(15);
    servo_2.slowmove(set_j2,13);
    delay(15);
    stepper.rotate(set_j3); 

    old_step = new_step;
    
  }

 // Serial.print(set_j1);
  //Serial.print(set_j2);
  //Serial.println(set_j3);
 // servo_1.write(set_j1); 
  //delay(15);
  //servo_2.write(set_j2);
 // delay(15);
  //stepper.rotate(set_j3-old_step); 

  //old_step = set_j3;
}

