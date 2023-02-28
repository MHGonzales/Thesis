
#include <Servo.h>

Servo servo;
int pos=100;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo.attach(10,544,2500);//default min:544 max: 2400 //yaw 544,2520 //pitch 544, 2500
  servo.write(pos);
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  while(Serial.available()){
    pos = Serial.parseInt();
    Serial.println(pos);
    servo.write(pos);
    break;
  }*/
  
  
}
