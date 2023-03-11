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
    
    if data[0] == 'GAME_STARTED':
        print('O jogo começou')
        player_hand.append(data[8])
        print('Sua mão é: ', player_hand)
        
    
    elif data[0] == 'HAND':
        player_hand.append(data[8])   
        
        print('Sua mão é: ', player_hand)
        return player_hand
   
# Loop infinito para enviar e receber mensagens
while True:
    resposta = cliente_socket.recv(1024).decode()
    
    formated_data = format_data(resposta)
    
    if formated_data[0] == 'GAME_STARTED':
        print('O jogo começou')
        player_hand.append(formated_data[8])
        print('Sua mão é: ', player_hand)
    
    print("Escreva 'buy' para comprar")
    print("Escreva 'put' para colocar uma carta na mesa")
    print("Escreva 'quit' para sair")
    message = input(' -> ')
    
    if message == 'buy':
        print('Você comprou uma carta')
        data = 'CARD_BUYED |   |   |   |   |   |  SUCESS |  DATA | STRING_DECK | PLAYER_NEXT_TURN '
        
    #parei aqui, tentando fazer o buy card!
    
    
    # verify_type(formated_data)
    
    # if formated_data[0] == 'HAND':
        # print('Sua mão é: ', algo)        
        
    # Envia mensagem para o servidor
    mensagem = input('Cliente 1: ')
    cliente_socket.sendall(mensagem.encode())

    # Recebe resposta do servidor
    if resposta:
        print('Servidor:', resposta)
