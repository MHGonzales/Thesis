import numpy as np
from numpy import pi
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot
import DobotDllType as dType
from math import pi,degrees
import keyboard
from threading import *

rb = Dobot()
x = 0.187
y = 0.0
z = 0.1

q0 = np.ndarray([0,0,0,0,0])

def jpos():
    
    Tf = SE3.Trans(x ,y ,z) *SE3.OA([0,  0, 1], [1, 0, 0])
    sol = rb.ikine_LMS(Tf,rb.qz)
    return sol.q*180/pi
    
def setje():
    #loop to move through qtraj
    while True:
        current_pose=dType.GetPose(api)
        dType.SetPTPCmd(api,2,(x-0.040)*1000,y*1000,z*1000,current_pose[7],1) 
    #return
def d2p(deg:float):
    
    pwm = (deg/18)+2.5
    print(pwm)
    return pwm
def setjW(q:float):
    while True:
        pwm = d2p(q)
        dType.SetIOPWM(api, 4, 50, pwm, 1)
        dType.dSleep(1500)
    
    #return



def main():
    #branch based on button pressed
    """
    if mov == "a":
        y=y+0.01
        print(f"x:{x},y:{y},z{z}") 
    elif mov == "w":
        z=z+0.01
        print(f"x:{x},y:{y},z{z}")       
    elif mov == "s":
        z=z-0.01
        print(f"x:{x},y:{y},z{z}")        
    elif mov == "d":
        y=y-0.01
        print(f"x:{x},y:{y},z{z}")
    #obtain new coordinates
        #get x,y,z
    """
    #obtain joint angles
    qn = jpos()
    #aqtraj = qpath(qn,q0)
    #convert rad to degrees
        #qn = r2d(qtraj)
    #set joint angles in robot using DOBOT API
    #setje()
    #setjW(qn[4])
        #  and setjw(qtraj)
    #update new angles to be current angles
    
    #repeat
    #return 
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
    api = dType.load()
    dType.ConnectDobot(api, "", 115200)
    current_pose = dType.GetPose(api)
    
    dType.SetIOMultiplexing(api, 4, 2, 1)
    qn = jpos()
    t1 = Thread(target = setje)
    t2 = Thread(target = setjW,args = qn[4])
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    
    while True:
        
        if keyboard.read_key() == "a":
            y=y+0.02
            print(f"x:{x},y:{y},z{z}") 
        elif keyboard.read_key() == "w":
            z=z+0.02
            print(f"x:{x},y:{y},z{z}")       
        elif keyboard.read_key() == "s":
            z=z-0.02
            print(f"x:{x},y:{y},z{z}")    
        elif keyboard.read_key() == "d":
            y=y-0.02
            print(f"x:{x},y:{y},z{z}")    
        elif keyboard.read_key() == 'esc':
            break
        else:
            continue
        main()

    dType.DisconnectDobot(api)
    