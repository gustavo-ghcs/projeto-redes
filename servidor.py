from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def handleRequest(clientSocket, clientAdress):
    clientRequest = clientSocket.recv(1024).decode()
    print(f"O cliente requisitou: {clientRequest}")

    print(clientRequest.split("\r\n")[0])


    header = clientRequest.split("\r\n")[0]
    print(header)
    searched_file = header.split()[1][1:]
    print(f"Header: {header}, Seached file: {searched_file}")
    extension = searched_file.split(".")[-1]

    is_binary = True
    if extension in ["html", "css", "js"]:
        is_binary = False

    try:
        if is_binary:
            file = open(searched_file, 'rb')
        else:
            file = open(searched_file, 'r', encoding='utf-8')
        file_content = file.read()
    except:
        msgHeader = 'HTTP/1.1 404 File not found \r\n' \
                    '\r\n'
        clientSocket.sendall((msgHeader+"file not found").encode())
        clientSocket.close()
        return

    msgHeader = 'HTTP/1.1 200 OK \r\n' \
                    '\r\n'

    if is_binary:
        clientSocket.sendall(msgHeader.encode() + file_content)
    else:
        clientSocket.sendall((msgHeader + file_content).encode())

    clientSocket.close()

IP_ADRESS = "127.0.0.1"
PORT_NUMBER = 8000

myServerSocket = socket(AF_INET, SOCK_STREAM)
myServerSocket.bind((IP_ADRESS, PORT_NUMBER))
myServerSocket.listen()
print(f"Servidor ouvindo em {IP_ADRESS} : {PORT_NUMBER}")

while True:
    clientSocket, clientAdress = myServerSocket.accept()
    print(f"Cliente {clientAdress[0]} : {clientAdress[1]} conectado com sucesso!")

    Thread(target=handleRequest, args=(clientSocket, clientAdress)).start()

myServerSocket.close()

