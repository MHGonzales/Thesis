import threading
import cv2

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

if __name__=='__main__':
    cam_list=[0, 1]
    threads = []
    for i, cam in enumerate(cam_list):
        thread1 = camThread("Robot Arm", i)
        thread2 = camThread("Lab View", i)
        threads.append(thread1)
        threads.append(thread2)
    for i in threads:
        i.start()