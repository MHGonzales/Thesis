import cv2
import bz2, base64
import numpy as np
import threading

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create threads as follows
thread1 = camThread("Robot Arm", 3)
thread2 = camThread("Lab View", 0)

thread1.start()
thread2.start()
print()
print("Active threads", threading.active_count())





