import numpy as np
from numpy import pi
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot

rb = Dobot()

if __name__ == "__main__":
    
    T = rb.fkine(np.array([pi/4,pi/4,0,0,0,0]))
    print(T)
    Tf = SE3.Trans(0.9979 ,1.012 ,2.407) *SE3.OA([0,  0, 1], [1, 0, 0])

    #solution test )1,1,2.4142
    sol = rb.ikine_LMS(Tf,q0=np.array([0,0,0,0,0,0]))
    #sol.q[3] = -sol.q[1]-sol.q[2],mask = np.array([1,1,1,1,1,0])
    print(sol)

    print(rb.fkine(sol.q))
    qtraj = rtb.jtraj(np.array([0,0,0,0,0,0]), sol.q, 300)
    rb.plot(qtraj.q, movie="dobot.gif")