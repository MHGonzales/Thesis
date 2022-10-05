""" servo pyfirmata"""

import pyfirmata
from time import sleep

def move_servo(angle):
    pin10.write(angle)
    sleep(0.015)
    
def main():
    global pin10
    
    board=pyfirmata.Arduino('COM7')

    iter8 = pyfirmata.util.Iterator(board)
    iter8.start()

    pin10 = board.get_pin('d:10:s')
    
    while True:
        for i in range(0,180):
            move_servo(i)
        for i in range(180,0,-1):
            move_servo(i)

main()