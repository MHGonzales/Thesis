from pyfirmata import Arduino, SERVO
from time import sleep


board = Arduino('COM6')
pin = 9
board.digital[pin].mode = SERVO

def rotateServo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)

while True:
    for i in range(0,180):
        rotateServo(pin,i)
    for i in range(180,1,-1):
        rotateServo(pin,i)
