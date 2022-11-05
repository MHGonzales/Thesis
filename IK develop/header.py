import numpy as np
import roboticstoolbox as rtb


We = np.diag([1,1,1,1,1,1])


def robot(l0:int,l1:int,l2:int):
    #reference frames translation and rotation
    e1 = rtb.ET.tz(l0)
    e2 = rtb.ET.Rz()
    e3 = rtb.ET.Ry()
    e4 = rtb.ET.tz(l1)
    e5 = rtb.ET.Ry()
    e6 = rtb.ET.tz(l2)
    
    
    #forward kinematics

    ets = rtb.ETS([e1, e2, e3, e4, e5, e6])
    #return ets object
    return ets

def error (Ti: np.ndarray, Tf: np.ndarray):

    
    e = rtb.angle_axis(Ti, Tf)
    E = 0.5 * e @ We @ e

    return e,E

def NR(ets: rtb.ETS, Tep: np.ndarray, q: np.ndarray):
    Te = ets.eval(q)
    e, E = error(Te, Tep)

    J = ets.jacob0(q)

    while E<1e-6:
        
        q += np.linalg.pinv(J) @ e
    
    return E, q

def createMatrix(x:float,y:float,z:float):

    im = np.eye(4)

    #Im = np.diag(im)
    
    for i in range(3):
        if i == 0:
            im[i,3] = x;
        if i == 1:
            im[i,3] = y;   
        if i == 2:
            im[i,3] = z;
    
    return im