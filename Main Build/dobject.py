from math import pi
import numpy as np
from roboticstoolbox import DHRobot,RevoluteMDH,jtraj
from spatialmath.base import trotx,troty,trotz,transl

class Dobot(DHRobot):

    def __init__(self):
        
        deg = pi/180
        mm =1e-3

        L1 = RevoluteMDH(
            
            qlim = np.array([-135*deg, 135*deg]),
            #d =140*mm,
            #flip =True
        )
        L2 = RevoluteMDH(
            alpha = pi/2,
            qlim = np.array([0*deg, 85*deg]),
            #flip=True,
            offset=90*deg
        )
        L3 = RevoluteMDH(
            a =135*mm,
            qlim = np.array([-10*deg, 95*deg]),
            offset=-90*deg,
            #flip=True
        )
        L4 = RevoluteMDH(
            a =147*mm,
            offset = -L2.theta - L3.theta ,
            #flip=True
        )
        L5 = RevoluteMDH(
            d=50*mm,
            #offset=-90*deg,
            #alpha = -np.pi/2,
            #flip=True
        )
        L6 = RevoluteMDH(
            a=0*mm,
            alpha = -np.pi/2,
            #flip=True
        )
        L7 = RevoluteMDH(
            alpha = np.pi/2,
            d=120*mm,
            a=50*mm,
            #flip=True
            #offset=-90*deg,
            #flip=True
        )

        
        tool = transl(0,0,35*mm)
        L = [L1,L2,L3,L4,L5,L6,L7]

        super().__init__(
            L,
            name = "Dobot",
            #tool =tool
            

        )
        self.qr = np.array([0*deg, deg*15, deg*40,-55*deg,90*deg,0*deg])
        self.qz = np.array([0*deg, deg*0, deg*0,0*deg,0*deg,0*deg,0*deg])

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz) 

if __name__ == "__main__":

    dobot = Dobot()
    print(dobot)