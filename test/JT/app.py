
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
 
message = ""  # Define message as a global variable

@app.route('/')
def index():
    return render_template('index.html')
 
@socketio.on('message')
def handle_message(msg):
    global message  # Use the global keyword to access the global message variable
    message = msg
    print('received message: ' + message)
    send(message, broadcast=True) 

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host='localhost', port=2038)

    