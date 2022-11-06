#from header import *
import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3
from ikdof import *

def robot():
    #reference frames translation and rotation
    E1 = rtb.ET.tz(0.333)
    E2 = rtb.ET.Rz()
    E3 = rtb.ET.Ry()
    E4 = rtb.ET.tz(0.316)
    E5 = rtb.ET.Rz()
    E6 = rtb.ET.tx(0.0825)
    E7 = rtb.ET.Ry(flip=True)
    E8 = rtb.ET.tx(-0.0825)
    E9 = rtb.ET.tz(0.384)
    E10 = rtb.ET.Rz()
    E11 = rtb.ET.Ry(flip=True)
    E12 = rtb.ET.tx(0.088)
    E13 = rtb.ET.Rx(np.pi)
    E14 = rtb.ET.tz(0.107)
    E15 = rtb.ET.Rz()


    panda = E1 * E2 * E3 * E4 * E5 * E6 * E7 * E8 * E9 * E10 * E11 * E12 * E13 * E14 * E15

    
    #return ets object
    return panda

qf= np.array([0.79,1.57,0])
q0 = np.array([0,0,0])
ets = robot()
#Final pose test
Tf = SE3.Trans(0.7, 0.2, 0.1) *SE3.OA([0,  1, 0], [0, 0, 1])
print(Tf)

rb = rtb.ERobot(ets)
#initial pose test
T=rb.fkine(np.zeros(7))
print(T)
#inv kinematics
sol = rb.ikine_LMS(Tf,ilimit = 3100)
print(sol)

print(rb.fkine(sol.q))



