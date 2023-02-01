#include <Servo.h>

Servo servo_1,servo_2,servo_3; // servo controller (multiple can exist)
int pos_1,pos_2,pos_3 = 0;    // servo starting position
int j1,j2,j3 = 0;

void setup() {
  servo_1.attach(9,520,2465);
  servo_2.attach(10,625,2540);
  servo_3.attach(11,520,2460); // start servo control
  Serial.begin(9600); // start serial monitor
  servo_1.write(pos_1);
  servo_2.write(pos_2);
  servo_3.write(pos_3); // move servo to 0 degrees
  Serial.println("Positioned at 0 Degrees");
  Serial.println("Input Desired Angle and Press Enter");
}

void loop() {
  while (Serial.available()){
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

    if (j1>=pos_1)
    {
      for (pos_1; pos_1 <= j1; pos_1 += 1) { 
        servo_1.write(pos_1);             // tell servo to go to position in variable 'pos'
        delay(30);                       // waits 15 ms for the servo to reach the position
       }
    }
    if (j2>=pos_2)
    {
      for (pos_2; pos_2 <= j2; pos_2 += 1) { 
        servo_2.write(pos_2);             // tell servo to go to position in variable 'pos'
        delay(20);                       // waits 15 ms for the servo to reach the position
       }
    }
    if (j3>=pos_3)
    {
      for (pos_3; pos_3 <= j3; pos_3 += 1) { 
        servo_3.write(pos_3);             // tell servo to go to position in variable 'pos'
        delay(20);                       // waits 15 ms for the servo to reach the position
       }
    }
    if (j1<=pos_1)
    {
      for (pos_1; pos_1 >= j1; pos_1 -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
        servo_1.write(pos_1);              // tell servo to go to position in variable 'pos'
        delay(20);                       // waits 15 ms for the servo to reach the position
       }
    }
    if (j2<=pos_2)
    {
      for (pos_2; pos_2 >= j2; pos_2 -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
        servo_2.write(pos_2);              // tell servo to go to position in variable 'pos'
        delay(20);                       // waits 15 ms for the servo to reach the position
       }
    }
    if (j3<=pos_3)
    {
      for (pos_3; pos_3 >= j3; pos_3 -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
        servo_3.write(pos_3);              // tell servo to go to position in variable 'pos'
        delay(30);                       // waits 15 ms for the servo to reach the position
       }
    } // convert angle and write servo // delay for maximum speed
    pos_1 = j1;
    pos_2 = j2;
    pos_3 = j3;
  }
  
}
