#from header import *
import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3
#from ikdof import *

def robot():
    deg = np.pi / 180
    mm = 1e-3
    tool_offset = (103) * mm

    l0 = rtb.Link(rtb.ET.tz(0.333) * rtb.ET.Rz(), name="link0", parent=None)

    l1 = rtb.Link( rtb.ET.Ry(), name="link1", parent=l0)

    l2 =rtb.Link( rtb.ET.tz(0.316) * rtb.ET.Rz(), name="link2", parent=l1)

    l3 = rtb.Link(rtb.ET.tx(0.0825) *  rtb.ET.Ry(), name="link3", parent=l2)

    l4 = rtb.Link(
            rtb.ET.tx(-0.0825) * rtb.ET.tz(0.384) * rtb.ET.Rz(),
            name="link4",
            parent=l3,
        )

    l5 = rtb.Link(rtb.ET.Ry(), name="link5", parent=l4)

    l6 = rtb.Link(
            rtb.ET.tx(0.088) * rtb.ET.Rx(180, "deg") * rtb.ET.tz(0.107) * rtb.ET.Rz(),
            name="link6",
            parent=l5,
        )

    ee = rtb.Link(rtb.ET.tz(tool_offset) * rtb.ET.Rz(-np.pi / 4), name="ee", parent=l6)

    elinks = [l0, l1, l2, l3, l4, l5, l6, ee]

    panda = rtb.ERobot(elinks)

    return panda

qf= np.array([0.79,1.57,0])
q0 = np.array([0,0,0])
ets = robot()
#Final pose test
Tf = SE3.Trans(0.7, 0.2, 0.1) *SE3.OA([0,  1, 0], [0, 0, -1])
print(Tf)

rb = rtb.ERobot(ets)
#initial pose test
T=rb.fkine(np.zeros(7))
print(T)
#inv kinematics
sol = rb.ikine_LMS(Tf,q0=np.array([0,0,0,0,0,0,0]))
print(sol)

print(rb.fkine(sol.q))



