from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

#Criação de um socket generico
myServerSocket = socket(AF_INET, SOCK_STREAM)
print(f'Socket criado ...')

def HandlThreads(mclienteSock, mclienteAddr):
    while True:
        print(f'O cliente {mclienteSock} {mclienteAddr} enviou solocitação')

        data = mclienteSock.recv(2048)
        req = data.decode()

        print(req)

        clienteSock.send(req.encode())

myServerSocket.bind(('127.0.0.1',9090))
myServerSocket.listen()
while True:
    clienteSock, clienteAddr = myServerSocket.accept()

    Thread(target=HandlThreads, args=(clienteSock, clienteAddr) ).start()

    # print(f'O cliente {clienteSock} {clienteAddr} enviou solocitação')

    # data = clienteSock.recv(2048)
    # req = data.decode()

    # print(req)

    # clienteSock.send(req.encode())


