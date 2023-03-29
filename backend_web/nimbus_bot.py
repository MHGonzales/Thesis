from flask import Flask, Response, render_template, request
import cv2, datetime
import os

import time as tm
from threading import Thread
from flask_socketio import SocketIO, send, emit

import xlwings as xw
import keyboard as kb
import roboticstoolbox as rtb
from spatialmath import SE3
from numpy import pi

from utilities_test import Dobot
from utilities_test.dobot import DobotDllType as dType
from serial import Serial as sr

print("Import Success !!")

ad = sr('COM4',9600) #Nano com
rb = Dobot()

#os.system("start \"\" http://1.tcp.ap.ngrok.io:21694")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
 
message = " "  # Define message as a global variable
_roll = " "

video = cv2.VideoCapture(2)
video2 = cv2.VideoCapture(1)
bg = cv2.imread('WEB.png', cv2.IMREAD_COLOR) 

@app.route("/")
def index():
    return render_template('web.html')

def gen(video2):
    while True:
        success, frame = video2.read()
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),20] 
        font = cv2.FONT_HERSHEY_PLAIN
        time = str(datetime.datetime.now())
        frame = cv2.putText(frame, time, (10,30), font,1, (255,122,160), 2 , cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', frame, encode_param) 
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen(video):
    while True:
        success2, frame1 = video.read()
        frame1 = cv2.resize(frame1, (588, 324))
        encode_param2=[int(cv2.IMWRITE_JPEG_QUALITY),20] 
        font = cv2.FONT_HERSHEY_PLAIN
        time = str(datetime.datetime.now())
        frame1 = cv2.putText(frame1, time, (10,30), font,1, (255,122,160), 2 , cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', frame1, encode_param2)
        frame1 = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n\r\n')

def robot(dx,dy,dz,nx,ny,nz,roll:str = "0",grip:str = "90"):
    global j4,j5,j6,l
    #calculate inverse kinematics for position
    if l==1:
        Tf = SE3.Trans((nx+65)/1000 ,ny/1000 ,nz/1000) *SE3.OA([1,  0, 0], [0, -1, 0])
        sol = rb.ikine_LMS(Tf,rb.qz)
        qn =sol.q*180/pi
        j4 = float(qn[4])+90
        j5= 0
        j6 = float(qn[5])+90
        gr =grip
        pos_wrist = str(str(j4) +','+ str(j5) + ','+ str(j6) +','+ str(gr) +',')
    else:
        Tf = SE3.Trans((nx+65)/1000 ,ny/1000 ,nz/1000) *SE3.OA([0,  0, 1], [0, -1, 0])
        sol = rb.ikine_LMS(Tf,rb.qz)
        qn =sol.q*180/pi
        j4 = float(qn[4])+90
        j5= roll
        j6= float(qn[5])+90
        gr=grip
        pos_wrist = str(str(j4) +','+ str(j5) + ','+ str(j6) +','+ str(gr) +',')
    ad.write(pos_wrist.encode())   
    dType.SetPTPCmdEx(api, 7, dx,  dy,  dz, 0, 1)

    
    #send serial to arduino

def roll():
    global _roll
    while True:
        if _roll[0] == "roll":
            
            roll = float(_roll[1])
            roll_out = (roll/1.2)*(300/100)*(200*1.8/15)
            print("Received Roll")
            current_pose= dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]
            print("Rolling")
            delta(ox,oy,oz,nx,ny,nz,roll,roll_out)
            _roll[0]=""
        tm.sleep(0.25) 


#move forward
def forward():
    global table,i,j,k,l,message,f
    while True:
        if f == 1:
            if message == "z" or message == "Z":
                current_pose = dType.GetPose(api)
                
                if l==1:
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]-10
                    robot(0,0,-10,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0]+10,current_pose[1],current_pose[2]
                    robot(10,0,0,nx,ny,nz)
                message=""
        elif f == 2:
            if message == "z" or message == "Z":
                current_pose = dType.GetPose(api)
                
                if l==1:
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]-5
                    robot(0,0,-5,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0]+5,current_pose[1],current_pose[2]
                    robot(5,0,0,nx,ny,nz)
                message=""
        elif f == 3:
            if message == "z" or message == "Z":
                current_pose = dType.GetPose(api)
                
                if l==1:
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]-1
                    robot(0,0,-1,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0]+1,current_pose[1],current_pose[2]
                    robot(1,0,0,nx,ny,nz)
                message=""
        tm.sleep(0.1)

def backward():
    global table,i,j,k,l,message,f
    while True:
        if f == 1:
            if message == "x" or message == "X":
                current_pose = dType.GetPose(api)
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                if l==1: 
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]+10
                    robot(0,0,10,nx,ny,nz)
                else:
                    #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                    nx,ny,nz = current_pose[0]-10,current_pose[1],current_pose[2]
                    robot(-10,0,0,nx,ny,nz)
                message=""
        elif f == 2:
            if message == "x" or message == "X":
                current_pose = dType.GetPose(api)
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                if l==1: 
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]+5
                    robot(0,0,5,nx,ny,nz)
                else:
                    #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                    nx,ny,nz = current_pose[0]-5,current_pose[1],current_pose[2]
                    robot(-5,0,0,nx,ny,nz)
                message=""
        elif f == 3:
            if message == "x" or message == "X":
                current_pose = dType.GetPose(api)
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                if l==1: 
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]+1
                    robot(0,0,1,nx,ny,nz)
                else:
                    #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                    nx,ny,nz = current_pose[0]-1,current_pose[1],current_pose[2]
                    robot(-1,0,0,nx,ny,nz)
                message=""
        tm.sleep(0.1)
    
def power():
    global table,i,j,k,l,message
    while True:
        if message == "p" or message == "P":
            ws = xw.Book("coordinates_py.xlsx").sheets['Power Supply']
            table = ws.range("A1:C5").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =100, table[0][1],table[0][2]
            i=0
            j=1
            k=2
            l=0
            delta(ox,oy,oz,nx,ny,nz)
            message=""
        tm.sleep(0.25)

def low_mid():
    global table,i,j,k,l,message
    while True:
        if message == "k" or message == "K":
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
            message=""
        tm.sleep(0.25)

def switches():
    global table,i,j,k,l,message
    while True:
        if message == "j" or message == "J":
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
            message =""
            tm.sleep(0.25)

def high_mid():
    global table,i,j,k,l,message
    while True:
        if message == "i" or message == "I":
            ws = xw.Book("coordinates_py.xlsx").sheets['Middle Upper Load']
            table = ws.range("A1:I2").value
            current_pose = dType.GetPose(api)
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz =135, table[0][1],table[0][2]
            i=0
            j=1
            k=2
            l=0
            delta(ox,oy,oz,nx,ny,nz)
            message =""
        tm.sleep(0.25)

def high_right():
    global table,i,j,k,l,message
    while True:
        if message == "o" or message == "O":
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
            message =""
        tm.sleep(0.25)

def low_right():
    global table,i,j,k,l,message
    while True:
        if message == "l" or message == "L":
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
            message =""
        tm.sleep(0.25)

def pickup_mode():
    global table,i,j,k,l,message
    while True:
        if message == "u" or message == "U":
            ws = xw.Book("coordinates_py.xlsx").sheets['Wires']
            table = ws.range("A1:R6").value
            current_pose = dType.GetPose(api)
            if l==0:
                ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
                nx,ny,nz =150,150, 100
                i=0
                j=1
                k=2
                l = 1
                delta(ox,oy,oz,nx,ny,nz)
            else:
                l = 0
                robot(0,0,0,roll=0) 
            message =""
        tm.sleep(0.25)
    return
    
def home_position():
    while True:
        global i,j,k,l,message
        if message == "h" or message == "H" :
            ox,oy,oz = current_pose[0],current_pose[1],current_pose[2]
            nx,ny,nz = 100, 0, 0
            i=0
            j=1
            k=2
            l = 0
            dType.SetHOMECmd(api,0,1) 
            message =""
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
    global i,table,j,k,l,message,f
    while True:
        if f == 0:
            if message == "a" or message == "A" :
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
                message =""
        tm.sleep(0.25)

def right():
    global i,table,j,k,l,message,f
    while True:
        if f == 0:
            if message == "d" or message == "D" :
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
                message =""
        tm.sleep(0.25)

def up():
    global i,table,j,k,l,message,f
    while True:
        if f == 0:
            if message == "w" or message == "W":
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
                message=""
        tm.sleep(0.25)

def down():
    global i,table,j,k,l,message,f
    while True:
        if f == 0:
            if message == "s" or message == "S":
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
                message=""
        tm.sleep(0.25)

def precision_left():
    global i,table,j,k,l,message,f
    while True:
        if f == 1:
            if message == "a" or message == "A":
                current_pose = dType.GetPose(api)
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                if l==1:
                    nx,ny,nz = current_pose[0],current_pose[1]+10,current_pose[2]
                    robot(0,10,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1]+10,current_pose[2]
                    robot(0,10,0,nx,ny,nz)
                message=""
        elif f == 2:
            if message == "a" or message == "A":
                current_pose = dType.GetPose(api)
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                if l==1:
                    nx,ny,nz = current_pose[0],current_pose[1]+5,current_pose[2]
                    robot(0,5,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1]+5,current_pose[2]
                    robot(0,5,0,nx,ny,nz)
                message=""
        elif f == 3:
            if message == "a" or message == "A":
                current_pose = dType.GetPose(api)
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                if l==1:
                    nx,ny,nz = current_pose[0],current_pose[1]+1,current_pose[2]
                    robot(0,1,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1]+1,current_pose[2]
                    robot(0,1,0,nx,ny,nz)
                message=""
        tm.sleep(0.25)

def precision_right():
    global i,table,j,k,l,message,f
    while True:
        if f == 1:
            if message == "d" or message == "D":
                current_pose = dType.GetPose(api)
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                if l==1:
                    nx,ny,nz = current_pose[0],current_pose[1]-10,current_pose[2]
                    robot(0,-10,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1]-10,current_pose[2]
                    robot(0,-10,0,nx,ny,nz)
                message=""
        elif f == 2:
            if message == "d" or message == "D":
                current_pose = dType.GetPose(api)
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                if l==1:
                    nx,ny,nz = current_pose[0],current_pose[1]-5,current_pose[2]
                    robot(0,-5,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1]-5,current_pose[2]
                    robot(0,-5,0,nx,ny,nz)
                message=""
        elif f == 3:
            if message == "d" or message == "D":
                current_pose = dType.GetPose(api)
                #ox,oy,oz =current_pose[0], table[i][j],table[i][k]
                if l==1:
                    nx,ny,nz = current_pose[0],current_pose[1]-1,current_pose[2]
                    robot(0,-1,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1]-1,current_pose[2]
                    robot(0,-1,0,nx,ny,nz)
                message=""
        tm.sleep(0.25)

def precision_up():
    global i,table,j,k,l,message,f
    while True:
        if f == 1:
            if message == "w" or message == "W":
                current_pose = dType.GetPose(api)        
                if l==1:
                    nx,ny,nz = current_pose[0]+10,current_pose[1],+current_pose[2]
                    robot(10,0,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]+10
                    robot(0,0,10,nx,ny,nz)
                message=""
        elif f == 2:
            if message == "w" or message == "W":
                current_pose = dType.GetPose(api)        
                if l==1:
                    nx,ny,nz = current_pose[0]+5,current_pose[1],current_pose[2]
                    robot(5,0,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]+5
                    robot(0,0,5,nx,ny,nz)
                message=""
        elif f == 3:
            if message == "w" or message == "W":
                current_pose = dType.GetPose(api)        
                if l==1:
                    nx,ny,nz = current_pose[0]+1,current_pose[1],+current_pose[2]
                    robot(1,0,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]+1
                    robot(0,0,1,nx,ny,nz)
                message=""
        tm.sleep(0.25)

def precision_down():
    global i,table,j,k,l,message,f
    while True:
        if f == 1:
            if message == "s" or message == "S":
                current_pose = dType.GetPose(api)
                if l==1:
                    nx,ny,nz = current_pose[0]-10,current_pose[1],current_pose[2]
                    robot(-10,0,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]-10
                    robot(0,0,-10,nx,ny,nz)
                message=""
        elif f == 2:
            if message == "s" or message == "S":
                current_pose = dType.GetPose(api)
                if l==1:
                    nx,ny,nz = current_pose[0]-5,current_pose[1],current_pose[2]
                    robot(-5,0,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]-5
                    robot(0,0,-5,nx,ny,nz)
                message=""
        elif f == 3:
            if message == "s" or message == "S":
                current_pose = dType.GetPose(api)
                if l==1:
                    nx,ny,nz = current_pose[0]-1,current_pose[1],current_pose[2]
                    robot(-1,0,0,nx,ny,nz)
                else:
                    nx,ny,nz = current_pose[0],current_pose[1],current_pose[2]-1
                    robot(0,0,-1,nx,ny,nz)
                message=""
        tm.sleep(0.25)

def _precision_switch_module():
    global message,f
    while True:
        if message == "f" or message == "F":
            if f != 0:
                f = 0
                print("Switching to Module Control")  
            message=""

def _precision_switch_10mm():
    global message,f
    while True:
        if message == "c" or message == "C":
            if f != 1:
                f = 1
                print("Switching to 10mm Precision Control") 

def _precision_switch_5mm():
    global message,f
    while True:
        if message == "v" or message == "V":
            if f != 2:
                f = 2
                print("Switching to 5mm Precision Control") 

def _precision_switch_1mm():
    global message,f
    while True:
        if message == "b" or message == "B":
            if f != 3:
                f = 3
                print("Switching to 1mm Precision Control") 

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
    t20 = Thread(target = _precision_switch_module,daemon =True)
    t21 = Thread(target = _precision_switch_10mm,daemon =True)
    t22 = Thread(target = _precision_switch_5mm,daemon =True)
    t23 = Thread(target = _precision_switch_1mm,daemon =True)
    


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
    t20.start()
    t21.start()
    t22.start()
    t23.start()

    print("Threads Initialized....")

    return

@app.route('/ARM VIEW')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/LAB VIEW')
def video_feed2():
    global video2
    return Response(gen(video2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/CONSOLE')
def control():
    return render_template('console.html')

@app.route('/MAIN')
def allview():
    return render_template('frame.html')

@app.route('/HEADER')
def ahdr():
    return render_template('header.html')

@app.route('/CLICK')
def clk():
    return render_template('clicked.html')

@app.route('/NEWCLICK')
def nclick():
    return render_template('index.html')

@app.route('/ROLL')
def HTRL():
    return render_template('roll.html')

@socketio.on('message')
def handle_message(msg):
    global message  # Use the global keyword to access the global message variable
    message = msg
    print('received message: ' + message)
    send(message, broadcast=True) 

@socketio.on('roll')
def handle_message(rl):
    global _roll  # Use the global keyword to access the global message variable
    roll = 'roll:'+rl
    _roll = roll.split(':')
    print(roll)
    print(_roll[0])
    send(roll, broadcast=True) 

if __name__ == '__main__':
    i = 0
    j = 1
    k = 2
    l = 0
    f = 0
    api = dType.load()
    dType.ConnectDobot(api, "COM21", 115200) #Dobot COM
    #dType.SetIOMultiplexing(api, 4, 2, 1)
    #global current_pose
    current_pose=dType.GetPose(api)
    dType.SetHOMECmd(api,0,1) 
    
    print(" Initializing Arduino Serial Connection")
    
    tm.sleep(5)
    print("Arduino Connected")
    print("Initializing threads....") 
    
    start_threads()

    print("Robot Control Active")
    socketio.run(app,host='localhost', port=2037)

    print("Flask running")

    while True:
        if kb.read_key() == "esc":
            break
        else:
            continue
    dType.DisconnectDobot(api)
