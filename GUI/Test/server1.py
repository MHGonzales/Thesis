# Welcome to PyShine
# In this video server is receiving video from clients and also record them with any names
# Lets import the libraries
import socket, cv2, pickle, struct
import imutils
import threading
import pyshine as ps # pip install pyshine
import cv2
from datetime import datetime

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)


def show_client(addr,client_socket):
    fourcc =0x7634706d 
    now = datetime.now()
    time_str = now.strftime("%d%m%Y%H%M%S")
    time_name = '_Rec_'+time_str+'.mp4'
    fps = 30
    frame_shape = False
    try:
        print('CLIENT {} CONNECTED!'.format(addr))
        if client_socket: # if a client socket exists
            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024) # 4K
                    if not packet: break
                    data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]
                
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                text  =  f"CLIENT: {addr}"
                time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                frame =  ps.putBText(frame,time_now,10,10,vspace=10,hspace=1,font_scale=0.7, background_RGB=(255,0,0),text_RGB=(255,250,250))
                
                if not frame_shape:
                    
                    video_file_name  = str(addr) + time_name
                    out = cv2.VideoWriter(video_file_name, fourcc, fps, (frame.shape[1], frame.shape[0]), True)
                    frame_shape = True
                out.write(frame)
                cv2.imshow(f"FROM {addr}",frame)
                key = cv2.waitKey(1) & 0xFF
                if key  == ord('q'):
                    break
            client_socket.close()
    except Exception as e:
        print(f"CLINET {addr} DISCONNECTED")
        pass
		
while True:
	client_socket,addr = server_socket.accept()
	thread = threading.Thread(target=show_client, args=(addr,client_socket))
	thread.start()
	print("TOTAL CLIENTS ",threading.activeCount() - 1)
	

