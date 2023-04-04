import socket
import threading
import time

# Definir o endereço do servidor
HOST = '127.0.0.1'
PORT = 5000

# Definindo o array com as mensagens
mensagens = [
    "Obra na BR-101",
    "Obra na PE-015",
    "Acidente Avenida Norte",
    "Acidente Avenida Cruz Cabugá",
    "Trânsito Intenso na Avenida Boa viagem",
    "Trânsito Intenso na Governador Agamenon Magalhães"
]
contador = 0

# Criar o socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
sock.connect((HOST, PORT))

# Função para recebimento da mensagem


def receber_mensagens():
    while True:
        # Esperar pela mensagem do servidor
        mensagem = sock.recv(1024)
        print("Mensagem recebida" + mensagem.decode('utf-8'))


def enviar_mensagem(mensagem):
    sock.sendall(mensagem.encode('utf-8'))


# Criar uma thread para receber mensagens do servidor
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

# Loop principal para enviar mensagens
while True:
    if contador <= len(mensagens):

        for i in range(contador):
            mensagem = mensagens[i]
            enviar_mensagem(mensagem)
            # Adicione um pequeno intervalo entre o envio das mensagens
            time.sleep(0.1)

        contador += 2
        # Adicione um intervalo antes de enviar o próximo conjunto de mensagens
        time.sleep(3)

# Fechar o socket
sock.close()
