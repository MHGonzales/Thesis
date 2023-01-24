#importing library

import socket
import numpy as np
import cv2 as cv
import threading

# client program socket to connect to the server program
skt = socket.socket()
skt.bind(("", 4321))  # empty means local system
server_ip = 'localhost'
server_port = 1234

skt.connect((server_ip, int(server_port))) 
skt.send(b"connected")  # sending string as data
camera = cv.VideoCapture(1) # starting the camera
camera1 = cv.VideoCapture(2) # starting the camera

# function for cleint to work as receiver
def receiver():
    framesLost = 0
    print("Entered")
    while True:
        framesLost += 1 # counting frame
        data = skt.recv(100000000)  # receiving data with the size limit
        if(data == b'finished'): # to stop receiving and stop camera
            print("Finished")
            camera.release()
            skt.close()
        else:  # converting the byte data into numpy array
            photo =  np.frombuffer(data, dtype=np.uint8)
            if len(photo) == 640*480*3: # changing the array shape and getting the video
                cv.imshow('Arm View', photo.reshape(480, 640, 3))
                if cv.waitKey(1) == 27: # camera closing condition
                    skt.send(b'finished')
                    camera.release()
                    cv.destroyAllWindows()
                    break

#def receiver2():
#    framesLost1 = 0
#    print("Entered - 1")
#    while True:
#        framesLost1 += 1 # counting frame
#        data1 = skt.recv(100000000)  # receiving data with the size limit
#        if(data1 == b'finished'): # to stop receiving and stop camera
#            print("Finished")
#            camera1.release()
#            skt.close()
#        else:  # converting the byte data into numpy array
#            photo1 =  np.frombuffer(data1, dtype=np.uint8)
#            if len(photo1) == 640*480*3: # changing the array shape and getting the video
#                cv.imshow('Lab View', photo1.reshape(480, 640, 3))
#                if cv.waitKey(1) == 27: # camera closing condition
#                    skt.send(b'finished')
#                    camera1.release()
#                    cv.destroyAllWindows()
#                    break


# threads to run both the functions
threading.Thread(target=receiver).start()
#threading.Thread(target=receiver2).start()