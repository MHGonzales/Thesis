String j1 = "0";
String j2 = "0";
String j3 = "0";
 //Set the size of the array to equal the number of values you will be receiveing.

void setup()
{
    //Start serial.
    Serial.begin(9600);
    
}

void loop()
{
  if(Serial.available()){
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
    //Put values from the array into the variables.
    j1 = strArr[0];
    j2 = strArr[1];
    j3 = strArr[2];

    Serial.print("Joint 1: ");
    Serial.print(j1);
    Serial.print(" Joint 2: ");
    Serial.print(j2);
    Serial.print(" Joint 3: ");
    Serial.print(j3);
    Serial.print("\n");
  }

}
