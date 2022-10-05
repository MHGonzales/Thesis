import pyfirmata
from time import sleep
port ='COM7'
pin = 10
board = pyfirmata.Arduino(port)

board.digital[pin].mode = pyfirmata.SERVO

def move_servo(pin,angle):
    board.digital[pin].write(angle)
    sleep(0.015)

while True:
    for i in range(0,180):
        move_servo(pin,i)
    for i in range(180,0,-1):
        move_servo(pin,i)