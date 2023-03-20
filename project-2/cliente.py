from socket import socket, AF_INET, SOCK_STREAM

IP_ADRESS = "127.0.0.1"
PORT_NUMBER = 8000

myClienteSocket = socket(AF_INET, SOCK_STREAM)
myClienteSocket.connect((IP_ADRESS, PORT_NUMBER))
print("conectado com sucesso!")

myClienteSocket.sendall(b"ping!")
answer = myClienteSocket.recv(1024)
print(f"servidor respondeu {answer.decode()}")

myClienteSocket.close()