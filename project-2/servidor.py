from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import os

IP_ADRESS = "127.0.0.1"
PORT_NUMBER = 8014

def serve_folder(folder_path):
    array_de_arquivos = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        print(folder_path == dirpath)
        print(filenames)
        for filename in filenames:
            array_de_arquivos.append(filename)
    return array_de_arquivos
# Trata as requisições dos clientes

def handleRequest(clientSocket, clientAdress):
    clientRequest = clientSocket.recv(1024).decode() # Recebe a requisição do cliente
    print(f"O cliente requisitou: {clientRequest}")

    # print(clientRequest.split("\r\n")[0])

    header = clientRequest.split("\r\n")[0] # Recorta a header da solicitação
    # print(header, len(header))
    if len(header.split(" / ")) == 2:
        searched_file = "./Pages/index.html"
    else:
        searched_file = 'data/'+header.split()[1][1:] # Descobre qual arquivo foi solicitado

    print(f"Header: {header}, Seached file: {searched_file}")
    extension = searched_file.split(".")[-1] # Pega a extensão do arquivo solicitado

    # Caso a extensão não seja nenhuma dessas o arquivo é binário ["png", "jpg", "jpeg"...]
    is_binary = True
    if extension in ["html", "css", "js"]:
        is_binary = False

    try: # Tenta abrir o arquivo
        if is_binary:
            file = open(searched_file, 'rb')
            print(file)
        else:
            file = open(searched_file, 'r', encoding='utf-8')

    except FileNotFoundError: # Caso o arquivo não seja encontrado

        # Header com status de File Not Found
        msgHeader = 'HTTP/1.1 404 File not found \r\n' \
                    '\r\n'
        clientSocket.sendall((msgHeader+"file not found").encode()) # Devolve a mensagem para o cliente
        clientSocket.close() # Fecha a coneção com o cliente
        return # Quebra a sequência do código

    # Header com status de sucesso
    msgHeader = 'HTTP/1.1 200 OK \r\n' \
                    '\r\n'
    
    file_content = file.read() # Ler o conteúdo do arquivo
    if searched_file == "./Pages/index.html":
        print(serve_folder('./data'))
        for i in serve_folder('./data'):
            print(i)
            file_content+= f"<li> <a target='_blank' href='/{i}'>{i}</a> </li>"
        file_content += '''</ul></body></html>'''

    # Envia o arquivo solicitado para o cliente
    if is_binary:
        clientSocket.sendall(msgHeader.encode() + file_content)
    else:
        clientSocket.sendall((msgHeader + file_content).encode())

    clientSocket.close() # Fecha conexão com o cliente

myServerSocket = socket(AF_INET, SOCK_STREAM) # Criação do socket
myServerSocket.bind((IP_ADRESS, PORT_NUMBER)) # Vincula nosso servidor a derterminada porta
myServerSocket.listen() # Servidor escutando por requisições
print(f"Servidor ouvindo em {IP_ADRESS} : {PORT_NUMBER}")

while True:
    clientSocket, clientAdress = myServerSocket.accept() # Aceita requisição do cliente
    print(f"Cliente {clientAdress[0]} : {clientAdress[1]} conectado com sucesso!")

    # Passa o tratamento da requisição para as threads
    Thread(target=handleRequest, args=(clientSocket, clientAdress)).start()


myServerSocket.close() # Encerra o servidor

# Para matar o processo
# netstat -a -n -o | findstr 8000
# Taskkill /PID <pid> /F
