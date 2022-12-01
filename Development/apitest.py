import DobotDllType as dType
from dobject import Dobot
from math import degrees
import roboticstoolbox as rtb
import numpy as np


print(1-5)
rb = Dobot()
api = dType.load()
#state = dType.ConnectDobot(api, "", 115200)[0]
    #initialize starting joint angles
q0 = [0,0,0]
for i in range(0,3,1):
    qd = degrees(rb.qr[i])
    q0[i] = qd
    
#current_pose = dType.GetPose(api)
#dType.SetPTPCmd(api,4,q0[0],q0[1],q0[2],current_pose[7],1)
tf = rb.fkine(rb.qr)
sol = rb.ikine_LMS(tf,rb.qr)
print(tf)
print(sol.q)
dType.DisconnectDobot(api)

