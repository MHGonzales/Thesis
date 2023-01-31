#include <Servo.h>

Servo servo_1,servo_2,servo_3; // servo controller (multiple can exist)

int servo_pin = 9; // PWM pin for servo control
int pos = 0;    // servo starting position

void setup() {
  servo_1.attach(servo_pin,520,2475);
  servo_2.attach(10,625,2550);
  servo_3.attach(11); // start servo control
  Serial.begin(9600); // start serial monitor
  servo_1.write(pos);
  servo_2.write(pos);
  servo_3.write(pos); // move servo to 0 degrees
  Serial.println("Positioned at 0 Degrees");
  Serial.println("Input Desired Angle and Press Enter");
}

void loop() {
  while (Serial.available()){
    String in_char = Serial.readStringUntil('\n'); // read until the newline
    Serial.print("Moving to: ");
    Serial.print(in_char);
    Serial.println(" Degrees");
    if (in_char.toInt()>=pos)
    {
      for (pos; pos <= in_char.toInt(); pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
        servo_1.write(pos); 
        servo_2.write(pos);
        servo_3.write(pos);             // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15 ms for the servo to reach the position
       }
    }
    if (in_char.toInt()<=pos)
    {
      for (pos; pos >= in_char.toInt(); pos -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
        servo_1.write(pos);
        servo_2.write(pos);
        servo_3.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15 ms for the servo to reach the position
       }
    } // convert angle and write servo // delay for maximum speed
    pos = in_char.toInt();
  }
  
}
