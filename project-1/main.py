import socket
import threading
import time

# Função para lidar com cada conexão de cliente
def handle_client(socket_cliente, endereco):
    # Exibe uma mensagem informando que uma conexão foi estabelecida
    print(f"\n***Conexão estabelecida com {endereco}***")

    while True:
        try:
            # Recebe dados do cliente
            dado = socket_cliente.recv(1024)
            if not dado:
                break

            # Converte os dados em uma string e exibe a mensagem recebida
            mensagem = dado.decode("utf-8")
            print(f"Recebido de {endereco}: {mensagem}")

            # Envia uma mensagem de confirmação de reecebimento
            mensagem_confirmacao = "Mensagem recebida pelo destinatário!"
            socket_cliente.sendall(mensagem_confirmacao.encode("utf-8"))
        except:
            break

    # Exibe uma mensagem informando que a conexão foi encerrada
    print(f"\n***Conexão encerrada com {endereco}***")

    # Pergunta ao usuário se ele deseja se conectar a outro nó ou sair do programa
    print("\nDigite 'c' para conectar-se a um nó e enviar a lista de mensagens, ou digite 's' para sair do programa, ou aguarde uma mensagem de outro nó: \n")

    # Fecha a conexão com o cliente
    socket_cliente.close()


# Função para iniciar o servidor do nó
def start_server(porta, ip):
    # Cria um objeto socket para o servidor e o configura para reutilizar endereços
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_servidor.bind((ip, porta))

    # Inicia o servidor e o coloca em modo de espera por conexões
    socket_servidor.listen(5)

    # Exibe uma mensagem informando que o servidor está ouvindo na porta especificada
    print(f"***Servidor do nó ouvindo na porta {porta}***\n")

    while True:
        # Aceita uma conexão de cliente e cria uma nova thread para lidar com ela
        socket_cliente, endereco = socket_servidor.accept()
        thread = threading.Thread(
            target=handle_client, args=(socket_cliente, endereco))
        thread.start()


# Função para conectar-se a outros nós e enviar mensagens
def connect_and_send_messages(ip, porta):
    # Mensagens a serem enviadas
    mensagens = [
        "Obra na BR-101",
        "Obra na PE-015",
        "Acidente Avenida Norte",
        "Acidente Avenida Cruz Cabugá",
        "Trânsito Intenso na Avenida Boa viagem",
        "Trânsito Intenso na Governador Agamenon Magalhães",
    ]
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect((ip, porta))
    contador = 0

    while contador <= len(mensagens):
        for i in range(contador):
            texto = mensagens[i]
            socket_cliente.sendall(texto.encode("utf-8"))
            time.sleep(0.2)

            # Receber mensagem de confirmação de recebimento
            mensagem_confirmacao = socket_cliente.recv(1024).decode("utf-8")
            print(mensagem_confirmacao)

        contador += 2
    socket_cliente.close()


def main():
    try:
        # Definindo o IP como localhost, para que ela possa s
        ip = "localhost"
        # Obter a porta local do usuário
        porta_local = int(
            input("Digite a porta local para que este nó ouça conexões de outros nós: "))

        # Iniciar servidor em uma thread separada
        thread_servidor = threading.Thread(
            target=start_server, args=(porta_local, ip))
        thread_servidor.start()

        # Aguardar 0.3 segundos para que o servidor possa ser iniciado
        time.sleep(0.3)

        while True:
            # Obter acao desejada pelo usuário
            acao = input(
                "\nDigite 'c' para conectar-se a um nó e enviar a lista de mensagens, ou digite 's' para sair do programa, ou aguarde uma mensagem de outro nó: \n")

            if acao.lower() == "c":
                # Conectar-se a outro nó e enviar mensagens
                porta_remota = int(
                    input("Digite a porta remota do nó para o qual deseja enviar mensagens: "))
                connect_and_send_messages(ip, porta_remota)
            elif acao.lower() == "s":
                # Sair do programa
                print("\n**Programa encerrado.**")
                break
            else:
                # Ação inválida
                print("\n**Atenção! Verifique se as entradas estão corretas!**\n")
    except:
        # Lidar com erros de entrada do usuário
        print("\n**Ops! Parece que aconteceu um erro, verifique a porta inserida e tente novamente.\n")
        # Recomeçar a função main
        main()


main()
