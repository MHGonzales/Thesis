import numpy as np
from numpy import pi
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot


rb = Dobot()

if __name__ == "__main__":
    
    #print(rb.fkine(np.array([5.07626309e+01, -4.14250837e+01,  1.3e+01, -1.32807423e+01 ,3.92373839e+01, -2.78967742e-05])*pi/180))
    Tf = SE3.Trans(0.187 ,0 ,0.135) *SE3.OA([0,  0, 1], [1, 0, 0])
    Tf2 = SE3.Trans(0.187 ,-0.10 ,00.135) *SE3.OA([0,  0, 1], [1, 0, 0])
    
    sol = rb.ikine_LMS(Tf,rb.qz)
    sol2 = rb.ikine_LMS(Tf2,sol.q)
    #sol.q[3] = -sol.q[1]-sol.q[2],mask = np.array([1,1,1,1,1,0])
    #print(sol,sol2)
    print(f"{(sol.q)*(180/pi)}")
    print(f"{(sol2.q)*(180/pi)}")
    print(sol2.success)
    #print(rb.fkine(sol2.q))
    qtraj = rtb.jtraj(sol.q, sol2.q, 100)
    rb.plot(qtraj.q, movie="dobot.gif")
    