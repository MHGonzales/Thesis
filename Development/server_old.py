import socket
import DobotDllType as dType
import roboticstoolbox


def server_program():
    # get the hostname
    host = '127.0.0.1'
    port = 5050   # initiate port no above 1024

    server_socket = socket.socket()  
    
    server_socket.bind((host, port))  
    server_socket.listen(2)

    conn, address = server_socket.accept()  
    print("Connection from: " + str(address))

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()

        if data == "a":
            dType.SetPTPCmdEx(api, 2, 200,  0,  0, current_pose[3], 1) # send message
            print("Robot go forward")
        elif data == "w":
            print("Robot go up")
        elif data == "s":
            print("Robot go down")
        elif data == "d":
            dType.SetPTPCmdEx(api, 2, 79,  0,  0, current_pose[3], 1)
            print("Robot go backward")
        elif data == "esc":
            print("Controller left the chat")
            break
        else:
            print("No data received")
            continue

    conn.close()  # close the connection


if __name__ == '__main__':
    CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
    
    api = dType.load()
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])

    current_pose = dType.GetPose(api)

    server_program()