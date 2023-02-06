import xlwings as xw
import keyboard as kb
from threading import Thread
import time as tm
from numpy import pi
from spatialmath import SE3
from dobject import Dobot
import DobotDllType as dType
from serial import Serial as sr
import roboticstoolbox as rtb

#specify sheets
#read data range from
#define keyboard funcions
#calculate delta
#move robot using delta
#activate threads for keyboard

ad = sr('COM6',9600)
rb = Dobot()

#this is for delta movement
def robot(dx,dy,dz,nx,ny,nz):
    #calculate inverse kinematics for position
    Tf = SE3.Trans((nx+90)/1000 ,ny/1000 ,nz/1000) *SE3.OA([0,  0, 1], [1, 0, 0])
    sol = rb.ikine_LMS(Tf,rb.qz)
    qn =sol.q*180/pi
    j4:str = str(0)
    j5:str= str(qn[5])
    j6:str= str(qn[6])
    pos_wrist = str(j4 +','+ j5 + ','+ j6 +',')
    ad.write(pos_wrist.encode())   
    dType.SetPTPCmdEx(api, 7, dx,  dy,  dz, 0, 1)

    
    #send serial to arduino

    


#create function rotate knob.
    #move to knob 2 servos (1st and 2nd servo)
    # grab knob( 1 servo last )
    #rotate knob(1 servo middle)

def low_mid():
    global table,i
    while True:
        if kb.read_key() == "k":
            ws = xw.Book("coordinates_py.xlsx").sheets['Middle Lower Load']
            table = ws.range("A1:C7").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =140, table[0][1],table[0][2]
            i=0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def high_mid():
    global table,i
    while True:
        if kb.read_key() == "i":
            ws = xw.Book("coordinates_py.xlsx").sheets['Middle Upper Load']
            table = ws.range("A1:C7").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =140, table[0][1],table[0][2]
            i=0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def high_right():
    global table,i
    while True:
        if kb.read_key() == "o":
            ws = xw.Book("coordinates_py.xlsx").sheets['Right Upper Load']
            table = ws.range("A1:C2").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =140, table[0][1],table[0][2]
            i=0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def low_right():
    global table,i
    while True:
        if kb.read_key() == "l":
            ws = xw.Book("coordinates_py.xlsx").sheets['Data Acquisition']
            table = ws.range("A1:C2").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =140, table[0][1],table[0][2]
            i=0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)


#this is for delta calculation
def delta(ox,oy,oz,nx,ny,nz):
    
    dy = ny-oy
    dz = nz - oz
    dx = nx-ox
    print("Delta x: ",dx,"Delat y: ",dy ," Delta z: ",dz )
    #new values
    #subtract from old
    robot(dx,dy,dz,nx,ny,nz)
    #new values becomes old values
    return

def left():
    global i,table
    i=0
    while True:
        if kb.read_key() == "a":
            current_pose = dType.GetPose(api)
            ox,oy,oz =current_pose[0], table[i][1],table[i][2]
            i-=2
            nx = current_pose[0]
            ny = table[i][1]
            nz = table[i][2]
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def right():
    global i,table
    while True:
        if kb.read_key() == "d":
            current_pose = dType.GetPose(api)
            ox,oy,oz =current_pose[0], table[i][1],table[i][2]
            i+=2
            nx = current_pose[0]
            ny = table[i][1]
            nz = table[i][2]
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def up():
    global i,table
    while True:
        if kb.read_key() == "w":
            current_pose = dType.GetPose(api)
            ox,oy,oz =current_pose[0], table[i][1],table[i][2]
            i-=1
            nx = current_pose[0]
            ny = table[i][1]
            nz = table[i][2]
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def down():
    global i,table
    while True:
        if kb.read_key() == "s":
            current_pose = dType.GetPose(api)
            ox,oy,oz =current_pose[0], table[i][1],table[i][2]
            i+=1
            nx = current_pose[0]
            ny = table[i][1]
            nz = table[i][2]
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

if __name__ == "__main__":


    api = dType.load()
    dType.ConnectDobot(api, "", 115200)
    #dType.SetIOMultiplexing(api, 4, 2, 1)
    #global current_pose
    current_pose=dType.GetPose(api)
    dType.SetPTPCmd(api,2,100,0,0,0,1) 
    
    print(" Initializing Arduino Serial Connection")
    tm.sleep(5)
    print("Initializing threads") 
    t1 = Thread(target=left)
    t2 = Thread(target=right)
    t3 = Thread(target=up)
    t4 = Thread(target=down)
    t5= Thread(target=low_mid)
    t6 = Thread(target=low_right)
    t7 = Thread(target=high_mid)
    t8 = Thread(target=high_right)


    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t4.setDaemon(True)
    t5.setDaemon(True)
    t6.setDaemon(True)
    t7.setDaemon(True)
    t8.setDaemon(True)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()

    
    while True:
        if kb.read_key() == "esc":
            break
        else:
            continue
    dType.DisconnectDobot(api)
