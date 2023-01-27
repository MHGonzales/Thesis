from flask import Flask, Response
import cv2

app = Flask(__name__)
video = cv2.VideoCapture(3)
video2 = cv2.VideoCapture(0)

@app.route('/')
def index():
    return "Welcome to RIAL-3-2021-4"

def gen(video):
    while True:
        success, image = video.read()
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),20] 
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen(video2):
    while True:
        success2, image2 = video2.read()
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),40] 
        ret, jpeg = cv2.imencode('.jpg', image2, encode_param)
        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/ARM VIEW')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/LAB VIEW')
def video_feed2():
    global video2
    return Response(gen(video2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='localhost', port=2037, threaded=True)