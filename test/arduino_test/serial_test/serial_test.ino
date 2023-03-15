float set_j1,set_j2,set_j3=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Starting Arduino");
  delay(2000);
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
    set_j3 = strArr[2].toFloat();
  }
  Serial.print(set_j1);
  Serial.print(",");
  Serial.print(set_j2);
  Serial.print(",");
  Serial.println(set_j3);
}
