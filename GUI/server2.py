import socket
import cv2
import pickle
import struct
import imutils

# socket: To get socket module from python
# cv2: To import Computer Vision module from python
# pickle: for serializing and de-serializing python object structures.
# struct: to convert native Python data types such as strings and numbers into a string of bytes and vice versa
# imutils: Image processing operations

# Server socket
# create an INET, STREAMING socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


host_name  = socket.gethostname()
HOST = "localhost"
print('HOST IP:',HOST)
PORT = 80 #change from ngrok

socket_address = (HOST,PORT)
print('Socket created')
# bind the socket to the host. 
#The values passed to bind() depend on the address family of the socket
server_socket.bind((socket_address))
print('Socket bind complete')
#listen() enables a server to accept() connections
#listen() has a backlog parameter. 
#It specifies the number of unaccepted connections that the system will allow before refusing new connections.
server_socket.listen(5)
print('Socket now listening')


while True:
    client_socket,addr = server_socket.accept()
    print('Connection from: ', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while (vid.isOpened()):
            img, frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv2.imshow('Sending...', frame)
            key = cv2.waitKey(10)
            if key == 27: # exit on ESC
                client_socket.close()


