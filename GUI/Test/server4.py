import struct
import pickle
import socket
import time

import cv2

# Define server socket. For testing, the IPV4 address works fine.
ip, port = 'localhost', 5050
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()
print(f'Server listening on {ip}')
client, address = server.accept()
print(f'Connection made with {address}\n')

# This is the number of bytes that represent an integer
bytes_length = struct.calcsize('q')
data = b''

while True:
    # The first 8 bytes ('q' data type) represent an integer. This integer is the size of the serialized frame object.
    # We need to make sure the data array has at least these 8 bytes, so that we know when to end the second while loop.
    start = time.perf_counter()
    while len(data) < bytes_length:
        data += client.recv(1024*2)
    frame_size_bytes = data[:bytes_length]
    frame_size = struct.unpack('q', frame_size_bytes)[0]

    # Keep adding the frame data until the known size is reached. There may be excess bytes that carry over, but the
    # first while loop expects this and takes care of it.
    frame_data = data[bytes_length:]
    while len(frame_data) < frame_size:
        frame_data += client.recv(1024*2)
    end = time.perf_counter()

    # Some measurements
    print(f'Total size received: {len(frame_data) + bytes_length:,} bytes')
    print(f'Time to receive: {end - start} seconds')
    print(f'Receive rate: {(len(frame_data) + bytes_length)/(end - start):,} bytes/second\n')

    # Get the frame object, resize it, then show it.
    frame = pickle.loads(frame_data[:frame_size])
    # height, width, _ = frame.shape
    resized = cv2.resize(frame, (400, 360))
    data = frame_data[frame_size:]  # excess data
    cv2.imshow('Received Video', resized)


    if cv2.waitKey(1) == 27:
        server.close()
        break