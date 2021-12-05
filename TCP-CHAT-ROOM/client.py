import socket, threading

def send():
    while True:
        msg = input('nMe > ').encode('utf-8')
        cli_sock.send(msg)

def receive():
    while True:
        sen_name = cli_sock.recv(1024).decode('utf-8')
        data = cli_sock.recv(1024).decode('utf-8')

        print('n' + str(sen_name) + ' > ' + str(data))

if __name__ == "__main__":   
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = '52.220.121.212' #change when starting new ngrok tunnel
    PORT = 18465    #change when starting new ngrok tunnel
    cli_sock.connect((HOST, PORT))     
    print('Connected to remote host...')
    uname = input('Enter your name to enter the chat > ').encode('utf-8')
    cli_sock.send(uname)

    thread_send = threading.Thread(target = send)
    thread_send.start()

    thread_receive = threading.Thread(target = receive)
    thread_receive.start()