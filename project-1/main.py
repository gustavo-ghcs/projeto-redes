import socket
import threading

# Mensagens a serem enviadas
messages = [
    "Obra na BR-101",
    "Obra na PE-015",
    "Acidente Avenida Norte",
    "Acidente Avenida Cruz Cabugá",
    "Trânsito Intenso na Avenida Boa viagem",
    "Trânsito Intenso na Governador Agamenon Magalhães",
]


# Função para lidar com conexões recebidas
def handle_client(client_socket, address):
    print(f"Conexão estabelecida com {address}")
    packets_received = 0

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            packets_received += 1
            message = data.decode("utf-8")
            print(f"Recebido de {address}: {message}")

            if packets_received >= 6:
                break
        except:
            break

    print(f"Conexão encerrada com {address}")
    client_socket.close()


# Função para iniciar o servidor
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(5)

    print(f"Servidor ouvindo na porta {port}")

    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()


# Função para conectar-se a outros nós e enviar mensagens
def connect_and_send_messages(ip, port, messages_to_send):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    for message in messages_to_send:
        client_socket.sendall(message.encode("utf-8"))

    client_socket.close()


def main():
    local_port = int(input("Digite a porta local para ouvir conexões: "))
    server_thread = threading.Thread(target=start_server, args=(local_port,))
    server_thread.start()

    while True:
        action = input("Digite 'c' para conectar a um nó ou 'q' para sair: ")

        if action.lower() == "c":
            remote_ip = input("Digite o endereço IP remoto: ")
            remote_port = int(input("Digite a porta remota: "))
            message_indexes = input("Digite os índices das mensagens a serem enviadas (ex: 1,2,3): ")
            message_indexes = list(map(int, message_indexes.split(",")))

            messages_to_send = [messages[i - 1] for i in message_indexes]
            connect_and_send_messages(remote_ip, remote_port, messages_to_send)
        elif action.lower() == "q":
            break


if __name__ == "__main__":
    main()
