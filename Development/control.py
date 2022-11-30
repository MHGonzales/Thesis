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
    qtraj = rb.jtraj(qn,q0,75)
    return qtraj.q

#convert rad to deg
def r2d(rad:float):
    deg:float
    #erika
    return deg

#convert deg to pwm
def r2p(rad:float):
    pwm:float
    #erika
    return pwm

#update joint angles
#input sol.q
def setje():
    #loop to move through qtraj
    #dtype.SetPTPCmd(api,4,j1,j2,j3) 
    exit

#update wrist position
def setjw(pwm:float):
    
    #dType.SetIOMultiplexing(api, 4, 2, 1)
    #dType.SetIOMultiplexing(api, 6, 2, 1)
    #dType.SetIOMultiplexing(api, 8, 2, 1)

    #loop to move through qtraj
    #dType.SetIOPWM(api, 4, 50, pwm,1)
    #dType.SetIOPWM(api, 6, 50, pwm,1)
    #dType.SetIOPWM(api, 8, 50, pwm,1)

    exit

def main():
    #branch based on button pressed
    #obtain new coordinates
        #get x,y,z
    #obtain joint angles
        #qn = jpos(q0,x,y,z)
        #qtraj = qpath(qn,q0)
    #convert rad to degrees
        #qn = r2d(qtraj)
    #convert degrees to pwm
        #qne = r2(qtraj)
    #set joint angles in robot using DOBOT API
        #setje(qtraj) and setjw(qtraj)
    #update new angles to be current angles
        #q0 = qn
    #repeat
    exit

if __name__ == "__main__":
    api = dType.load()
    #initialize starting joint angles
        #q0 = rb.qz
        #dtype.SetJointAngle(api,4,q0[0],q0[1],q0[2],current_pose[7],1)
    #while True:
        #keyboard event go to main
    main()
    