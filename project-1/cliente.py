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
    quebraDeLinha = 0
    while True:
        # Esperar pela mensagem do servidor
        mensagem = sock.recv(1024)
        print("Mensagem recebida " + mensagem.decode('utf-8'))
        quebraDeLinha += 1
        if quebraDeLinha == 2 or quebraDeLinha == 6 or quebraDeLinha == 12:
            print('='*20)

def enviar_mensagem(mensagem):
    sock.sendall(mensagem.encode('utf-8'))

# Criar uma thread para receber mensagens do servidor
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

# Input para impedir que o cliente envie as mensagens assim que for iniciado
while True:
    começar = input("Deseja iniciar o envio de mensagens?[S/N]\n")
    if começar in "sS":
        break
    else:
        print('Deixa de frescura e aperta sim logo =)')

# Loop principal para enviar mensagens
while True:
    if contador <= len(mensagens):
    
        for i in range(contador):
            mensagem = mensagens[i]
            enviar_mensagem(f"{mensagem}")
            time.sleep(0.1)  # Adicione um pequeno intervalo entre o envio das mensagens

        contador += 2
        time.sleep(3)  # Adicione um intervalo antes de enviar o próximo conjunto de mensagens

# Fechar o socket
sock.close()