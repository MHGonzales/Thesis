client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '0.tcp.ap.ngrok.io'
# Standard loopback interface address (localhost)
port = 16424
# Port to listen on (non-privileged ports are > 1023)
# now connect to the web server on the specified port number
client_socket.connect((host_ip,port)) 