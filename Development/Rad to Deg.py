# Python code to demonstrate
# working of radians()

# for radians
import math


## change input to inverse kinematics output
x = int(input('Input Radians Value: '));
deg = math.degrees(x);
print(deg);
pwm = (deg/18.0) + 2.5;
print(pwm);



