import socket


def server_program():
    # get the hostname
    host = '127.0.0.1'
    port = 5050   # initiate port no above 1024

    server_socket = socket.socket()  
    
    server_socket.bind((host, port))  
    server_socket.listen(2)

    conn, address = server_socket.accept()  
    print("Connection from: " + str(address))

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()

        if data == "a":
            print("Robot go left") # send message
        elif data == "w":
            print("Robot go up")
        elif data == "s":
            print("Robot go down")
        elif data == "d":
            print("Robot go right")
        elif data == "esc":
            print("Controller left the chat")
            break
        else:
            print("No data received")
            continue

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()