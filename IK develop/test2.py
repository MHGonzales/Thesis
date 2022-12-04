import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox.robot.ET import ET
from roboticstoolbox.robot.ERobot import ERobot
from roboticstoolbox.robot.Link import Link
from spatialmath import SE3
from math import pi
class dobot(ERobot):
    

    def __init__(self):

        deg = np.pi / 180
        mm = 1e-3
        tool_offset = (103) * mm

        l0 = Link(ET.tz(140*mm) * ET.Rz(), name="link0", parent=None)

        l1 = Link(ET.Rx(-90, "deg") * ET.Rz(), name="link1", parent=l0)

        l2 = Link(ET.Rx(90, "deg") * ET.tz(135*mm) * ET.Rx(-90, "deg")*ET.Rz(), name="link2", parent=l1)

        l3 = Link(ET.Rx(90, "deg") * ET.tz(147*mm) * ET.Rx(-90, "deg")*ET.Rz(), name="link3", parent=l2)
        l4 = Link(ET.Rx(90, "deg")*ET.Ry(-90, "deg")**ET.Rz(),name = "link4",parent=l3)
        l5 = Link(ET.Ry())
        #ee = Link(ET.Rx(90, "deg") , name="ee", parent=l3)
        
        #* ET.Rz(180, "deg")
        elinks = [l0, l1, l2,l3, ee] #ee]

        super(dobot, self).__init__(elinks, name="DOBOT", manufacturer="CHINA")

        self.qr = np.array([pi/4, pi/4, 0,0])
        self.qz = np.zeros(4)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

if __name__ == "__main__":  #run dobot test

    robot = dobot()
    robot.q
    T = robot.fkine(robot.qr)
    #print(robot.fkine(robot.qr))

    # IK
    

    #T = SE3(1,1,2.4142) * SE3.OA([0, 0, 1], [1, 0, 0])
    #print(T)
    sol = robot.ikine_LMS(T,robot.qz,ilimit =1000,mask= np.array([1,1,1,0,0,0]))  # solve IK, ignore additional outputs
    print(sol)  # display joint angles
    # FK shows that desired end-effector pose was achieved
    #print(robot.fkine(sol.q))
    qtraj = rtb.jtraj(robot.qz, sol.q, 25)
    robot.plot(qtraj.q, movie="dobot.gif")