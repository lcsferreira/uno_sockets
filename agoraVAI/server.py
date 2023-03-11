import random
import socket
import time

# Configurações do servidor
HOST = 'localhost'
PORT = 7000
# data_Decks = 'HAND | PLAYER_ID | CARD_TO_PUT | PREVIOUS_CARD | NUMBER | SET_COLOR | STATUS | DATA | STRING_DECK | NEXT_PLAYER'

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
        card_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "skip", "reverse", "draw2", "draw4", "wild"]
        card_colors = ["blue", "red", "yellow", "green"]

        for value in card_values:
            if value == "wild" or value == "draw4":
                card = Card(None, value)
                continue
            for color in card_colors:
                card = Card(color, value)
                self.deck.append(card)
    
    def random_card(self):
        return random.choice(self.deck)
    
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
        
        self.started = True
        
    def send_cards(self, cliente1, cliente2):
        self.setup_player()
        
        data = 'HAND | PLAYER_ID |   |   |   |   |   |   | STRING_DECK |  '
        hand = self.get_cards_stringfied(self.players[0].hand)
        data = data.replace('STRING_DECK', hand)
        data = data.replace('PLAYER_ID', str(self.players[0].name))
        cliente1.sendall(data.encode())
    
        self.setup_player()
    
        data = 'HAND | PLAYER_ID |   |   |   |   |   |   | STRING_DECK |  '
        hand = self.get_cards_stringfied(self.players[1].hand)
        data = data.replace('STRING_DECK', hand)
        data = data.replace('PLAYER_ID', str(self.players[1].name))
        cliente2.sendall(data.encode())
    
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
        self.hand.remove(card)

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
    
def server():   
    game = Game()
    
    # Cria um socket e associa ao host e porta especificados
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((HOST, PORT))

    # Escuta por conexões
    servidor_socket.listen()
    
    print('Servidor aguardando conexões...')
    
    while len(game.players) < 2:
        print('Aguardando pelos jogadores, atualmente contém', len(game.players), 'jogadores')
        
        # Aceita a primeira conexão
        cliente1, endereco1 = servidor_socket.accept()
        print('Cliente 1 conectado:', endereco1)
        player1 = Player(endereco1[1])
        game.players.append(player1)

        print('Aguardando pelos jogadores, atualmente contém', len(game.players), 'jogadores')

        # Aceita a segunda conexão
        cliente2, endereco2 = servidor_socket.accept()
        print('Cliente 2 conectado:', endereco2)
        player2 = Player(endereco2[1])
        game.players.append(player2)
        
    print('Todos jogadores conectados, iniciando o jogo!')
    
    print('Distribuindo cartas...')
    
    game.send_cards(cliente1, cliente2)

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
            
if __name__ == '__main__':
    server()
