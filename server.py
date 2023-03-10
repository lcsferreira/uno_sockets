import random
import socket
import threading
import time

# server = "127.0.0.1"
# port = 65432
# MAX_PLAYERS = 2

# global game_started

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

def print_deck(deck):
    for card in deck:
        card.get_card_str()

def get_cards_stringfied(deck):
    deck_stringfied:str = ""
    for card in deck:
        deck_stringfied += f"{card.number} {card.color}, " 
    return deck_stringfied    

def server_program():
    game = Game()
    host = "localhost"
    port = 5000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind((host, port))
    server_socket.listen(2)
    
    sockets_connected = []
    threads_in_execution = []
    
    while (not game.started) and (len(game.players) < 2):
        if (len(game.players) != 0):
            _game_started.release()
        
        print("Waiting for player, has current ", len(game.players), "players...")
        
        conn, address = server_socket.accept()
        sockets_connected.append(conn)
        
        game.players.append(address[1])
        
        print("Socket connected: ", address[-1])
        
        threads_in_execution.append(threading.Thread(target=server_client, args=(conn, address[1], game)))
        threads_in_execution[-1].start()
        time.sleep(0.1)
        _game_started.acquire()
        
    _update_client_lock.acquire()
    game_started = True
    connect_player(sockets_connected[0], game)
    # talvez colocar o update client aqui?
    _game_started.release()
    _update_client_lock.release()
    
def connect_player(conn, game):

    while game.has_winner == False:
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
          
        format_data = data.split(" | ")

        if(format_data[0] == "START_GAME"):
            game.create_deck()
            game.shuffle_cards()
            game.previous_card = game.deck.pop()
            conn.send(("GAME_STARTED | " + game.previous_card.get_card_str() ).encode())  # send data to the client
        elif(format_data[0] == "PUT_CARD"):
            card = Card(format_data[2].split(" ")[0], format_data[2].split(" ")[1])
                        
            if(card.number == "wild"):
                if(format_data[5] == "blue"):
                    card.color = "blue"
                elif (format_data[5] == "red"):
                    card.color = "red"
                elif (format_data[5] == "yellow"):
                    card.color = "yellow"
                else:
                    card.color = "green"
                game.previous_card = card
                conn.send(("CARD_ATT | " + game.previous_card.get_card_str() + " | sucess").encode())
            
            if(game.previous_card.color == card.color or game.previous_card.number == card.number):
                game.previous_card = card
                conn.send(("CARD_ATT | " + game.previous_card.get_card_str() + " | sucess").encode())
                
            else:
                conn.send(("CARD_ATT | " + game.previous_card.get_card_str() + " | fail").encode())
        
        elif(format_data[0] == "BUY_CARD"):
            buy_cards = list()
            new_card = game.random_card()
            need_buy = True

            while need_buy == True:
                buy_cards.append(new_card)
                new_card = game.random_card()
                if(new_card.color == game.previous_card.color):
                    need_buy = False
                elif(new_card.number == game.previous_card.number):
                    need_buy = False
                else:
                    need_buy = True
            string_deck = get_cards_stringfied(buy_cards)
            #remove last comma
            string_deck = string_deck[:-2]
            conn.send(("CARDS_BUYED | " + format_data[1] + " | " + string_deck + " | success").encode())
            #PADRONIZAR O PROTOCOLO
        elif(format_data[0] == "DRAW_CARD"):
            buy_cards = list()
            
            if format_data[3] == "2":
                for i in range(0, 2):
                    buy_cards.append(game.random_card())
                
            if format_data[3] == "4":
                for i in range(0, 4):
                    buy_cards.append(game.random_card())
                    
            string_deck = get_cards_stringfied(buy_cards)
            string_deck = string_deck[:-2]
            conn.send(("CARDS_BUYED | " + format_data[1] + " | " + string_deck + " | success" + 'PLAYER_NEXT_TURN').encode())              

    conn.close()  # close the connection

def server_client(connection_socket, player_id, game):
    # _game_started.acquire()
    # while not game.started:
    #     _game_started.release()
    #     time.sleep(0.5)
    #     _game_started.acquire()
    # _game_started.release()

    while game.started:
        print(f'Client {player_id} here')
        print('Thread server_client waiting player ', player_id, ' turn...')
    
        try:
            message = connection_socket.recv(1024)
        except Exception as msg:
            print("Caught exception socket.error : %s" % msg)
            break
        
        if message is None:
            print("No data received")
            continue
        
        connect_player(connection_socket, game)
        # message = message.decode()
        # print(f'Client {player_id} sent: {message}')
    
if __name__ == '__main__':
    _current_move_lock  = threading.Lock()
    _game_started = threading.Lock()
    _update_client_lock = threading.Lock()
    server_program()
