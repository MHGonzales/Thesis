# importing required libraries
import cv2  # OpenCV library 
import time # time library
from threading import Thread # library for multi-threading
# defining a helper class for implementing multi-threading 
class WebcamStream :
    # initialization method 
    def __init__(self, stream_id=0):
        self.stream_id = stream_id # default is 0 for main camera 
        
        # opening video capture stream 
        self.vcap      = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False :
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5)) # hardware fps
        print("FPS of input stream: {}".format(fps_input_stream))
            
        # reading a single frame from vcap stream for initializing 
        self.grabbed , self.frame = self.vcap.read() 
        if self.grabbed is False :
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is initialized to False 
        self.stopped = True
        # thread instantiation  
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True # daemon threads run in background 
        
    # method to start thread 
    def start(self):
        self.stopped = False
        self.t.start()
    # method passed to thread to read next available frame  
    def update(self):
        while True :
            if self.stopped is True :
                break
            self.grabbed , self.frame = self.vcap.read()
            if self.grabbed is False :
                print('[Exiting] No more frames to read')
                self.stopped = True
                break 
        self.vcap.release()
    # method to return latest read frame 
    def read(self):
        return self.frame
    # method to stop reading frames 
    def stop(self):
        self.stopped = True
    # initializing and starting multi-threaded webcam input stream 
webcam_stream = WebcamStream(stream_id=0) # 0 id for main camera
webcam_stream1 = WebcamStream(stream_id=1) 
webcam_stream.start()
webcam_stream1.start()
# processing frames in input stream
num_frames_processed = 0 
start = time.time()
while True :
    if webcam_stream.stopped is True :
        break
    else :
        frame = webcam_stream.read()
    if webcam_stream1.stopped is True :
        break
    else :
        frame1 = webcam_stream1.read()
    # adding a delay for simulating video processing time 
    delay = 0.03 # delay value in seconds
    time.sleep(delay) 
    num_frames_processed += 1
    # displaying frame 
    cv2.imshow('received 1' , frame)
    cv2.imshow('received 2' , frame1)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
end = time.time()
webcam_stream.stop() # stop the webcam stream
webcam_stream1.stop()
# printing time elapsed and fps 
elapsed = end-start
fps = num_frames_processed/elapsed 
print("FPS: {} , Elapsed Time: {} ".format(fps, elapsed))
# closing all windows 
cv2.destroyAllWindows()