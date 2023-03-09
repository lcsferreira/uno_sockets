from socket import *
import threading
import sys
import time
import json
from termcolor import colored

if len(sys.argv) > 1:
    SERVER_IP = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
else:
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 5555

# CONSTANTS
MESSAGE = 'INIT'
NEW_MESSAGE = False
PLAYER_ID = None
PLAYER_TURN = None
PLAYERS_NUM = None
P_NUM_CARDS = None
LAST_DISCARD = None
PLAYER_HAND = []
DRAW_SUM = 0
ERR = None
MAX_PLAYERS = 2


# PROTOCOL
def update_consts(res):
    # update antigo
    '''print(res)
    res2 = res.split('/')
    print(res2)
    res3 = [x.split(' ', 1)[1] for x in res2]
    global PLAYER_ID, PLAYER_TURN, PLAYER_HAND, LAST_DISCARD, PLAYERS_NUM, P_NUM_CARDS
    PLAYER_ID, PLAYER_TURN, PLAYER_HAND, LAST_DISCARD, PLAYERS_NUM, P_NUM_CARDS = res3
    eval(PLAYER_ID)
    eval(PLAYER_TURN)
    eval(PLAYER_HAND)
    #eval(LAST_DISCARD)
    eval(PLAYERS_NUM)
    eval(P_NUM_CARDS)'''
    # update novo
    global PLAYER_ID, PLAYER_TURN, PLAYER_HAND, LAST_DISCARD, PLAYERS_NUM, P_NUM_CARDS,DRAW_SUM, MAX_PLAYERS
    res_dict = json.loads(res)
    if 'ID' in res_dict:
        PLAYER_ID = res_dict.get('ID')
    if 'HAND' in res_dict:
        PLAYER_HAND = res_dict.get('HAND')
    if 'LAST' in res_dict:
        LAST_DISCARD = res_dict.get('LAST')
    PLAYER_TURN = res_dict.get('TURN')
    PLAYERS_NUM = res_dict.get('PNUM')
    P_NUM_CARDS = res_dict.get('PNUMC')
    DRAW_SUM = res_dict.get('DRS')
    MAX_PLAYERS = res_dict.get('MAX')


def server_output(client_socket):
    while 1:
        att = client_socket.recv(1500)
        att = att.decode()
        # print(f'Server response: {att}')
        if len(att) > 0:
            if '}{' in att:
                att2 = att.split('}{')
            update_consts(att)


def client_input(client_socket):
    global NEW_MESSAGE, MESSAGE
    while 1:
        if NEW_MESSAGE:
            print(MESSAGE)
            client_socket.send(MESSAGE.encode())
            NEW_MESSAGE = False
            time.sleep(0.1)


def req(card, skip=False):
    print(card)
    global NEW_MESSAGE, MESSAGE
    if skip:
        MESSAGE = f'SKIP: 1, BUY: 0, PUT: 0 0 0'
    elif card.number is not None:
        MESSAGE = f'SKIP: 0, BUY: 0, PUT: {card.color} {card.number} 0'
    elif card.wild is not None:
        MESSAGE = f'SKIP: 0, BUY: 0, PUT: {card.color} 0 {card.wild}'
    elif card.number == 666 or card.color == 'deck':
        MESSAGE = f'SKIP: 0, BUY: 1, PUT: 0 0 0'
    NEW_MESSAGE = True


def client():
    server_name = SERVER_IP
    server_port = SERVER_PORT

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    server_output_thread = threading.Thread(target=server_output, args=(client_socket, ))
    server_output_thread.start()

    client_input_thread = threading.Thread(target=client_input, args=(client_socket, ))
    client_input_thread.start()

def draw():
    global NEW_MESSAGE, MESSAGE
    MESSAGE = f'DRAW'
    NEW_MESSAGE = True

def skip():
    global NEW_MESSAGE, MESSAGE
    MESSAGE = f'SKIP'
    NEW_MESSAGE = True

def buy():
    global NEW_MESSAGE, MESSAGE
    MESSAGE = f'BUY'
    NEW_MESSAGE = True

def put(card):
    global NEW_MESSAGE, MESSAGE
    MESSAGE = f'PUT {card.color} {card.number} {card.wild}'
    print (MESSAGE)
    # req(MESSAGE)
    NEW_MESSAGE = True

def uno():
    global NEW_MESSAGE, MESSAGE
    MESSAGE = f'UNO'
    NEW_MESSAGE = True

def game():
    run = True
    while run:
        print(f'Você é o jogador {PLAYER_ID} | É a vez do jogador: {PLAYER_TURN}')
        print(f'Quantidade de cartas nas mãos dos jogadores: {P_NUM_CARDS}')
        print(f'Carta na mesa:', end = ' ')
        card_table = (LAST_DISCARD.split(' ', 1))
        print(colored(card_table[1], card_table[0]))
        print(f'Suas cartas', end=' -> ')
        for card in PLAYER_HAND:
            card_splitted = (card.split(' ', 1))
            print(colored(card_splitted[1], card_splitted[0]), '|', end=' ') 
            
        if PLAYER_ID != PLAYER_TURN:
            print(f'\n\nVocê não pode jogar, é a vez do jogador {PLAYER_TURN}')
            break
        else:
            print('\n\n')
            print("Player Hand: ", PLAYER_HAND) # COLOR TYPE(NUMBER/RESERVE/DRAW2)
            print("Card table: ", card_table) # COLOR TYPE(NUMBER/RESERVE/DRAW2)
        
            action = input(f'\n\nQual ação deseja realizar? (skip, buy, put, uno, quit)')
            
            # if action == 'buy':
                
            if action == 'put':
                card = {'number': 0, 'color': None, 'wild': None}
                can_play = False
                vet_card_game = {'number': 0, 'color': None}
                card_game = input("\n\nQual carta você quer jogar? (Formato: cor número)")
                vet_card_game = card_game.split(" ")
                
                print("Carta que quer jogar: ", vet_card_game)
                print("Carta que está na mesa: ", card_table)
                print
                
                for card in PLAYER_HAND:
                    if card == card_game: #Se existir uma carta no baralho igual a carta que o jogador quer jogar, pode jogar!
                        if vet_card_game != card_table[0] and vet_card_game[1] != card_table[1]: #Verifica se a carta que o jogador quer jogar é igual a carta que está na mesa
                            can_play = False
                            print("\nCarta inválida, por favor, jogue outra carta!")
                        else:
                            can_play = True
                            break
                    else:
                        can_play = False

                if can_play == True:
                    card = {'number': vet_card_game[1], 'color': vet_card_game[0], 'wild': None}
                    req(card)
                    
                # print("Você não possui essa carta!")
                        
                # vet_card_game = card_game.split(" ")
                # req(card_game)
                        
                # if card_game == ":
                #Fazer verificação de carta válida
                # print("Card game", card_game)
                # print("Vet card game", vet_card_game)
                
                # if vet_card_game[0] != card_table[0] or vet_card_game[1] != card_table[1]:
                #     print("Carta inválida, por favor, jogue outra carta!")
                # else:
                #     req(vet_card_game)
                # req(card)
            #O que é draw?
        
            # if action == 'put':
            #     print(PLAYER_HAND)
            #     card = input(f'Qual carta deseja jogar?')
            #     for card in PLAYER_HAND:
            #         card_splitted = (card.split(' ', 1))
            #         if card_splitted[1] == card:
            #             req(card)
            #             break
            #         else:
            #             print('Carta não encontrada')
            #             break
                    
            if action == 'quit':
                sys.exit()
        
        # print(f'Draw sum: {DRAW_SUM}') #não sei o que é.

def progress_bar():
    if PLAYERS_NUM != MAX_PLAYERS:
        print('\r\nProgress: [50%] [#########################_________________________]')
    else:
        print('\r\nProgress: [100%] [##################################################]')
        
def menu():
    global PLAYERS_NUM, MAX_PLAYERS
    run = True
    while run:
        print(f'\nWaiting players...')
        progress_bar()
        print(f'({PLAYERS_NUM}/{MAX_PLAYERS})')
        time.sleep(5)
        if PLAYERS_NUM == MAX_PLAYERS:
            run = False
            print('\n == Starting game == \n')
            time.sleep(1)
            game()

client()
time.sleep(0.5)
menu()
