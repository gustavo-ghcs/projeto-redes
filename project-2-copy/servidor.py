from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import os

# Trata as requisições dos clientes
def handleRequest(clientSocket, clientAdress):
    clientRequest = clientSocket.recv(1024).decode() # Recebe a requisição do cliente
    print(clientRequest.split("\r\n")[0])

    # Requisições
    # GET / HTTP/1.1
    # GET /flork.png HTTP/1.1
    # GET ./Pages/data HTTP/1.1
    # GET ./Pages/data/teste.txt HTTP/1.1

    header = clientRequest.split("\r\n")[0] # Recorta a header da solicitação
    if header == "GET / HTTP/1.1":
        searched_file = "./Pages"
    else:
        try:
            searched_file = header.split()[1][1:] # Descobre qual arquivo foi solicitado
            print("1:", searched_file)

            """if not searched_file.startswith('/Pages'):
                # Concatena './Pages/' com searched_file
                searched_file = './Pages/' + searched_file
                print("2:", searched_file)"""

        except IndexError:
            return

    #searched_file = header.split()[1][1:]

    extension = searched_file.split(".")[-1] # Pega a extensão do arquivo solicitado
    # Caso a extensão não seja nenhuma dessas o arquivo é binário ["png", "jpg", "jpeg"...]
    is_binary = False
    if extension not in ["html", "css", "js"]:
        is_binary = True
    
    if not (os.path.isdir(searched_file)):
        try: # Tenta abrir o arquivo
            if is_binary:
                file = open(searched_file, 'rb')
            else:
                file = open(searched_file, 'r', encoding='utf-8')

        except FileNotFoundError: # Caso o arquivo não seja encontrado
            # Header com status de File Not Found
            msgHeader = 'HTTP/1.1 404 File not found \r\n' '\r\n'
            clientSocket.sendall((msgHeader + "file not found").encode()) # Devolve a mensagem para o cliente
            clientSocket.close() # Fecha a coneção com o cliente
            return # Quebra a sequência do código

        file_content = file.read()
    

    if os.path.isdir(searched_file):
        file = open("index.html", 'r', encoding='utf-8')
        file_content = file.read() # File content recebe um html
        tags = {"png": "📷", "mp4": "🎞️", "mpeg": "🎵", "pdf": "📔"}
        print("3:", searched_file)
        for i in os.listdir(searched_file):
            #print("relative path:", os.path.relpath())
            if os.path.isdir(os.path.join(f'./{searched_file}', i)):
                tag = "📁"
                endereco = f"{searched_file}/{i}"
                #endereco = os.path.join(searched_file, i)
                #endereco = searched_file
                print("endereco diretory:", endereco)
            else:
                tag = tags.get(i.split(".")[-1])
                if not tag:
                    tag = "📄"
                endereco = f"{searched_file}/{i}"
                #endereco = os.path.join(searched_file, i)
                #endereco = searched_file
                print("endereco file:", endereco)
            file_content += f"<li> {tag} <a target='_blank' href='/{endereco}'>{i}</a> </li>"

        file_content += '''</ul></body></html>'''
        file_content = file_content.encode()


    # Header com status de sucesso
    msgHeader = 'HTTP/1.1 200 OK \r\n' '\r\n'

    # Envia o arquivo solicitado para o cliente
    if is_binary:
        clientSocket.sendall(msgHeader.encode() + file_content)
    else:
        clientSocket.sendall((msgHeader + file_content).encode())

    clientSocket.close() # Fecha conexão com o cliente


IP_ADRESS = "127.0.0.1"
PORT_NUMBER = 8014

myServerSocket = socket(AF_INET, SOCK_STREAM) # Criação do socket
myServerSocket.bind((IP_ADRESS, PORT_NUMBER)) # Vincula nosso servidor a derterminada porta
myServerSocket.listen() # Servidor escutando por requisições
print(f"Servidor ouvindo em {IP_ADRESS} : {PORT_NUMBER}")

while True:
    clientSocket, clientAdress = myServerSocket.accept() # Aceita requisição do cliente

    # Passa o tratamento da requisição para as threads
    Thread(target=handleRequest, args=(clientSocket, clientAdress)).start()


myServerSocket.close() # Encerra o servidor

# Para matar o processo
# netstat -a -n -o | findstr 8000
# Taskkill /PID <pid> /F
