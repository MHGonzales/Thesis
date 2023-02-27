#include <Servo.h>

Servo grip;

void setup() {
  // put your setup code here, to run once:
  grip.attach(11);
}

void loop() {
  // put your main code here, to run repeatedly:
  grip.write(85);

  delay(1000);

  grip.write(90);

  delay(1000);

  grip.write(95);

  delay(1000);

  grip.write(90);

  delay(1000);
}
