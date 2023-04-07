import threading
import socket
import random

# Define a porta que os nós vão usar para se comunicar
PORT = random.randint(1024, 65535)


class Node:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', PORT))
        self.server_socket.listen()
        print(f"Nó funcionando na porta {PORT}")

        # Armazena todas as conexões ativas
        self.connections = []

        # Inicia uma thread para ouvir conexões
        listening_thread = threading.Thread(target=self.listen_for_connections)
        listening_thread.start()

        # Inicia uma thread para permitir a entrada de comandos
        self.command_thread = threading.Thread(target=self.handle_commands)
        self.command_thread.start()

    def listen_for_connections(self):
        while True:
            # Define o timeout para 5 segundos
            self.server_socket.settimeout(5)
            try:
                # Aceita conexões dos outros pares
                client_socket, address = self.server_socket.accept()
                print(f"Nova conexão de endereço {address}")

                # Adiciona a nova conexão na lista de conexões
                self.connections.append(client_socket)

                # Inicia uma thread para lidar com a nova conexão
                client_thread = threading.Thread(
                    target=self.handle_client, args=[client_socket])
                client_thread.start()

                # Exibe a mensagem para escrever uma mensagem
                print("Escreva uma mensagem(ou digite 'exit' para sair):")
            except socket.error as e:
                # Em caso de erro, exiba a mensagem de erro e encerre a execução
                print(f"Erro no socket: {e}")
                break

    def handle_client(self, client_socket):
        while True:
            # Recebe mensagens do cliente
            data = client_socket.recv(1024)

            # Imprime a mensagem recebida
            print(f"Mensagem recebida: : {data.decode()}")

            # Encaminha a mensagem para os outros nós
            for connection in self.connections:
                if connection != client_socket:
                    connection.sendall(data)

    def handle_commands(self):
        while True:
            # Lê a entrada do usuário
            command = input()
            if command == "exit":
                # Fecha todas as conexões e encerra o programa
                for connection in self.connections:
                    connection.close()
                self.server_socket.close()
                return
            else:
                # Envia o comando para todos os nós
                for connection in self.connections:
                    connection.sendall(command.encode())


if __name__ == '__main__':
    node = Node()
