from threading import Thread
from numpy import pi
from spatialmath import SE3
from dobject import Dobot
import DobotDllType as dType
import keyboard

rb = Dobot()
x = 0.187
y = -0.083
z = -0.070

def d2p(deg:float):
    
    pwm = (deg/18)+2.5
    return pwm

def runA():
    while True:
        Tf = SE3.Trans(x ,y ,z) *SE3.OA([0,  0, 1], [1, 0, 0])
        sol = rb.ikine_LMS(Tf,rb.qz)
        qn = sol.q*180/pi
        pwm = d2p(qn[4])
        dType.SetIOPWM(api, 4, 50, pwm, 1)
        dType.dSleep(1000)
        

def runB():
    while True:
        current_pose=dType.GetPose(api)
        dType.SetPTPCmd(api,2,(x-0.040)*1000,y*1000,z*1000,current_pose[7],1) 
        dType.dSleep(1000)

if __name__ == "__main__":

    api = dType.load()
    dType.ConnectDobot(api, "", 115200)
    dType.SetIOMultiplexing(api, 4, 2, 1)
    
    t1 = Thread(target = runA)
    t2 = Thread(target = runB)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    while True:
        if keyboard.read_key() == "a":
            message = "a"
            y=y+0.02
            print(f"x:{x},y:{y},z{z}")   # send message
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
            print("Controller left the chat")
            break
        else:
            print("No data received")
            continue
