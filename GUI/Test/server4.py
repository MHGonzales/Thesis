import socket
import numpy as np
import cv2 as cv
import threading

skt = socket.socket()
skt.bind(("localhost", 1234))
skt.listen()
session, address = skt.accept() #accepting request from any server
print(session.recv(4*1024)) 
camera = cv.VideoCapture(0) # staritng camera
camera1 = cv.VideoCapture(1) # staritng camera

def sender():
    while True:
        status, photo = camera.read()
        photo = cv.resize(photo, (640, 480))
        print(photo.shape)
        if status:
            session.send(np.ndarray.tobytes(photo))
        else: print("Could not get frame")
#def sender1():
    while True:
        status1, photo1 = camera1.read()
        photo1 = cv.resize(photo1, (640, 480))
        print(photo1.shape)
        if status1:    
            session.send(np.ndarray.tobytes(photo1))
        else: print("Could not get frame")

threading.Thread(target=sender).start()                
#threading.Thread(target=sender1).start()
