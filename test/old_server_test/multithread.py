import cv2,datetime
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
        font = cv2.FONT_HERSHEY_PLAIN
        time = str(datetime.datetime.now())
        frame = cv2.putText(frame, time, (10,50), font,1, (0,0,0), 2 , cv2.LINE_AA)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create threads as follows
thread1 = camThread("Robot Arm", 2)
thread2 = camThread("Lab View", 3)

thread1.start()
thread2.start()
print()
print("Active threads", threading.active_count())


