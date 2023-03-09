import random
import socket
from termcolor import colored

# server = "localhost"
# port = 5555

# class Client:
#     def __init__(self):
#         self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.connection.connect((server, port))
#     def server_output(self):
#       while 1:
#           att = self.connection.recv(1500)
#           att = att.decode()
#           print(att)
#           #if att.type == "ALLOW_PLAY"
#             #msg = input("informe a carta que você quer jogar")
#             #self.send_message(msg
#     def send_message(self, message):
#         self.connection.send(message.encode())
class Card:
    def __init__(self, color, value):
        self.color = color
        self.number = value
    
    def get_card_str(self):
        print(colored(self.number, self.color))
    
def generate_deck():
    deck = []
    colors = ["red", "blue", "green", "yellow"]
    for color in colors:
        for i in range(1, 10):
            deck.append(Card(color, i))
    random.shuffle(deck)
    return deck

def print_deck(deck):
    for card in deck:
        card.get_card_str()

def draw_player_hand(deck):
    player_hand = list()

    for i in range (0, 7):
        player_hand.append(deck.pop())

    return player_hand

   #for each card in the deck check if the card is the same as the card to remove 
def remove_card( card: str, deck: list):

    print("deck_temp")
    print_deck(deck)
    print("----")
    for c in deck[:]:
        if str(c) == card:
            deck.remove(c)
            return deck
    return deck
        
def client_program():
    host = "localhost" # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    #get the second part of the tuple, which is the port number
    player_id = client_socket.getsockname()[1]
    player_hand = list()

    print("Your ID is: ", player_id)

    #check if connection was succesful
    if client_socket:
      print("Connection was succesful")
    else:
      print("Connection failed")

    print("Welcome to UNO! Type 'start' to start the game")
    print("Type 'quit' to exit")

    message = input("-> ")  # take input

    while message.lower().strip() != 'quit':
      if(message == "start"):
        data_to_server = "START_GAME" + " | " + str(player_id)
        client_socket.send(data_to_server.encode())
        data = client_socket.recv(1024).decode()

        print('Received from server: ' + data)

        format_data = data.split(" | ")

        if(format_data[0] == "GAME_STARTED"):
          print("Table card is:", format_data[1])
          player_hand = draw_player_hand(generate_deck())
          print("Your hand is: ")
          print_deck(player_hand)

        message = input("Type 'put' to put a card ")  # again take input

      elif(message == "put"):
        print("Your hand is: ")
        print_deck(player_hand)
        card_to_put = input("Which card do you want to put? ")
        data_to_server = "PUT_CARD" + " | " + str(player_id) + " | " + card_to_put
        client_socket.send(data_to_server.encode())
        data = client_socket.recv(1024).decode()
        print('Received from server: ' + data)
        format_data = data.split(" | ")
        if(format_data[2] == "sucess"):
          print("Card was put sucessfully")
          card_remove = Card(card_to_put.split(" ")[0], card_to_put.split(" ")[1])
          #iterates to find the card in the player hand and remove it
          for c in player_hand[:]:
            if str(c.number) == str(card_remove.number) and c.color == card_remove.color:
              player_hand.remove(c)
              break
          #print the new hand
          print("Your hand is: ")
          print_deck(player_hand)
        else:
          print("Card don`t match the table card")
        message = input("Type 'put' to put a card ")  # again take input
      else:
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection
    
if __name__ == '__main__':
    client_program()
