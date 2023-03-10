import socket

# Configurações do cliente
HOST = 'localhost'
PORT = 5000

# Cria um socket e se conecta ao servidor
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((HOST, PORT))

# Loop infinito para enviar e receber mensagens
while True:
    # Envia mensagem para o servidor
    mensagem = input('Cliente 2: ')
    cliente_socket.sendall(mensagem.encode())

    # Recebe resposta do servidor
    resposta = cliente_socket.recv(1024).decode()
    if resposta:
        print('Servidor:', resposta)
