import pickle
import socket
import struct
import time

import cv2

# Define client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('1.tcp.ap.ngrok.io', 21694))

# Define VideoCapture object
# There must be a camera plugged up. Play with the first argument of the VideoCapture declaration.
# The codec is provided for faster launch.
width, height = 256, 144 # 1920 x 1080 is too much
cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

while True:
    # Capture frame
    _, frame = cam.read()

    # Serialize the frame, then send it to the server socket.
    # It's necessary to include the length of the byte stream at the beginning in order for the server to know when to
    # stop receiving.
    frame_bytes = pickle.dumps(frame)
    send_bytes = struct.pack('q', len(frame_bytes)) + frame_bytes
    start = time.perf_counter()
    client.sendall(send_bytes)
    end = time.perf_counter()

    # Some measurements
    print(f'Total size sent: {len(send_bytes):,} bytes')
    print(f'Time to send: {end - start} seconds')
    print(f'Send rate: {len(send_bytes)/(end - start):,} bytes/second\n')

    # Show the frame
    cv2.imshow('Sending Video', frame)

    if cv2.waitKey(1) == 27:
        client.close()
        break