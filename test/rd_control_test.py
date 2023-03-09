import time as tm
from threading import Thread

import xlwings as xw
import keyboard as kb
import roboticstoolbox as rtb
from spatialmath import SE3
from numpy import pi

from utilities_test import Dobot
from utilities_test.dobot import DobotDllType as dType
from serial import Serial as sr

print("Import Success !!")

ad = sr('COM4',9600)
rb = Dobot()

#this is for delta movement and robot movement
def robot(dx,dy,dz,nx,ny,nz,roll:str = "0",grip:str = "90"):
    global j4,j5,j6,l
    #calculate inverse kinematics for position
    if l==1:
        Tf = SE3.Trans((nx+107)/1000 ,ny/1000 ,nz/1000) *SE3.OA([1,  0, 0], [0, 0, -1])
        sol = rb.ikine_LMS(Tf,rb.qz)
        qn =sol.q*180/pi
        j4 = 90
        j5= 0
        j6 = 0
        gr =grip
        pos_wrist = str(str(j4) +','+ str(j5) + ','+ str(j6) +','+ str(gr) +',')
    else:
        Tf = SE3.Trans((nx+102)/1000 ,ny/1000 ,nz/1000) *SE3.OA([0,  0, 1], [0, 1, 0])
        sol = rb.ikine_LMS(Tf,rb.qz)
        qn =sol.q*180/pi
        j4 = int(qn[4])
        j5= roll
        j6= 90
        gr=grip
        pos_wrist = str(str(j4) +','+ str(j5) + ','+ str(j6) +','+ str(gr) +',')
    ad.write(pos_wrist.encode())   
    dType.SetPTPCmdEx(api, 7, dx,  dy,  dz, 0, 1)

    
    #send serial to arduino

def roll():
    while True:
        if kb.read_key() == "r":
            roll = input("Roll Degrees: ")
            current_pose= dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
            delta(ox,oy,oz,nx,ny,nz,roll)
        tm.sleep(0.25) 


#move forward
def forward():
    global table,i,j,k,l
    while True:
        if kb.read_key() =="z":
            current_pose = dType.GetPose(api)
            
            if l==1:
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]-5
                robot(0,0,-5,nx,ny,nz)
            else:
                nx,ny,nz = current_pose[0]+10,current_pose[1],current_pose[2]
                robot(10,0,0,nx,ny,nz)
        tm.sleep(0.1)

def backward():
    global table,i,j,k,l
    while True:
        if kb.read_key() =="x":
            current_pose = dType.GetPose(api)
            #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
            if l==1: 
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]+5
                robot(0,0,5,nx,ny,nz)
            else:
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                nx,ny,nz = current_pose[0]-10,current_pose[1],current_pose[2]
                robot(-10,0,0,nx,ny,nz)
        tm.sleep(0.1)
    
def power():
    global table,i,j,k,l
    while True:
        if kb.read_key() == "p":
            ws = xw.Book("coordinates_py.xlsx").sheets['Power Supply']
            table = ws.range("A1:C5").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =125, table[0][1],table[0][2]
            i=0
            j=1
            k=2
            l=0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def low_mid():
    global table,i,j,k,l

    while True:
        if kb.read_key() == "k":
            ws = xw.Book("coordinates_py.xlsx").sheets['Middle Lower Load']
            table = ws.range("A1:I2").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =140, table[0][1],table[0][2]
            i=0
            j=1
            k=2
            l=0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def switches():
    global table,i,j,k,l
    while True:
        if kb.read_key() == "j":
            ws = xw.Book("coordinates_py.xlsx").sheets['Switches']
            table = ws.range("A1:AJ2").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =140, table[0][1],table[0][2]
            i=0
            j=1
            k=2
            l=0
            delta(ox,oy,oz,nx,ny,nz)
            tm.sleep(0.25)

def high_mid():
    global table,i,j,k,l
    while True:
        if kb.read_key() == "i":
            ws = xw.Book("coordinates_py.xlsx").sheets['Middle Upper Load']
            table = ws.range("A1:I2").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =140, table[0][1],table[0][2]
            i=0
            j=1
            k=2
            l=0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def high_right():
    global table,i,j,k,l
    while True:
        if kb.read_key() == "o":
            ws = xw.Book("coordinates_py.xlsx").sheets['Right Upper Load']
            table = ws.range("A1:C2").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =120, table[0][1],table[0][2]
            i=0
            j=1
            k=2
            l=0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def low_right():
    global table,i,j,k,l
    while True:
        if kb.read_key() == "l":
            ws = xw.Book("coordinates_py.xlsx").sheets['Data Acquisition']
            table = ws.range("A1:L4").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =140, table[0][1],table[0][2]
            i=0
            j=1
            k=2
            l=0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def pickup_mode():
    global table,i,j,k,l
    while True:
        if kb.read_key() == "u":
            ws = xw.Book("coordinates_py.xlsx").sheets['Wires']
            table = ws.range("A1:R6").value
            current_pose = dType.GetPose(api)
            if l==0:
                ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
                nx,ny,nz =50,151.6, 150
                i=0
                j=1
                k=2
                l = 1
                delta(ox,oy,oz,nx,ny,nz)
            else:
                l = 0
                robot(0,0,0,roll=0) 
        tm.sleep(0.25)
    return
    
def home_position():
    while True:
        global i,j,k,l
        if kb.read_key()=="h":
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz = 100, 0, 0
            i=0
            j=1
            k=2
            l = 0
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0)
#this is for delta calculation
def delta(ox,oy,oz,nx,ny,nz,roll:str = "0",grip:str = "90"):
    
    dy = ny-oy
    dz = nz - oz
    dx = nx-ox
    print("Delta x: ",dx,"Delat y: ",dy ," Delta z: ",dz )
    robot(dx,dy,dz,nx,ny,nz,roll,grip )
    return

def left():
    global i,table,j,k,l
    while True:
        if kb.read_key() == "a":
            current_pose = dType.GetPose(api)
            #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
            if l==1:
                ox,oy,oz =table[i][j],table[i][k],current_pose[2]
                j-=3
                k-=3
                nx,ny,nz = table[i][j],table[i][k],current_pose[2]
            else:
                ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                j-=3
                k-=3
                nx,ny,nz = current_pose[0], table[i][j],table[i][k]
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def right():
    global i,table,j,k,l
    while True:
        if kb.read_key() == "d":
            current_pose = dType.GetPose(api)
            #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
            if l==1:
                ox,oy,oz =table[i][j],table[i][k],current_pose[2]
                j+=3
                k+=3
                nx,ny,nz = table[i][j],table[i][k],current_pose[2]
            else:
                ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                j+=3
                k+=3
                nx,ny,nz = current_pose[0], table[i][j],table[i][k]
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def up():
    global i,table,j,k,l
    while True:
        if kb.read_key() == "w":
            current_pose = dType.GetPose(api)
            #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
            
            if l==1:
                ox,oy,oz =table[i][j],table[i][k],current_pose[2]
                i-=1
                nx,ny,nz = table[i][j],table[i][k],current_pose[2]
            else:
                ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                i-=1
                nx,ny,nz = current_pose[0], table[i][j],table[i][k]
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def down():
    global i,table,j,k,l
    while True:
        if kb.read_key() == "s":
            current_pose = dType.GetPose(api)
            if l==1:
                ox,oy,oz =table[i][j],table[i][k],current_pose[2]
                i+=1
                nx,ny,nz = table[i][j],table[i][k],current_pose[2]
            else:
                ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                i+=1
                nx,ny,nz = current_pose[0],table[i][j],table[i][k]
            delta(ox,oy,oz,nx,ny,nz)
        tm.sleep(0.25)

def precision_left():
    global i,table,j,k,l
    while True:
        if kb.read_key() == "left":
            current_pose = dType.GetPose(api)
            #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
            if l==1:
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
                robot(0,1,0,nx,ny,nz)
            else:
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
                robot(0,1,0,nx,ny,nz)
        tm.sleep(0.25)

def precision_right():
    global i,table,j,k,l
    while True:
        if kb.read_key() == "right":
            current_pose = dType.GetPose(api)
            #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
            if l==1:
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
                robot(0,-1,0,nx,ny,nz)
            else:
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
                robot(0,-1,0,nx,ny,nz)
        tm.sleep(0.25)

def precision_up():
    global i,table,j,k,l
    while True:
        if kb.read_key() == "up":
            current_pose = dType.GetPose(api)        
            if l==1:
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
                robot(1,0,0,nx,ny,nz)
            else:
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
                robot(0,0,1,nx,ny,nz)
        tm.sleep(0.25)

def precision_down():
    global i,table,j,k,l
    while True:
        if kb.read_key() == "down":
            current_pose = dType.GetPose(api)
            if l==1:
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
                robot(-1,0,0,nx,ny,nz)
            else:
                nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
                robot(0,0,-1,nx,ny,nz)
        tm.sleep(0.25)

def start_threads():
    t1 = Thread(target=left,daemon=True)
    t2 = Thread(target=right,daemon=True)
    t3 = Thread(target=up,daemon=True)
    t4 = Thread(target=down,daemon=True)
    t5= Thread(target=low_mid,daemon=True)
    t6 = Thread(target=low_right,daemon=True)
    t7 = Thread(target=high_mid,daemon=True)
    t8 = Thread(target=high_right,daemon=True)
    t9 = Thread(target=switches,daemon=True)
    t10 = Thread(target=forward,daemon=True)
    t11 = Thread(target=backward,daemon=True)
    t12 = Thread(target = power,daemon=True)
    t13 = Thread(target = roll,daemon=True)
    t14 = Thread(target = pickup_mode,daemon=True)
    t15 = Thread(target = home_position,daemon=True)
    t16 = Thread(target = precision_down,daemon=True)
    t17 = Thread(target = precision_left,daemon=True)
    t18 = Thread(target = precision_right,daemon=True)
    t19 = Thread(target = precision_up,daemon=True)
    


    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()
    t17.start()
    t18.start()
    t19.start()

    print("Threads Initialized....")

    return


if __name__ == "__main__":

    i,l = 0
    j = 1
    k = 2
    api = dType.load()
    dType.ConnectDobot(api, "", 115200)
    #dType.SetIOMultiplexing(api, 4, 2, 1)
    #global current_pose
    current_pose=dType.GetPose(api)
    dType.SetPTPCmd(api,2,100,0,0,0,1) 
    
    print(" Initializing Arduino Serial Connection")
    
    tm.sleep(5)
    print("Arduino Connected")
    print("Initializing threads....") 
    
    start_threads()

    print("Robot Control Active")

    
    while True:
        if kb.read_key() == "esc":
            break
        else:
            continue
    dType.DisconnectDobot(api)
