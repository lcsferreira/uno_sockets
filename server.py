import socket
import threading
import random
import time
from socket import *
import sys
import json

from termcolor import colored


if len(sys.argv) > 1:
    MAX_PLAYERS = int(sys.argv[1])
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])
else:
    MAX_PLAYERS = 2
    server_ip = '127.0.0.1'
    server_port = 5555

# Global current move
current_move = None


def update_client(connection_socket=None, ID=None):
    # Mensagem antiga (n usando dict)
    '''mes = ''
    if ID is not None:
        mes += 'ID ' + str(ID) + '/'
    if connection_socket is not None:
        mes += 'HAND ' + str(game.players[ID].get_hand()) + '/'
    mes += 'TURN ' + str(game.player_turn) + '/'
    if len(game.discards) > 0:
        mes += 'LAST ' + str(game.discards[-1].name) + '/'
    else:
        mes += 'LAST ' + 'None' + '/'
    mes += 'PNUM ' + str(game.num_players) + '/'
    mes += 'PNUMC ' + str(game.att_ncards_players())
    print(mes)'''
    # Mensagem nova (usando dict)
    global sockets_connected
    mes = dict()

    if ID is not None:
        mes['ID'] = ID
    if connection_socket is not None:
        mes['HAND'] = game.players[ID].get_hand()
    mes['TURN'] = game.player_turn
    if len(game.discards) > 0:
        mes['LAST'] = game.discards[-1].name
    mes['PNUM'] = game.num_players
    mes['PNUMC'] = game.att_ncards_players()
    mes['DRS'] = game.draw_sum
    mes['MAX'] = MAX_PLAYERS

    if connection_socket is None:
        for socket in sockets_connected:
            socket.send(json.dumps(mes).encode())
    else:
        connection_socket.send(json.dumps(mes).encode())


def server_client(connection_socket, ID):

    global current_move, sockets_connected
    __update_client_lock.acquire()
    update_client(connection_socket, ID)
    __update_client_lock.release()

    # Segura players pre game
    __game_started.acquire()
    while not game.started:
        __game_started.release()
        time.sleep(0.5)
        __game_started.acquire()
    __game_started.release()

    while game.started:
        print(f'Client {ID} here')
        __update_client_lock.acquire()
        update_client(connection_socket, ID)
        __update_client_lock.release()
        while game.player_turn != ID:
            time.sleep(0.5)

        print(f'Client {ID} here')
        print('Thread server_client waiting player ', ID, ' turn...')
        try:
            sentence = connection_socket.recv(1024)
        except Exception as msg:
            print("Caught exception: %s" % msg)
            break
        # No data receiving
        if sentence is None:
            print('No data receiving')
            continue

        # Byte -> String
        sentence = sentence.decode() #aqui é o que chega do cliente, para o servidor
        if len(sentence.split(',')) < 3 or len(sentence.split(',')) > 3:
            continue

        # SKIP: 0,
        # BUY: 0,
        # PUT: BLUE 8 0
        #
        print(sentence)

        # Verifica procedencia dos comandos
        skip, buy, put = sentence.split(',', 3) # ValueError: too many values to unpack (expected 3) (sometimes)
        if len(put.split()) < 3:
            connection_socket.send('Invalid syntax of uno protocol.'.encode())
            continue
        garbage, colour, value, wild = put.split(None, 3)
        print('skip: ', skip)
        print('buy: ', buy)
        print('put: ', put)
        card = None
        print(buy)
        if skip == ' SKIP: 0':
            code = 'skip'
        elif buy == ' BUY: 1':
            code = 'buy'
        elif put != ' PUT: 0 0 0':
            if wild != '0':
                card = Card(colour=colour, wild=wild)
            else:
                card = Card(colour, value)
            code = 'put'
        else:
            code = 'exit'

        __current_move_lock.acquire()

        current_move = (code, card)

        __current_move_lock.release()

        time.sleep(0.2)

    # for socket in sockets_connected:
    #    socket.close()


def server():

    global current_move
    global game
    global sockets_connected
    game = Game()

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(4)
    server_socket.settimeout(180)

    sockets_connected = []
    threads_in_execution = []

    # Espera por players
    while (not game.started) and (game.num_players < MAX_PLAYERS):

        if game.num_players != 0:
            __game_started.release()

        __update_client_lock.acquire()
        update_client()
        __update_client_lock.release()

        print("Waiting for players, has current ", game.num_players, ' players...')
        client_socket, client_info = server_socket.accept()
        sockets_connected.append(client_socket)

        # Adiciona jogadores até o jogo começar
        game.add_player(Player(game.num_players, client_info[0], client_info[1]))

        print("Socket connected: ", client_info[-1])
        # Retorna o ID do jogador
        threads_in_execution.append(threading.Thread(target=server_client, args=(sockets_connected[-1], game.players[-1].id, )))
        threads_in_execution[-1].start()
        time.sleep(0.1)
        __game_started.acquire()

    __update_client_lock.acquire()
    game.start()
    update_client()
    __game_started.release()
    __update_client_lock.release()

    print('=== Game running ===')
    while game.started:
        __current_move_lock.acquire()
        if current_move is None:
            # print('Current move is: ', current_move)
            __current_move_lock.release()
            time.sleep(0.1)
        else:
            print('Current move is: ', current_move)
            game.play(current_move[0], current_move[1])
            current_move = None
            __update_client_lock.acquire()
            update_client()
            __update_client_lock.release()
            __current_move_lock.release()
    # Reinicar game ***

class Game:
    def __init__(self):
        self.num_players = 0
        self.players = list()
        self.uno_deck = self.shuffle_deck(self.build_deck())
        self.discards = list()
        self.player_turn = 0
        self.play_direction = 1

        self.started = False
        self.max_players = MAX_PLAYERS
        self.draw_sum = 0
        self.tunr_list = [x for x in range(self.max_players)]

    def add_player(self, player):
        if self.num_players >= self.max_players:
            return False
        else:
            player.id = self.num_players
            self.players.append(player)
            self.num_players += 1
            return True

    def att_ncards_players(self):
        return [len(player.hand) for player in self.players]

    def build_deck(self):
        deck = list()
        colours = ['red', 'blue', 'green', 'yellow']
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'draw_two', 'skip', 'reverse']
        for colour in colours:
            for value in values:
                card = Card(colour, value)
                deck.append(card)
                if value != '0':
                    card = Card(colour, value)
                    deck.append(card)
        for i in range(4):
            deck.append(Card(wild='wild_'+str(i)))
            deck.append(Card(wild='wild_draw_four_'+str(i)))
        return deck

    def shuffle_deck(self, deck):
        for card_pos in range(len(deck)):
            rand_pos = random.randint(0, 107)
            deck[card_pos], deck[rand_pos] = deck[rand_pos], deck[card_pos]
        return deck

    def draw_cards(self, num_cards):
        cards_draw = list()
        for i in range(num_cards):
            cards_draw.append(self.uno_deck.pop())
        return cards_draw

    def discard_card(self, card):
        index_card = self.players[self.player_turn].hand.index(card)
        self.discards.append(card)
        del (self.players[self.player_turn].hand[index_card])

    def next_player_turn(self):
        last_card = self.discards[-1]
        if last_card.value == 'skip':
            if (self.player_turn + (2*self.play_direction)) >= self.max_players:
                next_player = abs(self.player_turn+(2*self.play_direction)) - self.max_players
            elif (self.player_turn + (2*self.play_direction)) < 0:
                next_player = self.max_players + self.player_turn - (2*self.play_direction)
            else:
                next_player = self.player_turn + (2 * self.play_direction)
        else:
            next_player = self.player_turn + (1 * self.play_direction)
            if next_player < 0:
                next_player = self.max_players - 1
            elif next_player > (self.max_players - 1):
                next_player = 0
        self.player_turn = next_player

    def can_play(self, card):
        if self.draw_sum > 0:
            if self.discards[-2].wild is not None:
                if 'wild_draw_four' in self.discards[-2].wild:
                    if card.wild is not None:
                        if 'wild_draw_four' in card.wild:
                            return True
                        else:
                            return False
                    else:
                        return False
            else:
                if 'draw_two' in self.discards[-1].value:
                    if card.value == 'draw_two':
                        return True
                    else:
                        return False
        last_colour = self.discards[-1].colour
        last_value = self.discards[-1].value

        if card.value == last_value or card.colour.lower() in last_colour.lower()or last_colour.lower() in card.colour.lower()  or card.wild is not None:
            return True
        else:
            return False

    def start(self):
        print('Game started!')
        game.started = True
        self.discards.append(self.uno_deck.pop())
        while self.discards[-1].wild is not None or str(self.discards[-1].value).isalpha():
            self.discards.append(self.uno_deck.pop())

        print('First card is: ', self.discards[-1].colour, ' - ', self.discards[-1].value)

        for player in self.players:
            for i in range(7):
                card = self.uno_deck.pop()
                while card.value == None or card.colour == None:
                    card = self.uno_deck.pop()
                player.hand.append(card)

        print('Cards: ')
        for player in self.players:
            for card in player.hand:
                print(card.value, ' - ', card.colour)
                print('card of player[', player.ID, '] : ', colored(card.value, card.colour), ' - ',  card.wild)

    def play(self, move, card):
        if move == 'buy':
            if self.draw_sum > 0:
                for i in range(self.draw_sum ):
                    self.players[self.player_turn].hand.append(self.uno_deck.pop())
                self.draw_sum = 0
            else:
                self.players[self.player_turn].hand.append(self.uno_deck.pop())

        elif move == 'put':
            print(f'can play {self.can_play(card)}')
            if self.can_play(card) and self.players[self.player_turn].put_card(card):
                self.discards.append(card)
                if self.discards[-1].wild is not None:
                    if 'wild_draw_four' in self.discards[-1].wild:
                        self.discards[-1].apply_effects()
                    self.discards.append(Card(card.colour, ''))

                print('PLAYED!: ', card.colour, '-', card.value, '-', card.wild)
                self.discards[-1].apply_effects()
            else:
                print('Cannot play: ', card.colour, '-', card.value, '-', card.wild)
                return

        # Verifica vitoria
        if len(self.players[self.player_turn].hand) == 0:
            print(f'Player {self.player_turn} venceu!')
            self.started = False
            return

        # Faz o efeito da carta e vai para próximo jogador
        self.next_player_turn()
        print('Last placed card is: ', self.discards[-1].colour, ' - ', self.discards[-1].value, ' - ', self.discards[-1].wild)
        print('Player turn is: ', self.player_turn)
        print('Cards: ')
        for player in self.players:
            for att_card in player.hand:
                print('card of player[', player.ID, '] : ',  att_card.colour, ' - ',  att_card.value, ' - ',  att_card.wild)


class Player:
    def __init__(self, ID=None, IP=None, port=None):
        self.ID = ID
        self.IP = IP
        self.port = port
        self.hand = list()

    # def get_card(self, card):
    
    
    # def get_color(self):
    
    def get_hand(self):
        return [card.name for card in self.hand]

    def put_card(self, card):
        for actual_card in self.hand:
            if card.wild is not None and actual_card.wild is not None:
                if (actual_card.wild in card.wild) or (card.wild in actual_card.wild):
                    self.hand.remove(actual_card)
                    return True
            if actual_card.colour == card.colour.lower() and actual_card.value == card.value:
                self.hand.remove(actual_card)
                return True
        else:
            return False


class Card:
    def __init__(self, colour=None, value=None, wild=None):
        self.colour = colour
        self.value = value
        self.wild = wild
        if wild is None:
            self.name = self.colour + " " + self.value
        else:
            self.name = self.wild
        if value == 'reverse' or value == 'skip' or wild is not None or 'draw_two' in value:
            self.effect = True
        else:
            self.effect = False

    def apply_effects(self):
        if self.effect:
            if self.value == 'reverse':
                game.play_direction *= -1
            elif self.value == 'skip':
                # Done in game.next_player_turn()
                pass
            elif self.wild is not None:
                if 'wild_draw_four' in self.wild:
                    game.draw_sum += 4
                    print('Draw_sum: ', game.draw_sum)
            elif 'draw_two' in self.value:
                game.draw_sum += 2
                print('Draw_sum: ', game.draw_sum)


if __name__ == '__main__':
    game = Game()
    __current_move_lock = threading.Lock()
    __game_started = threading.Lock()
    __update_client_lock = threading.Lock()
    server()
