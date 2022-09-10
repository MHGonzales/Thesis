import keyboard
import socket

def client_program():
    host = '127.0.0.1'
    port = 5050 

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server


    while True:
        
        if keyboard.read_key() == "a":
            message = "a"
            client_socket.send(message.encode())  # send message
        elif keyboard.read_key() == "w":
            message = "w"
            client_socket.send(message.encode())
        elif keyboard.read_key() == "s":
            message = "s"
            client_socket.send(message.encode())
        elif keyboard.read_key() == "d":
            message = "d"
            client_socket.send(message.encode())
        elif keyboard.read_key() == 'esc':
            message = "esc"
            client_socket.send(message.encode())
            break
        else:
            continue
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()


        
