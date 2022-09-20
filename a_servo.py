from pyfirmata import Arduino, SERVO
from time import sleep

port = ''
pin = 10
board = Arduino(port)
board.digital(pin).mode = SERVO
def rotateSERVO(pin, angle):
   board.digital[pin].write(angle)
   sleep(0.015)

while True:
    for i in range (0,180):
        rotateSERVO(pin,i)
    for i in range(180,1,-1):
        rotateSERVO(pin, i)