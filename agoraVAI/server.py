import os
import random
import socket
import threading
import time
from termcolor import colored

# Configurações do servidor
HOST = 'localhost'
PORT = 7000
# data_Decks = 'INSTRUCTION | PLAYER_ID | CARD_TO_PUT | PREVIOUS_CARD | NUMBER | SET_COLOR | STATUS | DATA | STRING_DECK | NEXT_PLAYER'

class Game:
    def __init__(self):
        self.deck = list()
        self.players = list()
        self.turn_player = 0
        self.previous_card = None
        self.is_clockwise = True
        self.has_winner = False
        self.started = False
        
    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def create_deck(self):
        card_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "draw2", "wild_draw4", "wild"]
        card_colors = ["blue", "red", "yellow", "green"]

        for value in card_values:
            if value == "wild" or value == "wild_draw4":
                card = Card(None, value)
                continue
            for color in card_colors:
                card = Card(color, value)
                self.deck.append(card)
    
    def random_card(self):
        return random.choice(self.deck)
    
    def buy_cards(self):
        cards = list()
        card = random.choice(self.deck)
        if card.color == self.previous_card.color or card.number == self.previous_card.number:
            self.previous_card = card
        else:
            while card.color != self.previous_card.color and card.number != self.previous_card.number:
                card = random.choice(self.deck)
                if card.color == self.previous_card.color or card.number == self.previous_card.number:
                    self.previous_card = card
                    break
                cards.append(card)
            
            self.previous_card = card
        return cards
    
    def reverse_game(self):
        self.is_clockwise = not self.is_clockwise

    def shuffle_cards(self):
        random.shuffle(self.deck)

    def draw_player_hand(self):
        player_hand = list()

        for i in range (0, 7):
            player_hand.append(self.deck.pop())

        return player_hand
    
    def next_player(self):
        if self.is_clockwise:
            self.turn_player += 1
        else:
            self.turn_player -= 1  

    def remove_card_player(self, player, card):
        self.players[player].remove_card(card)
        
    def setup_player(self):
        self.create_deck()
        self.shuffle_cards()
        
        for player in self.players:
            player.hand = self.draw_player_hand()

    def setup_game(self):
        self.create_deck()
        self.shuffle_cards()
        self.turn_player = self.players[0]
        
        self.previous_card = self.random_card()
        while self.previous_card.color == None:
            self.previous_card = self.random_card()
        
        self.started = True
        
    def send_cards(self, cliente1, cliente2):
        self.setup_player()
        
        data = 'HAND | PLAYER_ID |   |   |   |   |   | DATA | STRING_DECK |  '
        hand = self.get_cards_stringfied(self.players[0].hand)
        data = data.replace('STRING_DECK', hand)
        data = data.replace('PLAYER_ID', str(self.players[0].name))
        data = data.replace('DATA', str(len(self.players[1].hand)))

        cliente1.sendall(data.encode())
    
        data = 'HAND | PLAYER_ID |   |   |   |   |   | DATA | STRING_DECK |  '
        hand = self.get_cards_stringfied(self.players[1].hand)
        data = data.replace('STRING_DECK', hand)
        data = data.replace('PLAYER_ID', str(self.players[1].name))
        data = data.replace('DATA', str(len(self.players[0].hand)))

        cliente2.sendall(data.encode())

    def send_start_game(self, cliente1, cliente2):
        data = 'START_GAME | PLAYER_ID |   | PREVIOUS_CARD |   |   |   | DATA |  | NEXT_PLAYER'
        data = data.replace('PREVIOUS_CARD', self.previous_card.get_card_str())
        data = data.replace('PLAYER_ID', str(self.players[0].name))
        data = data.replace('NEXT_PLAYER', str(self.turn_player.name))
        data = data.replace('DATA', str(len(self.players[1].hand)))

        cliente1.sendall(data.encode())
    
        data = 'START_GAME | PLAYER_ID |   | PREVIOUS_CARD |   |   |   | DATA |  | NEXT_PLAYER'
        data = data.replace('PREVIOUS_CARD', self.previous_card.get_card_str())
        data = data.replace('PLAYER_ID', str(self.players[1].name))
        data = data.replace('NEXT_PLAYER', str(self.turn_player.name))
        data = data.replace('DATA', str(len(self.players[0].hand)))

        cliente2.sendall(data.encode())

        self.started = True
    
    def get_cards_stringfied(self, deck):
        deck_stringfied:str = ""
        for card in deck:
            deck_stringfied += f"{card.number} {card.color}, " 
        return deck_stringfied    
      
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = list()
    
    def add_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        #find card in hand, get index and remove

        for i in range(0, len(self.hand)):
            if self.hand[i].number == card.number and self.hand[i].color == card.color:
                self.hand.pop(i)
                break


    def print_hand(self):
        for card in self.hand:
            print(card.get_card_str())

class Card:
    def __init__(self, color, value):
        self.color = color
        self.number = value
    
    def get_card_str(self):
        if self.color == None:
            return f"{self.number} white"
        return f"{self.number} {self.color}"
    
    def print_card(self):
        print(colored(self.number, self.color), end=' ')

def format_data(data):
    data = data.split(' | ')
    return data
    
def server():   
    game = Game()
    
    # Cria um socket e associa ao host e porta especificados
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((HOST, PORT))

    # Escuta por conexões
    servidor_socket.listen()
    
    os.system('clear')
    
    titulo = 'UNO - Servidor'
    linha = '-' * 50
    subtitulo1 = '== Servidor iniciado com sucesso =='
    subtitulo2 = '== Aguardando conexões =='
    
    print(titulo.center(50))
    print(linha.center(50))
    print(subtitulo1.center(50))
    print(subtitulo2.center(50))
    print(linha.center(50))
    
    while len(game.players) < 2:
        texto_jogadores = '== Aguardando pelos jogadores =='
        print(texto_jogadores.center(50))
        
        # Aceita a primeira conexão
        cliente1, endereco1 = servidor_socket.accept()
        print('Cliente 1 conectado:', endereco1)
        player1 = Player(endereco1[1])
        game.players.append(player1)

        # Aceita a segunda conexão
        cliente2, endereco2 = servidor_socket.accept()
        print('Cliente 2 conectado:', endereco2)
        player2 = Player(endereco2[1])
        game.players.append(player2)

        texto_conectados = '== Todos jogadores conectados =='
        print(texto_conectados.center(50))
        print(linha.center(50))
        
    text_iniciando_jogo = '== Iniciando o jogo =='
    print(text_iniciando_jogo.center(50))
    
    texto_distribuindo_cartas = '== Distribuindo cartas =='
    print(texto_distribuindo_cartas.center(50))
    
    game.send_cards(cliente1, cliente2)

    texto_cartas_distribuidas = '== Cartas distribuidas =='
    print(texto_cartas_distribuidas.center(50))

    game.setup_game()

    texto_jogo_iniciado = '== Jogo iniciado =='
    print(texto_jogo_iniciado.center(50))

    texto_carta_na_mesa = '== Carta na mesa  =='
    print(texto_carta_na_mesa.center(50))
    game.previous_card.print_card()

    print('\n')
    texto_jogador_inicial = '== Jogador inicial =='
    print(texto_jogador_inicial.center(50))
    print(game.turn_player.name)

    game.send_start_game(cliente1, cliente2)

    print(linha.center(50))

    # Loop infinito para receber e enviar mensagens
    while True:

        # Recebe mensagem do cliente 1
        while game.started:
            mensagem1 = cliente1.recv(1024).decode()
            print(mensagem1)
            
            if mensagem1:
                print('Cliente 1:', mensagem1)
                # Envia mensagem para o cliente 1
                formatted_message = format_data(mensagem1)
                if formatted_message[0] == "CARD_PUT":
                    card_to_put = formatted_message[2]
                    card_to_put = card_to_put.split(' ')
                    card_to_put = Card(card_to_put[0], card_to_put[1])
                    if(card_to_put.color == game.previous_card.color or card_to_put.number == game.previous_card.number):
                        if (game.turn_player == game.players[1]):
                            game.turn_player = game.players[0]
                        else:
                            game.turn_player = game.players[1]

                        game.previous_card = card_to_put
                        game.players[0].remove_card(card_to_put)
                        data = 'ATT_CARD | PLAYER_ID |   | PREVIOUS_CARD |   |   | STATUS | DATA | STRING_DECK | NEXT_PLAYER'
                        data = data.replace('PREVIOUS_CARD', game.previous_card.get_card_str())
                        data = data.replace('PLAYER_ID', str(game.players[0].name))
                        data = data.replace('NEXT_PLAYER', str(game.turn_player.name))
                        data = data.replace('DATA', str(len(game.players[1].hand)))
                        data = data.replace('STRING_DECK', " ")
                        data = data.replace('STATUS', 'Success')
                        cliente1.sendall(data.encode())

                        string_deck = ""

                        if card_to_put.number == "draw2":
                            for i in range(0, 2):
                                new_card = game.random_card()
                                game.players[1].add_card(new_card)
                                string_deck += new_card.get_card_str() + ", "
                            string_deck = string_deck[:-2]

                        data = 'ATT_CARD | PLAYER_ID |   | PREVIOUS_CARD |   |   | STATUS | DATA | STRING_DECK | NEXT_PLAYER'
                        data = data.replace('PREVIOUS_CARD', game.previous_card.get_card_str())
                        data = data.replace('PLAYER_ID', str(game.players[1].name))
                        data = data.replace('NEXT_PLAYER', str(game.turn_player.name))
                        data = data.replace('DATA', str(len(game.players[0].hand)))
                        data = data.replace('STRING_DECK', string_deck)
                        data = data.replace('STATUS', 'Success')
                        print(data)
                        cliente2.sendall(data.encode())

                elif formatted_message[0] == 'BUY_CARD':
                    if (game.turn_player == game.players[1]):
                        game.turn_player = game.players[0]
                    else:
                        game.turn_player = game.players[1]
                    string_deck = ""
                    data = 'CARDS_BUYED | PLAYER_ID | PREVIOUS_CARD |   |   |   | STATUS | DATA | STRING_DECK | NEXT_PLAYER'
                    print('Cliente 1 está comprando cartas...')
                    cards_buyed = game.buy_cards()
                    if len(cards_buyed) == 0:
                        print("Cliente 1 não comprou cartas")
                        string_deck = "no cards"
                    else:
                        print('Cliente 1 comprou ', len(cards_buyed), ' cartas')
                        for card in cards_buyed:
                            string_deck += card.get_card_str() + ', '
                            game.players[0].add_card(card)
                        
                        string_deck = string_deck[:-2]
                    print("Cliente 1 jogou: ", game.previous_card.get_card_str())
                    
                    data = data.replace('STRING_DECK', string_deck)
                    data = data.replace('PLAYER_ID', str(game.players[0].name))
                    data = data.replace('NEXT_PLAYER', str(game.turn_player.name))
                    data = data.replace('PREVIOUS_CARD', game.previous_card.get_card_str())
                    data = data.replace('DATA', str(len(game.players[1].hand)))
                    data = data.replace('SUCCESS', 'Success')
                    print(data)
                    cliente1.sendall(data.encode())
                    
                    string_deck = 'empty'

                    data = 'CARDS_BUYED | PLAYER_ID | PREVIOUS_CARD |   |   |   | STATUS | DATA | STRING_DECK | NEXT_PLAYER'
                    data = data.replace('STRING_DECK', string_deck)
                    data = data.replace('PLAYER_ID', str(game.players[1].name))
                    data = data.replace('NEXT_PLAYER', str(game.turn_player.name))
                    data = data.replace('PREVIOUS_CARD', game.previous_card.get_card_str())
                    data = data.replace('DATA', str(len(game.players[0].hand)))
                    data = data.replace('SUCCESS', 'Success')
                    print(data)
                    cliente2.sendall(data.encode())

            mensagem2 = cliente2.recv(1024).decode()
            print(mensagem2)
            if mensagem2:
                print('Cliente 2:', mensagem2)
                # Envia mensagem para o cliente 2
                formatted_message = format_data(mensagem2)
                if formatted_message[0] == "CARD_PUT":
                    card_to_put = formatted_message[2]
                    card_to_put = card_to_put.split(' ')
                    card_to_put = Card(card_to_put[0], card_to_put[1])
                    if(card_to_put.color == game.previous_card.color or card_to_put.number == game.previous_card.number):
                        if (game.turn_player == game.players[1]):
                            game.turn_player = game.players[0]
                        else:
                            game.turn_player = game.players[1]

                        string_deck = ""
                        
                        if card_to_put.number == "draw2":
                            for i in range(0, 2):
                                new_card = game.random_card()
                                game.players[0].add_card(new_card)
                                string_deck += new_card.get_card_str() + ", "
                            string_deck = string_deck[:-2]

                        game.previous_card = card_to_put
                        game.players[1].remove_card(card_to_put)
                        data = 'ATT_CARD | PLAYER_ID |   | PREVIOUS_CARD |   |   | STATUS | DATA | STRING_DECK | NEXT_PLAYER'
                        data = data.replace('PREVIOUS_CARD', game.previous_card.get_card_str())
                        data = data.replace('PLAYER_ID', str(game.players[0].name))
                        data = data.replace('NEXT_PLAYER', str(game.turn_player.name))
                        data = data.replace('DATA', str(len(game.players[1].hand)))
                        data = data.replace('STRING_DECK', string_deck)
                        data = data.replace('STATUS', 'Success')
                        cliente1.sendall(data.encode())
                        data = 'ATT_CARD | PLAYER_ID |   | PREVIOUS_CARD |   |   | STATUS | DATA |   | NEXT_PLAYER'
                        data = data.replace('PREVIOUS_CARD', game.previous_card.get_card_str())
                        data = data.replace('PLAYER_ID', str(game.players[1].name))
                        data = data.replace('NEXT_PLAYER', str(game.turn_player.name))
                        data = data.replace('DATA', str(len(game.players[0].hand)))
                        data = data.replace('STRING_DECK', " ")
                        data = data.replace('STATUS', 'Success')
                        cliente2.sendall(data.encode())

                elif formatted_message[0] == 'BUY_CARD':
                    if (game.turn_player == game.players[1]):
                        game.turn_player = game.players[0]
                    else:
                        game.turn_player = game.players[1]

                    string_deck_2 = ""
                    print('Cliente 2 está comprando cartas...')
                    cards_buyed = game.buy_cards()
                    if len(cards_buyed) == 0:
                        print("Cliente 2 não comprou cartas")
                        string_deck_2 = "no cards"
                    else:
                        print('Cliente 2 comprou ', len(cards_buyed), ' cartas')
                        for card in cards_buyed:
                            string_deck_2 += card.get_card_str() + ', '
                            game.players[1].add_card(card)
                        
                        string_deck_2 = string_deck_2[:-2]

                    string_deck = 'empty'
                    data = 'CARDS_BUYED | PLAYER_ID | PREVIOUS_CARD |   |   |   | STATUS | DATA | STRING_DECK | NEXT_PLAYER'
                    data = data.replace('STRING_DECK', string_deck)
                    data = data.replace('PLAYER_ID', str(game.players[0].name))
                    data = data.replace('NEXT_PLAYER', str(game.turn_player.name))
                    data = data.replace('PREVIOUS_CARD', game.previous_card.get_card_str())
                    data = data.replace('DATA', str(len(game.players[1].hand)))
                    data = data.replace('SUCCESS', 'Success')
                    print(data)
                    cliente1.sendall(data.encode())

                    data = 'CARDS_BUYED | PLAYER_ID | PREVIOUS_CARD |   |   |   | STATUS | DATA | STRING_DECK | NEXT_PLAYER'
                    print("Cliente 2 jogou: ", game.previous_card.get_card_str())
                    
                    data = data.replace('STRING_DECK', string_deck_2)
                    data = data.replace('PLAYER_ID', str(game.players[1].name))
                    data = data.replace('NEXT_PLAYER', str(game.turn_player.name))
                    data = data.replace('PREVIOUS_CARD', game.previous_card.get_card_str())
                    data = data.replace('DATA', str(len(game.players[0].hand)))
                    data = data.replace('SUCCESS', 'Success')
                    print(data)
                    cliente2.sendall(data.encode())


            
if __name__ == '__main__':
    server()
