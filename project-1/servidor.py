import socket
import threading

# Definir o endereço do servidor
HOST = '127.0.0.1'
PORT = 5000

# Criar o socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associar o socket ao endereço do servidor
sock.bind((HOST, PORT))

# Armazenar as conexões dos clientes
conexoes = []


def receber_mensagens(conn, addr):
    while True:
        # Esperar pela mensagem do cliente
        mensagem = conn.recv(1024)

        # Exibir a mensagem recebida
        print('Mensagem recebida de', addr, ':', mensagem.decode('utf-8'))

        # Enviar a mensagem para todos os clientes conectados
        for conexao in conexoes:
            if conexao != conn:
                conexao.sendall(mensagem)

        # Fechar a conexão se a mensagem for 'sair'
        if mensagem.decode('utf-8') == 'sair':
            conn.close()
            conexoes.remove(conn)
            break


# Loop principal
while True:
    # Esperar por uma conexão
    sock.listen()
    conn, addr = sock.accept()

    # Adicionar a conexão à lista de conexões
    conexoes.append(conn)
    # print(conexoes)

    # Criar uma thread para receber mensagens do cliente
    thread_receber = threading.Thread(
        target=receber_mensagens, args=(conn, addr))
    thread_receber.start()

# Fechar o socket
sock.close()
