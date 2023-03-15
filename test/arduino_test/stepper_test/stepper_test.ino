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
#define MOTOR_STEPS 200
#define RPM 30

#define DIR 3
#define STEP 4
#define SLEEP 5

/*
 * Choose one of the sections below that match your board
 */
 /*
#include "A4988.h"
#define MS1 10
#define MS2 11
#define MS3 12
A4988 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, MS1, MS2, MS3);
*/

/*
#include "DRV8825.h"
#define MODE0 8
#define MODE1 7
#define MODE2 6
DRV8825 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, MODE0, MODE1, MODE2);
*/
#include "A4988.h"
#define MS1 6
#define MS2 7
#define MS3 8
A4988 stepper(MOTOR_STEPS, DIR, STEP, SLEEP, MS1, MS2, MS3);
// #include "BasicStepperDriver.h" // generic
// BasicStepperDriver stepper(DIR, STEP);

void setup() {
  /*
     * Set target motor RPM.
     */
  Serial.begin(9600);
  //digitalWrite(6,LOW); // Set Enable low
  stepper.begin(RPM);

  // if using enable/disable on ENABLE pin (active LOW) instead of SLEEP uncomment next line
  // stepper.setEnableActiveState(LOW);
  stepper.enable();
  stepper.setMicrostep(1); 
  // set current level (for DRV8880 only).
  // Valid percent values are 25, 50, 75 or 100.
  // stepper.setCurrent(100);
}

void loop() {

  /*
     * Moving motor in full step mode is simple:
     */
 // Set microstep mode to 1:1

  // One complete revolution is 360°
  stepper.rotate(350*15);  // forward revolution

  // One complete revolution is also MOTOR_STEPS steps in full step mode
  //stepper.move(MOTOR_STEPS);    // forward revolution
  Serial.println("First Rotation");
  delay(1000);
  stepper.rotate(-360*15);
  Serial.println("Second Rotation");
  delay(1000);
}
