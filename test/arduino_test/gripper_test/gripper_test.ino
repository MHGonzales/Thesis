#include <Servo.h>

Servo grip;

void setup() {
  // put your setup code here, to run once:
  grip.attach(11);
  delay(5000);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  grip.write(80);

  delay(1000);

  grip.write(90);

  delay(1000);

  grip.write(100);

  delay(1000);

  grip.write(90);

  delay(1000);
}
