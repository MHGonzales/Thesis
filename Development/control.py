import numpy as np
from math import pi,degrees
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot
import DobotDllType as dType
import keyboard


#global variables

rb = Dobot()
MM=1e-3
x = 0.187
y = 0.1
z = 0.135


#determine joint angles
# inputs: coordinates, initial joint angles
def jpos(q0:np.ndarray,x:float,y:float,z:float):
    
    Tf = SE3.Trans(x ,y ,z) *SE3.OA([0,  0, 1], [1, 0, 0])
    sol = rb.ikine_LMS(Tf,q0)
    #print(rb.fkine(sol.q))
    #print(sol)
    return sol.q

#determine joint trajectory
def qpath(qn,q0):
    qtraj = rb.jtraj(qn,q0,75)
    return qtraj.q

#convert rad to deg
def r2d(rad:float):
    deg:float
    #deg = degrees(rad)
    return deg

#convert deg to pwm
def d2p(deg:float):
    pwm:float
    #
    return pwm

#update joint angles
#input sol.q
def setje(qn):
    #loop to move through qtraj
    q0 = [0,0,0]
    for i in range(0,3,1):
        qd = degrees(qn[i])
        q0[i] = -qd
    print(q0)
    current_pose=dType.GetPose(api)
    dType.SetPTPCmd(api,4,q0[0],-q0[1],-q0[2],0,1) 
    return

#update wrist positionw
def setjw(pwm:float):
    
    #dType.SetIOMultiplexing(api, 4, 2, 1)
    #dType.SetIOMultiplexing(api, 6, 2, 1)
    #dType.SetIOMultiplexing(api, 8, 2, 1)

    #loop to move through qtraj
    #dType.SetIOPWM(api, 4, 50, pwm,1)
    #dType.SetIOPWM(api, 6, 50, pwm,1)
    #dType.SetIOPWM(api, 8, 50, pwm,1)

    return
#input
def main(mov:str,q0:np.ndarray,x,y,z):
    #branch based on button pressed
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
    #obtain joint angles
    qn = jpos(q0,x,y,z)
    #aqtraj = qpath(qn,q0)
    #convert rad to degrees
        #qn = r2d(qtraj)
    #set joint angles in robot using DOBOT API
    setje(qn)
        #  and setjw(qtraj)
    #update new angles to be current angles
    
    #repeat
    return qn,x,y,z

if __name__ == "__main__":
    
    api = dType.load()
    state = dType.ConnectDobot(api, "", 115200)[0]
    
    #initialize starting joint angles
    q0 = [0,0,0]
    for i in range(0,3,1):
        qd = degrees(rb.qz[i])
        q0[i] = qd
    print(q0)
    current_pose = dType.GetPose(api)
    dType.SetPTPCmd(api,4,q0[0],-q0[1],-q0[2],current_pose[7],1)

    q0 = rb.qr
    qset = [q0,x,y,z]
    
    while True:
        #print(qset[0])
        if keyboard.read_key() == "a":
            qset = main("a",qset[0],qset[1],qset[2],qset[3])
            
        elif keyboard.read_key() == "w":
            qset = main("w",qset[0],qset[1],qset[2],qset[3])
            
        elif keyboard.read_key() == "s":
            qset =main("s",qset[0],qset[1],qset[2],qset[3])
            
        elif keyboard.read_key() == "d":
            qset =main("d",qset[0],qset[1],qset[2],qset[3])
            
        elif keyboard.read_key() == 'esc':
            break
        else:
            continue
    #main()
    dType.DisconnectDobot(api)
    