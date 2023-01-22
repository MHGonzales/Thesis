from threading import Thread
from numpy import pi
from spatialmath import SE3
from dobject import Dobot
rb = Dobot()
x = 0.187
y = 0.0
z = 0.1

def runA():
    while True:
        Tf = SE3.Trans(x ,y ,z) *SE3.OA([0,  0, 1], [1, 0, 0])
        sol = rb.ikine_LMS(Tf,rb.qz)
        print ("Move Position Dobot\n")

def runB():
    while True:
        print ('Move Servo Position\n')

if __name__ == "__main__":
    t1 = Thread(target = runA)
    t2 = Thread(target = runB)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    while True:
        print("Waiting for Input\n")