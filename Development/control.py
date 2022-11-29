import numpy as np
from numpy import pi
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot
import DobotDllType as dType

#global variables
q0:np.ndarray
rb = Dobot()

#determine joint angles
# inputs: coordinates, initial joint angles
def jpos(q0:np.ndarray,x:float,y:float,z:float):
    
    Tf = SE3.Trans(x ,y ,z) *SE3.OA([0,  0, 1], [1, 0, 0])
    sol = rb.ikine_LMS(Tf,q0)
    return sol.q

#determine joint trajectory
def qpath(qn,q0):
    qtraj = rb.jtraj(qn,q0,100)
    return qtraj.q

#convert rad to deg
def r2g(rad:float):
    deg:float

    return deg

#convert rad to pwm
def r2p(rad:float):
    pwm:float

    return pwm

#update joint angles
def updateje():
    exit

#update wrist position
def updatejw():
    exit

def main():
    exit

if __name__ == "__main__":
    api = dType.load()
    main()
    