import socket
from termcolor import colored

# Configurações do cliente
HOST = 'localhost'
PORT = 7000

# Cria um socket e se conecta ao servidor
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((HOST, PORT))

player_hand = list()

def format_data(data):
    return data.split(" | ")

def verify_type(data):
    print('\n\n', data[7], '\n\n')
    
    if data[0] == 'HAND':
        player_hand.append(data[8])   
        
        print('Sua mão é: ', player_hand)
        return player_hand
   
# Loop infinito para enviar e receber mensagens
while True:
    resposta = cliente_socket.recv(1024).decode()
    
    formated_data = format_data(resposta)
    
    verify_type(formated_data)
    
    # if formated_data[0] == 'HAND':
        # print('Sua mão é: ', algo)        
        
    # Envia mensagem para o servidor
    mensagem = input('Cliente 2: ')
    cliente_socket.sendall(mensagem.encode())

    # Recebe resposta do servidor
    if resposta:
        print('Servidor:', resposta)
