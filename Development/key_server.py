# Imports
import socket
from _thread import *
import Queue
import DobotDllType as dType
from spatialmath import SE3
import roboticstoolbox as rtb
from dobject import Dobot
import DobotDllType as dType
from math import pi

# Declarations
host = '127.0.0.1'
port = 5050
ThreadCount = 0

rb = Dobot()

x = 0.187
y = 0.0
z = 0.1

api = dType.load()
dType.ConnectDobot(api, "", 115200)

def jpos(x,y,z):
    
    Tf = SE3.Trans(x ,y ,z) *SE3.OA([0,  0, 1], [1, 0, 0])
    sol = rb.ikine_LMS(Tf,rb.qz)
    return sol.q*180/pi
    
def setje(x,y,z):
    #loop to move through qtraj
    
    current_pose=dType.GetPose(api)
    dType.SetPTPCmd(api,2,(x-0.040)*1000,y*1000,z*1000,current_pose[7],1) 
    #return
def d2p(deg:float):
    
    pwm = (deg/18)+2.5
    print(pwm)
    return pwm
def setjW(q:float):
    
    pwm = d2p(q)
    dType.SetIOPWM(api, 4, 50, pwm, 1)
    dType.dSleep(1500)
    
    return

def client_handler(connection):
    connection.send(str.encode('You are now connected to the replay server... Type BYE to stop'))
    
    x = 0.187
    y = 0.0
    z = 0.1
    
    while True:
        data = connection.recv(2048).decode()

        if data == "a":
            y=y+0.02
            print(f"x:{x},y:{y},z{z}") 
        elif data == "w":
            z=z+0.02
            print(f"x:{x},y:{y},z{z}") 
        elif data == "s":
            z=z-0.02
            print(f"x:{x},y:{y},z{z}") 
        elif data == "d":
            y=y-0.02
            print(f"x:{x},y:{y},z{z}") 
        elif data == "esc":
            print("Controller left the chat")
            break
        else:
            print("No data received")
            continue
        qn = jpos(x,y,z)
        setje(x,y,z)
        setjW(qn[4])

    connection.close()

def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (Client, ))

def start_server(host, port):
    ServerSocket = socket.socket()
    x = 0.187
    y = 0.0
    z = 0.1
    dType.SetIOMultiplexing(api, 4, 2, 1)
    qn = jpos(x,y,z)
    setje(x,y,z)
    setjW(qn[4])

    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print(f'Server is listing on the port {port}...')
    ServerSocket.listen()
    
    while True:
        accept_connections(ServerSocket)


start_server(host, port)

if __name__ == '__main__':
    CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
    
    api = dType.load()
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])

    current_pose = dType.GetPose(api)

    client_handler()