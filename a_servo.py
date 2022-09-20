""" servo pyfirmata"""

import pyfirmata
from tkinter import *

def move_servo(angle):
    pin10.write(angle)
    
def main():
    global pin10
    
    board=pyfirmata.Arduino('COM11')

    iter8 = pyfirmata.util.Iterator(board)
    iter8.start()

    pin10 = board.get_pin('d:10:s')
    
    root = Tk()
    scale = Scale(root, command = move_servo, to = 175, 
                  orient = HORIZONTAL, length = 400, label = 'Angle')
    scale.pack(anchor = CENTER)

    root.mainloop()

main()