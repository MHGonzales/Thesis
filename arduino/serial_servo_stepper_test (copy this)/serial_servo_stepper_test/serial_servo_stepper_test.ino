#include <VarSpeedServo.h>

VarSpeedServo servo_1,servo_2,grip;

#define MOTOR_STEPS 200
#define RPM 30

#define DIR 3
#define STEP 4
#define SLEEP 5


#include "DRV8825.h"
#define MODE0 8
#define MODE1 7
#define MODE2 6
DRV8825 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, MODE0, MODE1, MODE2);

float set_j1,set_j2,set_j3,set_j4 = 90;
float new_step,old_step=0;
int pos_1= 90,pos_2= 90,pos_3 = 90;

void setup() {
  // put your setup code here, to run once:
  servo_1.attach(11,544,2520);
  servo_2.attach(10,544,2500);
  grip.attach(9,544,2520);

  Serial.begin(9600); // start serial monitor
  //Wire.begin();

  servo_1.write(90);
  servo_2.write(90);
  grip.write(pos_3); 

  stepper.begin(RPM);
  stepper.enable();
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
    set_j4 = strArr[3].toFloat();

    set_j2 = new_step - old_step;
    
    servo_1.slowmove(set_j1,13); 
    delay(15);
    servo_2.slowmove(set_j3,13);
    delay(15);
    grip.write(set_j4);
    stepper.rotate(set_j2); 

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
