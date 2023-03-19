from socket import socket, AF_INET, SOCK_STREAM

#Criação de um socket generico
myClientSocket = socket(AF_INET, SOCK_STREAM)

myClientSocket.connect(('127.0.0.1', 9090))
while True:
    msg = input('Manda tua braba: ')
    myClientSocket.send(msg.encode())
    data = myClientSocket.recv(2048)
    print(data.decode())