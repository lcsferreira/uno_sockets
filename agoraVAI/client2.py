import socket
from termcolor import colored

from server import Card

# Configurações do cliente
HOST = 'localhost'
PORT = 7000

# Cria um socket e se conecta ao servidor
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((HOST, PORT))

player_hand = list()

def print_hand(deck):
    for card in deck:
        card.print_card()

def format_data(data):
    return data.split(" | ")

def verify_type(data):
    if data[0] == 'HAND':
        #Recebe a mão do servidor
        string_deck = data[8]
        string_deck = string_deck[:-2]
        string_deck = string_deck.split(', ')
        for card in string_deck:
            card = card.split(' ')
            player_hand.append(Card(card[1], card[0]))
   
# Loop infinito para enviar e receber mensagens
while True:
    resposta = cliente_socket.recv(1024).decode()
    
    formated_data = format_data(resposta)
    
    verify_type(formated_data)
    
    # if formated_data[0] == 'HAND':
        # print('Sua mão é: ', algo)        
        
    # Envia mensagem para o servidor
    # mensagem = input('Cliente 2: ')
    # cliente_socket.sendall(mensagem.encode())

    # Recebe resposta do servidor
    # if resposta:
    #     print('Servidor:', resposta)
