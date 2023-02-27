/*
 * Microstepping demo
 *
 * This requires that microstep control pins be connected in addition to STEP,DIR
 *
 * Copyright (C)2015 Laurentiu Badea
 *
 * This file may be redistributed under the terms of the MIT license.
 * A copy of this license has been included with this distribution in the file LICENSE.
 */
#include <Arduino.h>

// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 400
#define RPM 30

#define DIR 3
#define STEP 4
#define SLEEP 2

/*
 * Choose one of the sections below that match your board
 */


#include "A4988.h"
#define MS1 5
#define MS2 6
#define MS3 7
A4988 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, MS1, MS2, MS3);

// #include "BasicStepperDriver.h" // generic
// BasicStepperDriver stepper(DIR, STEP);

void setup() {
    /*
     * Set target motor RPM.
     */
      Serial.begin(9600);
      digitalWrite(6,LOW); // Set Enable low
      stepper.begin(RPM);
    // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
    // stepper.setEnableActiveState(LOW);
    stepper.enable();
    
    // set current level (for DRV8880 only). 
    // Valid percent values are 25, 50, 75 or 100.
    // stepper.setCurrent(100);
}

void loop() {

    /*
     * Moving motor in full step mode is simple:
     */
    stepper.setMicrostep(2);  // Set microstep mode to 1:1

    // One complete revolution is 360°
    stepper.rotate(360);     // forward revolution

    // One complete revolution is also MOTOR_STEPS steps in full step mode
    //stepper.move(MOTOR_STEPS);    // forward revolution

    stepper.rotate(-360);    
    //stepper.move(MOTOR_STEPS); 
    //digitalWrite(6,HIGH); // Set Enable high

}
