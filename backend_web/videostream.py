from flask import Flask, Response, render_template
import cv2
import os

os.system("start \"\" http://1.tcp.ap.ngrok.io:21694")

app = Flask(__name__)
video = cv2.VideoCapture(2)
video2 = cv2.VideoCapture(3)
bg = cv2.imread('WEB.png', cv2.IMREAD_COLOR) 

@app.route("/")
def index():
    return render_template('web.html')

def gen(video2):
    while True:
        success, img = video2.read()
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),20] 
        ret, jpeg = cv2.imencode('.jpg', img, encode_param)
        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen(video):
    while True:
        success2, img2 = video.read()
        new_img2 = cv2.resize(img2, (588, 324))
        encode_param2=[int(cv2.IMWRITE_JPEG_QUALITY),20] 
        ret, jpeg = cv2.imencode('.jpg', new_img2, encode_param2)
        frame1 = jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n\r\n')

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

@app.route('/CONSOLE')
def control():
    return render_template('console.html')

@app.route('/MAIN')
def allview():
    return render_template('frame.html')

@app.route('/HEADER')
def ahdr():
    return render_template('header.html')

@app.route('/CLICK')
def clk():
    return render_template('clicked.html')

if __name__ == '__main__':
    app.run(host='localhost', port=2037, threaded=True)
