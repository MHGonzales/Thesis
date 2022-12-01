import numpy as np
from numpy import pi
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot


rb = Dobot()

if __name__ == "__main__":
    
    
    Tf = SE3.Trans(0.200 ,0 ,0.140) *SE3.OA([0,  0, 1], [1, 0, 0])
    Tf2 = SE3.Trans(0.200 ,0.01 ,0.140) *SE3.OA([0,  0, 1], [1, 0, 0])
    
    sol = rb.ik_lm_sugihara(Tf,rb.qr)
    sol2 = rb.ik_lm_sugihara(Tf2,q0 = sol[0])
    #sol.q[3] = -sol.q[1]-sol.q[2],mask = np.array([1,1,1,1,1,0])
    
    print((sol[0])*(180/pi))
    print(rb.fkine(rb.qr))
    qtraj = rtb.jtraj(rb.qr, sol[0], 25)
    rb.plot(qtraj.q, movie="dobot.gif")
    