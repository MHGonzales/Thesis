from math import pi
import numpy as np
from roboticstoolbox import DHRobot,RevoluteMDH,jtraj
from spatialmath.base import trotx,troty,trotz,transl

class Dobot(DHRobot):

    def __init__(self):
        
        deg = pi/180
        mm =1e-3

        L1 = RevoluteMDH(
            d =1,
            qlim = np.array([-135*deg, 135*deg])
        )
        L2 = RevoluteMDH(
            alpha = pi/2,
            qlim = np.array([0*deg, 85*deg])
        )
        L3 = RevoluteMDH(
            a =1,
            qlim = np.array([-10*deg, 95*deg]),
        )
        L4 = RevoluteMDH(
            a =1,
            offset = -L2.theta - L3.theta ,
        )
        L5 = RevoluteMDH(
            d=0.01,
            alpha = np.pi/2,
        )
        L6 = RevoluteMDH(
            alpha = np.pi/2,
            d=0.01,
            offset = 90 *deg
        )
        L7 = RevoluteMDH(
            alpha = -np.pi/2,

        )
        #tool = 
        L = [L1,L2,L3,L4,L5]

        super().__init__(
            L,
            name = "Dobot",

        )
        self.qr = np.array([pi/4, pi/4, 0,0])
        self.qz = np.zeros(5)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz) 

if __name__ == "__main__":

    dobot = Dobot()
    print(dobot)