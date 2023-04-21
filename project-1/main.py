import socket
import threading
import time


def handle_client(client_socket, address):
    print(f"\n***Conexão estabelecida com {address}***")

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode("utf-8")
            print(f"Recebido de {address}: {message}")

            # Enviar mensagem de confirmação de recebimento
            confirmation_msg = "Mensagem recebida! "
            client_socket.sendall(confirmation_msg.encode("utf-8"))
        except:
            break

    print(f"\n***Conexão encerrada com {address}***")
    print("\nDigite 'c' para conectar-se  a um nó e enviar a lista de mensagens, ou digite 's' para sair do programa, ou aguarde uma mensagm de outro nó: \n")
    client_socket.close()


# Função para iniciar o servidor do nó
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(5)

    print(f"***Servidor do nó ouvindo na porta {port}***\n")

    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(
            target=handle_client, args=(client_socket, address))
        thread.start()


# Função para conectar-se a outros nós e enviar mensagens
def connect_and_send_messages(ip, port):
    # Mensagens a serem enviadas
    messages = [
        "Obra na BR-101",
        "Obra na PE-015",
        "Acidente Avenida Norte",
        "Acidente Avenida Cruz Cabugá",
        "Trânsito Intenso na Avenida Boa viagem",
        "Trânsito Intenso na Governador Agamenon Magalhães",
    ]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    counter = 0

    while counter <= len(messages):
        for i in range(counter):
            text = messages[i]
            client_socket.sendall(text.encode("utf-8"))
            time.sleep(0.2)

            # Receber mensagem de confirmação de recebimento
            confirmation_msg = client_socket.recv(1024).decode("utf-8")
            print(confirmation_msg)

        counter += 2

    client_socket.close()


def main():
    try:
        local_port = int(
            input("Digite a porta local para que este nó ouça conexões de outros nós: "))
        server_thread = threading.Thread(
            target=start_server, args=(local_port,))
        server_thread.start()
        time.sleep(0.3)

        while True:
            action = input(
                "\nDigite 'c' para conectar-se  a um nó e enviar a lista de mensagens, ou digite 's' para sair do programa, ou aguarde uma mensagm de outro nó: \n")

            if action.lower() == "c":
                ip = "localhost"
                remote_port = int(
                    input("Digite a porta remota do nó para o qual deseja enviar mensagens: "))

                connect_and_send_messages(ip, remote_port)
            elif action.lower() == "s":
                break
            else:
                print("\n**Antenção! Verifique se as entradas estão corretas!**\n")
    except:
        print("\n**Ops! Parece que aconteceu um erro, verifique a porta inserida e tente novamente.\n")
        main()


if __name__ == "__main__":
    main()
