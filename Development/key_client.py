import keyboard
import socket

def client_program():
    host = '3.22.15.135'
    port = 16621

    client_socket = socket.socket()  # instantiate
    print('Waiting for connection')

    client_socket.connect((host, port))  # connect to the server
    print('Connected')
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
        print(message)
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()



