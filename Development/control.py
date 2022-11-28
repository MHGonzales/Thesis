import numpy as np
from numpy import pi
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot


rb = Dobot()
q0 = rb.qr

def IKine(q0,x:float, y:float ,z:float ):
    Tf = SE3.Trans(x ,y ,z) *SE3.OA([0,  0, 1], [1, 0, 0])
    sol = rb.ikine_LMS(Tf,q0,)

if __name__ == "__main__":
    while True:
        x =1