import cv2
import io
import socket
import struct
import time
import pickle
import numpy as np
import imutils

host = '13.229.3.203'
port = 15290

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # client_socket.connect(('0.tcp.ngrok.io', 19194))

cam1 = cv2.VideoCapture(0)
cam = cv2.VideoCapture(1)
img_counter = 0

#encode to jpeg format
#encode param image quality 0 to 100. default:95
#if you want to shrink data size, choose low image quality.
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),100]

while True:
    ret1, frame1 = cam1.read()
    ret, frame = cam.read()
    # 影像縮放
    frame1 = imutils.resize(frame1, width=480)
    frame = imutils.resize(frame, width=480)
    # 鏡像
    frame1 = cv2.flip(frame1,180)
    frame = cv2.flip(frame,180)
    
    result1, image1 = cv2.imencode('.jpg', frame1, encode_param)
    result, image = cv2.imencode('.jpg', frame, encode_param)
    data1 = pickle.dumps(image1, 0)
    data = pickle.dumps(image, 0)
    size = len(data)

    if img_counter%10==0:
        client_socket.sendall(struct.pack(">L", size) + data)
        cv2.imshow('Arm View',frame1)
        cv2.imshow('Lab View',frame)
        
    img_counter += 1

    # 若按下 q 鍵則離開迴圈
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()