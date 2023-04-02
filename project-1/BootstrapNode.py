from socket import socket, AF_INET, SOCK_STREAM
from hashlib import sha3_224

# Classe do nó que vai ficar ali para direcionar os outros quando tudo ainda for mato
class BootstrapNode:
    
    # Inicializando o "servidor"
    def __init__(self, ip, port):
        self.count = 0
        self.IP_ADRESS = ip
        self.PORT_NUMBER = port
        self.nodes = {} # Dicionário para guardar as informações dos outros nós
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.IP_ADRESS, self.PORT_NUMBER))
        self.server_socket.listen()
    
    # Começa a escutar por solicitações para se conectar
    def listening(self):
        print("listening")
        while True:
            client_socket, client_adress = self.server_socket.accept()
            print(f"connecting to {client_socket}")
            nodeId = self.getNewID(client_adress) # Solicita um ID único para armazenar o nó
            self.nodes[nodeId] = client_adress # Armazena as Informações do nó
            print(self.nodes)
    
    # Função para gerar o ID único a partir da função hash sha3_224
    def getNewID(self, client_adress):
        hash_obj = sha3_224() # Cria um objecto hash
        print(client_adress[0] + str(client_adress[1]))
        as_bytes = (client_adress[0] + str(client_adress[1])).encode()
        hash_obj.update(as_bytes)
        hash_value = hash_obj.hexdigest() # Usa a função hash com o IP do cliente e passa para hexadecimal
        return hash_value


bootstrap_node = BootstrapNode("localhost", 8000)
bootstrap_node.listening()