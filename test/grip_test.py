import time as tm
from threading import Thread

import xlwings as xw
import keyboard as kb

import roboticstoolbox as rtb
from spatialmath import SE3
from numpy import pi

from utilities_test import Dobot
from utilities_test.dobot import DobotDllType as dType
from serial import Serial as sr


print("Import Success !!")

ad = sr('COM4',9600)

def robot(grip:str="90"):
    global j4,j5,j6,l
    #calculate inverse kinematics for position       
    j4 = 90
    j5 = 90
    j6 = 90
    gr = grip
    pos_wrist = str(str(j4) +','+ str(j5) + ','+ str(j6) +','+ str(gr) +',')
    ad.write(pos_wrist.encode())   
    
def grip_close():
    g:int = 0
    while True:
        if kb.read_key() == "g":
            if g == 0:
                
                robot(grip = "80")
                g = 1
            else:
 
 
                robot(grip = "90")
                g=0
        tm.sleep(0.5) 
def grip_open():
    f:int = 0
    while True:
        if kb.read_key() == "f":
            if f == 0:
                
                robot(grip = "100")
                
                f = 1
            else:
                
                robot(grip = "90")
                
                f=0
        tm.sleep(0.5) 

if __name__ == "__main__":

    print(" Initializing Arduino Serial Connection")
    tm.sleep(5)
    print("Arduino Intialized")
    
    t16 = Thread(target = grip_close,daemon= True)
    t16.start()
    t17 = Thread(target = grip_open,daemon= True)
    t17.start()

    while True:
        if kb.read_key() == "esc":
            break
        else:
            continue
    