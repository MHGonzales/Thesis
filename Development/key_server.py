# Imports
import socket
from _thread import *
import Queue
import DobotDllType as dType
import roboticstoolbox

# Declarations
host = '127.0.0.1'
port = 1233
ThreadCount = 0

def client_handler(connection):
    connection.send(str.encode('You are now connected to the replay server... Type BYE to stop'))
    while True:
        data = connection.recv(2048).decode()

        if data == "a":
            #dType.SetPTPCmdEx(api, 2, 200,  0,  0, current_pose[3], 1) # send message
            print("Robot go forward")
        elif data == "w":
            print("Robot go up")
        elif data == "s":
            print("Robot go down")
        elif data == "d":
            #dType.SetPTPCmdEx(api, 2, 79,  0,  0, current_pose[3], 1)
            print("Robot go backward")
        elif data == "esc":
            print("Controller left the chat")
            break
        else:
            print("No data received")
            continue
    connection.close()

def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (Client, ))

def start_server(host, port):
    ServerSocket = socket.socket()
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