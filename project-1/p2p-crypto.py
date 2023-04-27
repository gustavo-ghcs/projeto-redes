import threading
import time
from Crypto.Cipher import DES3
from Crypto.Signature import DSS
from Crypto.Hash import SHA3_224
from Crypto.PublicKey import ECC
from Crypto import Random


def handle_client(socket_cliente, endereco, key_privada):
    print(f"\n***Conexão estabelecida com {endereco}***")

    while True:
        try:
            data = socket_cliente.recv(1024)
            if not data:
                break

            mensagem = data.decode("utf-8")
            partes_msg = mensagem.split(":")
            msg_criptografada = partes_msg[0]
            assinatura = partes_msg[1]
            iv = partes_msg[2]

            # Verificar assinatura digital da mensagem
            h = SHA3_224.new()
            h.update(msg_criptografada.encode())
            verificador = DSS.new(key_privada, 'fips-186-3')
            if not verificador.verify(h, assinatura):
                print("A mensagem recebida não é autêntica. Descartando.")
                break

            # Descriptografar mensagem
            cipher = DES3.new(iv.encode(), DES3.MODE_CBC, iv.encode())
            msg_descriptografada = cipher.decrypt(msg_criptografada.encode()).decode().strip()

            print(f"Recebido de {endereco}: {msg_descriptografada}")

            # Enviar mensagem de confirmação de recebimento
            msg_confirmacao = "Mensagem recebida! "
            socket_cliente.sendall(msg_confirmacao.encode("utf-8"))
        except:
            break

    print(f"\n***Conexão encerrada com {endereco}***")
    print("\nDigite 'c' para conectar-se a um nó e enviar a lista de mensagens, ou digite 's' para sair do programa, ou aguarde uma mensagem de outro nó: \n")
    socket_cliente.close()


# Função para iniciar o servidor do nó
def start_server(porta, key_privada):
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_servidor.bind(("", porta))
    socket_servidor.listen(5)

    print(f"***Servidor do nó ouvindo na porta {porta}***\n")

    while True:
        socket_cliente, endereco = socket_servidor.accept()
        thread = threading.Thread(
            target=handle_client, args=(socket_cliente, endereco, key_privada))
        thread.start()


def connect_and_send_messages(ip, porta):
    # Gerar chave privada e pública para ECC
    key_privada = ECC.generate(curve='prime224v1')
    chave_publica = key_privada.chave_publica()

    # Mensagens a serem enviadas
    mensagens = [
        "Obra na BR-101",
        "Obra na PE-015",
        "Acidente Avenida Norte",
        "Acidente Avenida Cruz Cabugá",
        "Trânsito Intenso na Avenida Boa viagem",
        "Trânsito Intenso na Governador Agamenon Magalhães",
    ]

    # Definir chave e IV para TDES
    chave_tdes = b"ThisIsASecretKey1234567890"
    iv = b"12345678"

    # Criar objeto TDES com a chave e IV definidos
    tdes_cipher = DES3.new(chave_tdes, DES3.MODE_CBC, iv)

    # Conectar ao outro nó
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect((ip, porta))
    contador = 0

    while contador <= len(mensagens):
        for i in range(contador):
            # Encriptar a mensagem com TDES
            texto_simples = mensagens[i].encode('utf-8')
            padded_plaintext = texto_simples + b"\0" * (8 - len(texto_simples) % 8)
            ciphertext = tdes_cipher.encrypt(padded_plaintext)

            # Hash da mensagem com SHA3-224
            h = SHA3_224.new()
            h.update(ciphertext)
            digest = h.digest()

            # Assinar o hash com a chave privada ECC
            assinatura = key_privada.sign(digest)

            # Enviar mensagem encriptada, hash e assinatura
            data = (ciphertext, digest, assinatura, chave_publica)
            socket_cliente.sendall(str(data).encode('utf-8'))

            # Receber mensagem de confirmação de recebimento
            msg_confirmacao = socket_cliente.recv(1024).decode("utf-8")
            print(msg_confirmacao)

        contador += 2

    socket_cliente.close()

def main():
    try:
        # Obter a porta local do usuário
        porta_local = int(input("Digite a porta local para que este nó ouça conexões de outros nós: "))

        # Iniciar servidor em uma thread separada
        thread_servidor = threading.Thread(target=start_server, args=(porta_local,))
        thread_servidor.start()

        # Aguardar 0.3 segundos para que o servidor possa ser iniciado
        time.sleep(0.3)

        while True:
            # Obter acao desejada pelo usuário
            acao = input("\nDigite 'c' para conectar-se a um nó e enviar a lista de mensagens, ou digite 's' para sair do programa, ou aguarde uma mensagem de outro nó: \n")

            if acao.lower() == "c":
                # Conectar-se a outro nó e enviar mensagens
                ip = "localhost"
                porta_remota = int(input("Digite a porta remota do nó para o qual deseja enviar mensagens: "))
                connect_and_send_messages(ip, porta_remota)
            elif acao.lower() == "s":
                # Sair do programa
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