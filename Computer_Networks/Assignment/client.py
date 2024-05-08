# 2018007956 김채아
import socket

HOST = '127.0.0.1'
PORT = 8080

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    message = input('Enter Message : ')
    if message == 'quit':
        break
    if not message :
        break
    client_socket.send(message.encode())

    data = client_socket.recv(1024)
    print('Received from the server :', repr(data.decode()))

client_socket.close()