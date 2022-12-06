import numpy as np
from numpy import pi
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot
import DobotDllType as dType

rb = Dobot()
x = 0.187
y = -0.07
z = 0.135

q0 = np.ndarray(0,0,0,0)

def jpos(q0:np.ndarray):
    
    Tf = SE3.Trans(x ,y ,z) *SE3.OA([0,  0, 1], [1, 0, 0])
    sol = rb.ikine_LMS(Tf,q0)
    #print(rb.fkine(sol.q))
    #print(sol)
    


if __name__ == "__main__":
    
    #print(rb.fkine(rb.qz))
    #Tf = SE3.Trans(x ,y ,z) *SE3.OA([0,  0, 1], [1, 0, 0])
    #Tf2 = SE3.Trans(0.187 ,0.100 ,0.135) *SE3.OA([0,  0, 1], [1, 0, 0])
    #api = dType.load()
    #state = dType.ConnectDobot(api, "", 115200)[0]
    
    #sol = rb.ikine_LMS(Tf,rb.qz)
    #sol2 = rb.ikine_LMS(Tf2,sol.q)
    #sol.q[3] = -sol.q[1]-sol.q[2],mask = np.array([1,1,1,1,1,0])
    #print(sol,sol2)
    #print(f"{-(sol.q)*(180/pi)}")
    
    #current_pose=dType.GetPose(api)
    #dType.SetPTPCmd(api,4,sol.q[0]*(180/pi),-sol.q[1]*(180/pi),-sol.q[2]*(180/pi),current_pose[7],1)
    #print(dType.GetPose(api))
    #dType.SetPTPCmd(api,4,sol.q[0]*(180/pi),current_pose[5],-sol.q[2]*(180/pi),current_pose[7],1)  
    #print(f"{-(sol2.q)*(180/pi)}")current_pose[6]
    #print(sol.success)
    #print(rb.fkine(sol.q))
    #qtraj = rtb.jtraj(sol.q, sol2.q, 100)
    #rb.plot(qtraj.q, movie="dobot.gif")
    #dType.DisconnectDobot(api)
    exit