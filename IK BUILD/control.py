import numpy as np
from numpy import pi
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot


rb = Dobot()

if __name__ == "__main__":
    
    
    Tf = SE3.Trans(0.200 ,0 ,0.140) *SE3.OA([0,  0, 1], [1, 0, 0])
    Tf2 = SE3.Trans(0.200 ,-0.15 ,0.25) *SE3.OA([0,  0, 1], [1, 0, 0])
    
    sol = rb.ikine_LMS(Tf,q0=np.array([0,0,0,0,0,0]))
    sol2 = rb.ikine_LMS(Tf2,q0 = sol.q)
    #sol.q[3] = -sol.q[1]-sol.q[2],mask = np.array([1,1,1,1,1,0])
    

    #print(rb.fkine(sol.q))
    qtraj = rtb.jtraj(sol.q, sol2.q, 50)
    #rb.plot(qtraj.q, movie="dobot.gif")
    print(qtraj.q[1,])