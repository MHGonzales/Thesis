import xlwings as xw
import keyboard as kb
from threading import Thread
import time as tm
from numpy import pi
from spatialmath import SE3
from dobject import Dobot
import DobotDllType as dType


#specify sheets
#read data range from
#define keyboard funcions
#calculate delta
#move robot using delta
#activate threads for keyboard

ws = xw.Book("coordinates_py.xlsx").sheets['Middle Lower Load']
table = ws.range("A1:C7").value


#this is for delta movement
def robot(y,z):
    
    #current_pose=dType.GetPose(api)
    dType.SetPTPCmdEx(api, 7, 0,  y,  z, 0, 1)
    dType.dSleep(1000)


#create function rotate knob.
    #move to knob 2 servos (1st and 2nd servo)
    # grab knob( 1 servo last )
    #rotate knob(1 servo middle)


#this is for delta calculation
def delta(oy,oz,ny,nz):
    global i
    dy = ny-oy
    dz = nz - oz
    print("Delat y: ",dy ," Delta z: ",dz )
    #new values
    #subtract from old
    robot(dy,dz)
    #new values becomes old values
    return

def left():
    global i,table
    i=0
    while True:
        if kb.read_key() == "a":
            oy,oz = table[i][1],table[i][2]
            i-=2
            ny = table[i][1]
            nz = table[i][2]
            delta(oy,oz,ny,nz)
        tm.sleep(0.25)

def right():
    global i,table
    while True:
        if kb.read_key() == "d":
            oy,oz = table[i][1],table[i][2]
            i+=2
            ny = table[i][1]
            nz = table[i][2]
            delta(oy,oz,ny,nz)
        tm.sleep(0.25)

def up():
    global i,table
    while True:
        if kb.read_key() == "w":
            oy,oz = table[i][1],table[i][2]
            i-=1
            ny = table[i][1]
            nz = table[i][2]
            delta(oy,oz,ny,nz)
        tm.sleep(0.25)

def down():
    global i,table
    while True:
        if kb.read_key() == "s":
            oy,oz = table[i][1],table[i][2]
            i+=1
            ny = table[i][1]
            nz = table[i][2]
            delta(oy,oz,ny,nz)
        tm.sleep(0.25)

if __name__ == "__main__":


    api = dType.load()
    dType.ConnectDobot(api, "", 115200)
    #dType.SetIOMultiplexing(api, 4, 2, 1)
    #global current_pose
    dType.SetPTPCmd(api,2,140,0,0,0,1) 
    current_pose=dType.GetPose(api)
    oy,oz = current_pose[1],current_pose[2]
    ny = table[0][1]
    nz = table[0][2]
    delta(oy,oz,ny,nz)

    t1 = Thread(target=left)
    t2 = Thread(target=right)
    t3 = Thread(target=up)
    t4 = Thread(target=down)
    


    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t4.setDaemon(True)
    

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    


    while True:
        if kb.read_key() == "esc":
            break
        else:
            continue
    dType.DisconnectDobot(api)