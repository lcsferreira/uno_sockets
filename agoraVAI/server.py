import socket

# Configurações do servidor
HOST = 'localhost'
PORT = 5000

# Cria um socket e associa ao host e porta especificados
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.bind((HOST, PORT))

# Escuta por conexões
servidor_socket.listen()

# Aceita a primeira conexão
cliente1, endereco1 = servidor_socket.accept()
print('Cliente 1 conectado:', endereco1)

# Aceita a segunda conexão
cliente2, endereco2 = servidor_socket.accept()
print('Cliente 2 conectado:', endereco2)

# Loop infinito para receber e enviar mensagens
while True:
    # Recebe mensagem do cliente 1
    mensagem1 = cliente1.recv(1024).decode()
    if mensagem1:
        print('Cliente 1:', mensagem1)
        # Envia mensagem para o cliente 2
        cliente2.sendall(mensagem1.encode())

    # Recebe mensagem do cliente 2
    mensagem2 = cliente2.recv(1024).decode()
    if mensagem2:
        print('Cliente 2:', mensagem2)
        # Envia mensagem para o cliente 1
        cliente1.sendall(mensagem2.encode())
