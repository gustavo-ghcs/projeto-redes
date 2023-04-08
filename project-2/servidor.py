from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import os


# Lista o conteúdo de uma pasta no html
def list_content(html, searched_file):
        tags = {"png": "&#128247;", "mp4": "&#127916;", "mpeg": "&#127925;", "pdf": "&#128212;"}

        for i in os.listdir(searched_file):
            if os.path.isdir(os.path.join(f'./{searched_file}', i)):
                tag = "&#128193;"
            else:
                tag = tags.get(i.split(".")[-1])
                if not tag:
                    tag = "&#128196;"
            endereco = f"{searched_file}/{i}"
            html += f"<li> {tag} <a href='/{endereco}'>{i}</a> </li>"
        
        html += '''</ul></body></html>'''
        return html.encode()

# Trata as requisições dos clientes
def handleRequest(clientSocket, clientAdress):
    clientRequest = clientSocket.recv(1024).decode() # Recebe a requisição do cliente

    header = clientRequest.split("\r\n")[0] # Recorta a header da solicitação
    if header == "GET / HTTP/1.1":
        searched_file = "./Pages"
    else:
        try:
            searched_file = header.split()[1][1:] # Descobre qual arquivo foi solicitado
        except IndexError:
            return # Retorna porque não requisitou nada

    extension = searched_file.split(".")[-1] # Pega a extensão do arquivo solicitado

    is_binary = True
    if extension in ["html", "css", "js"]:
        is_binary = False

    # Se for um arquivo
    if not (os.path.isdir(searched_file)):
        try: # Tenta abrí-lo
            if is_binary:
                file = open(searched_file, 'rb')
            else:
                file = open(searched_file, 'r', encoding='utf-8')

        except FileNotFoundError: # Caso o arquivo não seja encontrado
            msgHeader = 'HTTP/1.1 404 File not found \r\n' '\r\n'
            clientSocket.sendall((msgHeader + "file not found").encode()) # Devolve a mensagem para o cliente
            clientSocket.close() # Fecha a coneção com o cliente
            return

        file_content = file.read()

    # Se for uma pasta
    if os.path.isdir(searched_file):
        html_file = open("index.html", 'r', encoding='utf-8') # Abre o html universal para listar os arquivos
        html_base = html_file.read() # File content recebe um html
        file_content = list_content(html_base, searched_file)

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
