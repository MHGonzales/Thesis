import socket,cv2, pickle,struct
import pyshine as ps # pip install pyshine
import imutils # pip install imutils

vid = cv2.VideoCapture(0)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '1.tcp.ap.ngrok.io' # ngrok

port = 21694 # ngrok port
client_socket.connect((host_ip,port))

if client_socket: 
	while (vid.isOpened()):
		try:
			img, frame = vid.read()
			frame = imutils.resize(frame,width=720)
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			client_socket.sendall(message)
			cv2.imshow("LAB CAMERA",frame)
			key = cv2.waitKey(10) & 0xFF
			if key == 27:
				client_socket.close()
		except:
			print('VIDEO FINISHED!')
			break

