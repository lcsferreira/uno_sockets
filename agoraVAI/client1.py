import socket
import sys
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
previous_card = None

def menu():
    option = ""
    while option != 'put' or option != 'buy' or option != 'quit':
        print("\nType 'put' to put a card")
        print("Type 'buy' to buy cards")
        print("Type 'quit' to quit the game")
        option = input(' ->')
        if option == 'put' or option == 'buy' or option == 'quit':
            return option
        else:
            print("Opção inválida, tente novamente")

def print_hand(deck):
    for card in deck:
        card.print_card()

def format_data(data):
    return data.split(" | ")

def remove_card_from_hand(card):
    global player_hand
    for i in range(0, len(player_hand)):
            if player_hand[i].number == card.number and player_hand[i].color == card.color:
                player_hand.pop(i)
                break

def put_card():
    global player_hand, previous_card
    print("A carta da mesa é: ", colored(previous_card[0], previous_card[1]))
    print("Suas cartas são: ")
    print_hand(player_hand)
    option = menu()
    if(option == 'put'):
        has_card = False
        card_to_put = input("Qual carta você deseja jogar? (cor número):")
        card_to_put_formated = card_to_put.split()

        for cards in player_hand:            
            if cards.color == card_to_put_formated[0] or cards.number == card_to_put_formated[1]: #se a cor ou o nº for igual, joga a carta
                has_card = True
                break
            else:
                has_card = False
        if has_card == True and (card_to_put_formated[1] == "wild" or card_to_put_formated[1] == "wild_draw4"):
            color_wild = input("Qual cor você deseja jogar? (red, blue, green, yellow):")
            card_to_put_formated[0] = color_wild
            print("Você jogou a carta ", colored(card_to_put_formated[1], card_to_put_formated[0]))    
            data = 'CARD_PUT | PLAYER_ID | CARD_TO_PUT |   |   |   |   |   |   |  '
            data = data.replace('PLAYER_ID', player_id)
            data = data.replace('CARD_TO_PUT', card_to_put)
            cliente_socket.sendall(data.encode()) #envia pro servidor
        elif has_card == True and (previous_card[1] == card_to_put_formated[0] or previous_card[0] == card_to_put_formated[1]):
            print("Você jogou a carta ", colored(card_to_put_formated[1], card_to_put_formated[0]))    
            data = 'CARD_PUT | PLAYER_ID | CARD_TO_PUT |   |   |   |   |   |   |  '
            data = data.replace('PLAYER_ID', player_id)
            data = data.replace('CARD_TO_PUT', card_to_put)
            cliente_socket.sendall(data.encode()) #envia pro servidor
        else:
            print("Você não pode jogar essa carta! (Ou você não tem ela na mão, ou ela não é válida)")
            put_card()    
    elif(option == 'buy'):
        data = 'BUY_CARD | PLAYER_ID |   |   |   |   |   |   |   |  '
        data = data.replace('PLAYER_ID', player_id)
        cliente_socket.sendall(data.encode())
    elif(option == 'quit'):
        sys.exit()
        
def verify_type(data):
    global player_id, player_hand, previous_card
    player_id = data[1]
    
    if data[0] == 'HAND':
        print("Você é o jogador ", player_id)
        print("Recebendo as cartas...")
        #Recebe a mão do servidor
        string_deck = data[8]
        string_deck = string_deck[:-2]
        string_deck = string_deck.split(', ')
        for card in string_deck:
            card = card.split(' ')
            player_hand.append(Card(card[1], card[0]))

    elif data[0] == 'START_GAME':
        print("\nO jogo começou!")
        previous_card = data[3]
        previous_card = previous_card.split(' ')
        #se o next_player for igual ao player_id, é a vez dele
        if(data[9] == player_id):
            print("É a sua vez de jogar!")
            put_card()
        else:
            print("A carta da mesa é: ", colored(previous_card[0], previous_card[1]))
            print('Suas cartas são:')
            print_hand(player_hand)
            print("É a vez do jogador ", data[9])
            print("Aguardando jogada do jogador ", data[9])
            print("O seu adversário possui: ", data[7], " cartas")

    elif data[0] == "ATT_CARD":
        if(data[6] == 'Success'):
            print("A carta foi jogada com sucesso!")
            previous_card = data[3]
            previous_card = previous_card.split(' ')
            if previous_card[0] == 'draw2' and player_id == data[9]:
                print("Você comprou 2 cartas obrigatoriamente!")
                cards_to_add = data[8]
                cards_to_add = cards_to_add.split(', ')
                print(cards_to_add)
                for card in cards_to_add:
                    card = card.split(' ')
                    player_hand.append(Card(card[1], card[0]))
            elif previous_card[0] == 'wild_draw4' and player_id == data[9]:
                print("Você comprou 4 cartas obrigatoriamente!")
                cards_to_add = data[8]
                cards_to_add = cards_to_add.split(', ')
                for card in cards_to_add:
                    card = card.split(' ')
                    player_hand.append(Card(card[1], card[0]))
        
            print("O seu adversário possui: ", data[7], " cartas")
            if(data[9] == player_id):
                print("É a sua vez de jogar!")
                put_card()
            else:
                card_formatted = data[3]
                card_formatted = card_formatted.split(' ')
                print(card_formatted)
                remove_card = Card(card_formatted[1], card_formatted[0])
                remove_card_from_hand(remove_card)
                print("A carta da mesa é: ", colored(previous_card[0], previous_card[1]))
                print('Suas cartas são:')
                print_hand(player_hand)
                print("É a vez do jogador ", data[9])
                print("Aguardando jogada do jogador ", data[9])
                print("O seu adversário possui: ", data[7], " cartas")
        else:
            print("A carta não é válida!")
            previous_card = data[3]
            previous_card = previous_card.split(' ')
            print("A carta da mesa é: ", colored(previous_card[0], previous_card[1]))
            if(data[9] == player_id):
                print("Jogue outra carta!")
                put_card()
            else:
                print("A carta da mesa é: ", colored(previous_card[0], previous_card[1]))
                print('Suas cartas são:')
                print_hand(player_hand)
                print("É a vez do jogador ", data[9])
                print("Aguardando jogada do jogador ", data[9])
                print("O seu adversário possui: ", data[7], " cartas")
    elif data[0] == "CARDS_BUYED":
        string_deck = data[8]
        previous_card = data[2]
        previous_card = previous_card.split(' ')
        if(string_deck != 'empty'):
            print("Você compra até conseguir jogar!")
            print("Recebendo as cartas...")

            if(string_deck == "no cards"):
                print("Você comprou e jogou!")
            else:
                string_deck = string_deck.split(', ')
                print("você comprou ", len(string_deck), " cartas")
                for card in string_deck:
                    card = card.split(' ')
                    player_hand.append(Card(card[1], card[0]))
            print("A carta da mesa é: ", colored(previous_card[0], previous_card[1]))
            print("O seu adversário possui: ", data[7], " cartas")
        else:
            print("O outro jogador comprou cartas!")
            print("É a sua vez de jogar!")
            print("O seu adversário possui: ", data[7], " cartas")
            put_card()
   
# Loop infinito para enviar e receber mensagens
while True:
    resposta = cliente_socket.recv(1024).decode()
    
    formated_data = format_data(resposta)

    verify_type(formated_data)