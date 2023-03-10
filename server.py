import random
import socket


# server = "127.0.0.1"
# port = 65432
# MAX_PLAYERS = 2

class Game:
    def __init__(self):
        self.deck = list()
        self.players = list()
        self.turn_player = 0
        self.previous_card = None
        self.is_clockwise = True
        self.has_winner = False
    
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
    # get the hostnam
    game = Game()
    host = "localhost"
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    while not game.has_winner:
        # receive data stream. it won't accept data packet greater than 1024 bytes
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

if __name__ == '__main__':
  server_program()
      
# class Server:
#     def __init__(self,server, port):
#       self.game = Game()
#       self.server = server
#       self.port = port
#       self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#       self.server_socket.bind((self.server, self.port))
#       self.server_socket.listen(MAX_PLAYERS)
#       self.sockets_connected = list()

#     def play(self):
#       self.game.create_deck()
#       self.game.shuffle_cards()

#       while (len(self.game.players) < MAX_PLAYERS):
#         print("Waiting for players, has current ", len(self.game.players), ' players...')
#         client_socket, client_info = self.server_socket.accept()
#         self.sockets_connected.append(client_socket)
#         print(client_info[0], client_info[1])
#         # Adiciona jogadores até o jogo começar
#         self.game.add_player(Player("Player " + str(len(self.game.players) + 1)))
#         self.send_hand_player(self.game.players[0])

#         print("Socket connected: ", client_info[-1])

#       print("==== Game started ====")

#       while (not self.game.has_winner):
#         self.allow_play(self.game.turn_player)
#         try:
#             sentence = self.connection_socket.recv(1024)
#         except Exception as msg:
#             print("Caught exception: %s" % msg)
#             break
#         # No data receiving
#         if sentence is None:
#             print('No data receiving')
#             continue

#         # Byte -> String
#         sentence = sentence.decode()
#         self.receive_message(sentence)

#     def receive_message(self, msg):
#         if msg.type == "PLAY_CARD":
#           msg.card = self.game.players[msg.player].remove_card(msg.data)
#           self.game.previous_card = msg.card
#           self.remove_card_player(msg.player, msg.card)
#           self.game.next_player()
#         elif msg.type == "DRAW_CARD":
#           self.game.players[msg.player].add_card(self.game.deck.pop())
#           self.add_card_player(msg.player, self.game.deck.pop())
#           self.game.next_player()
#         elif msg.type == "CHANGE_CLOCKWISE":
#           self.change_clockwise()
#           self.game.next_player()
#         elif msg.type == "WINNER":
#           self.game.has_winner = True

#     def change_clockwise(self):
#       self.game.reverse_game()

#     def send_hand_player(self, player):
#       player_hand = self.game.draw_player_hand()
#       msg = {
#         "type": "SEND_HAND",
#         "data": player_hand,
#         "player": player
#       }
#       self.send_data(msg)

#     def remove_card_player(self, player, card):
#       msg = {
#         "type": "REMOVE_CARD",
#         "data": card,
#         "player": player
#       }
#       self.send_data(msg)

#     def add_card_player(self, player, card):
#       msg = {
#         "type": "ADD_CARD",
#         "data": card,
#         "player": player
#       }
#       self.send_data(msg)

#     def allow_play(self, player):
#       msg = {
#         "type": "ALLOW_PLAY",
#         "player": player,
#         "previous_card": self.game.previous_card
#       }
#       self.send_data(msg)
         
#     #server send message function
#     def send_data(self, data):
#       print(data)
#       self.connection_socket.send(data.encode())