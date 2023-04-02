from socket import socket, AF_INET, SOCK_STREAM

class ClientNode:

    # Inicializando o cliente
    def __init__(self, ip, port):
        self.IP_ADRESS = ip
        self.PORT_NUMBER = port
        self.client_socket = socket(AF_INET, SOCK_STREAM)
    
    # Função para conectar o novo nó ao nó bootstrap
    def connectToBootstrap(self):
        self.client_socket.connect((self.IP_ADRESS, self.PORT_NUMBER))
        print(f"Connected to bootstrap node at {self.IP_ADRESS}:{self.PORT_NUMBER}")



client_node = ClientNode("localhost", 8000)
client_node.connectToBootstrap()