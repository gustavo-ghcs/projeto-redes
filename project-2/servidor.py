from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import os

# Lista o conteúdo de uma pasta no html
def list_content(html, searched_file):
        tags = {"png": "&#128247;", "mp4": "&#127916;", "mpeg": "&#127925;", "aac": "&#127925;", "wav": "&#127925;", "flac": "&#127925;", "mp3": "&#127925;", "pdf": "&#128212;", "txt": "&#128212;", "epub": "&#128212;", "odt": "&#128212;", "docx": "&#128212;", "rtf": "&#128212;"}

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

# Checa se tem caracteres inválidos na header
def invalid_characters(header):
    for char in ['%7B', '%7D', '%'+'%', '%20', '[', ']', ':', '*', '?', '"', '<', '>', '|']:
        if char in header:
            return True
    return False

# Abre e retorna o conteúdo de um arquivo html
def get_html_content(filename):
    html_file = open(filename, 'r', encoding='utf-8')
    return html_file.read()

# Devolve a mensagem de erro para o cliente
def error_message(clientSocket, error_code, error_msg):
    msgHeader = f'HTTP/1.1 {error_code} {error_msg} \r\n' '\r\n'
    clientSocket.sendall((msgHeader + get_html_content(f"./Erros/{error_code}.html")).encode()) # Devolve a mensagem para o cliente
    clientSocket.close() # Fecha a coneção com o cliente

# Trata as requisições dos clientes
def handleRequest(clientSocket, clientAdress):
    clientRequest = clientSocket.recv(1024).decode() # Recebe a requisição do cliente

    header = clientRequest.split("\r\n")[0] # Recorta a header da solicitação
    if header == "GET / HTTP/1.1":
        searched_file = "./Pages"

    elif header[-3:] != "1.1":
        return error_message(clientSocket, 505, "HTTP Version Not Supported")

    elif invalid_characters(header):
        return error_message(clientSocket, 400, "Bad Request")

    else:
        try:
            searched_file = header.split()[1][1:] # Descobre qual arquivo foi solicitado
            if searched_file == "Pages/Adm":
                return error_message(clientSocket, 403, "Forbidden")

        except IndexError:
            return # Retorna porque não requisitou nada

    extension = searched_file.split(".")[-1] # Pega a extensão do arquivo solicitado

    is_binary = True
    if extension in ["html", "htm", "css", "js"]:
        is_binary = False

    # Se for um arquivo
    if not (os.path.isdir(searched_file)):
        try: # Tenta abrí-lo
            if is_binary:
                file = open(searched_file, 'rb')
            else:
                file = open(searched_file, 'r', encoding='utf-8')

        except FileNotFoundError: # Caso o arquivo não seja encontrado
            return error_message(clientSocket, 404, "Not Found")

        file_content = file.read()

    # Se for uma pasta
    if os.path.isdir(searched_file):
        html_base = get_html_content("index.html") # Pega o conteúdo do html base para listar arquivos
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
myServerSocket.bind((IP_ADRESS, PORT_NUMBER)) # Vincula nosso servidor a determinada porta
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
