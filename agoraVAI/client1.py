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
player_id = 0

def menu():
    print("Type 'put' to put a card")
    print("Type 'buy' to buy cards")
    print("Type 'quit' to quit the game")
    option = input(' -> ')
    return option

def print_hand(deck):
    for card in deck:
        card.print_card()

def format_data(data):
    return data.split(" | ")

def put_card():
    print("Suas cartas são: ")
    print_hand(player_hand)
    option = menu()
    if(option == 'put'):
        print("Digite a carta que deseja jogar (cor número)")
        card_number = input(' -> ')
        

def verify_type(data):
    if data[0] == 'HAND':
        player_id = data[1]
        print("Você é o jogador ", player_id)
        print("Recebendo as cartas...")
        #Recebe a mão do servidor
        string_deck = data[8]
        string_deck = string_deck[:-2]
        string_deck = string_deck.split(', ')
        for card in string_deck:
            card = card.split(' ')
            player_hand.append(Card(card[1], card[0]))
        print_hand(player_hand)

    elif data[0] == 'START_GAME':
        print("O jogo começou!")
        previous_card = data[3]
        previous_card = previous_card.split(' ')
        print("A carta anterior é: ", colored(previous_card[0], previous_card[1]))
        #se o next_player for igual ao player_id, é a vez dele
        if(data[9] == player_id):
            print("É a sua vez de jogar!")
            put_card()
        else:
            print("É a vez do jogador ", data[9])
            print("Aguardando jogada do jogador ", data[9])
   
# Loop infinito para enviar e receber mensagens
while True:
    resposta = cliente_socket.recv(1024).decode()
    
    formated_data = format_data(resposta)

    verify_type(formated_data)
    
    # if message == 'buy':
    #     print('Você comprou uma carta')
    #     data = 'CARD_BUYED |   |   |   |   |   |  SUCESS |  DATA | STRING_DECK | PLAYER_NEXT_TURN '
        
    #parei aqui, tentando fazer o buy card!
    
    
    # verify_type(formated_data)
    
    # if formated_data[0] == 'HAND':
        # print('Sua mão é: ', algo)        
        
    # Envia mensagem para o servidor
    # mensagem = input('Cliente 1: ')
    # cliente_socket.sendall(mensagem.encode())

    # Recebe resposta do servidor
    # if resposta:
    #     print('Servidor:', resposta)
