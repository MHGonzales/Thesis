import numpy as np
from roboticstoolbox.robot.ET import ET
from roboticstoolbox.robot.ERobot import ERobot
from roboticstoolbox.robot.Link import Link
from spatialmath import SE3
from math import pi
class dobot(ERobot):
    """
    Create model of Franka-Emika Panda manipulator
    panda = Panda() creates a robot object representing the Franka-Emika
    Panda robot arm. This robot is represented using the elementary
    transform sequence (ETS).
    ETS taken from [1] based on
    https://frankaemika.github.io/docs/control_parameters.html
    :references:
        - Kinematic Derivatives using the Elementary Transform
          Sequence, J. Haviland and P. Corke
    """

    def __init__(self):

        deg = np.pi / 180
        mm = 1e-3
        tool_offset = (103) * mm

        l0 = Link(ET.tz(1) * ET.Rz(), name="link0", parent=None)

        l1 = Link(ET.Rx(-90, "deg") * ET.Rz(), name="link1", parent=l0)

        l2 = Link(ET.Rx(90, "deg") * ET.tz(1) * ET.Rx(-90, "deg")*ET.Rz(), name="link2", parent=l1)

        l3 = Link(ET.Rx(90, "deg") * ET.tz(1) * ET.Rx(-90, "deg")*ET.Rz(), name="link3", parent=l1)
        ee = Link(ET.Rx(90, "deg") , name="ee", parent=l3)
        #* ET.Rz(180, "deg")
        elinks = [l0, l1, l2,l3, ee] #ee]

        super(dobot, self).__init__(elinks, name="DOBOT", manufacturer="CHINA")

        self.qr = np.array([pi/4, pi/4, 0,0])
        self.qz = np.zeros(4)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

if __name__ == "__main__":  #run dobot test

    robot = dobot()
    T = robot.fkine(robot.qr)
    print(robot.fkine(robot.qr))

    # IK
    1.408,1.421,1.002

    T = SE3(1,1,2.4142) * SE3.OA([0, 1, 0], [0, 0, 1])
    print(T)
    sol = robot.ikine_LMS(T,robot.qz,ilimit =1000,mask= np.array([1,1,1,0,0,0]))  # solve IK, ignore additional outputs
    print(sol)  # display joint angles
    # FK shows that desired end-effector pose was achieved
    print(robot.fkine(sol.q))