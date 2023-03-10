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
      if self.color == None:
        print(colored(self.number, "white"))
      else:
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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
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

        print("Type 'quit' to quit game")
        print("Type 'buy' to buy cards")
        print("Type 'put' to put a card ")
        message = input(' -> ')  # again take input

      elif(message == "put"):
        print("Your hand is: ")
        print_deck(player_hand)
        card_to_put = input("Which card do you want to put? ")
        
        if card_to_put == "draw2":
          data_to_server = "DRAW_CARD" + " | " + str(player_id) + " | " + card_to_put + " | " + "2"
          client_socket.send(data_to_server.encode())
          data = client_socket.recv(1024).decode()
          print('Received from server: ' + data)
          format_data = data.split(" | ")
          
        if card_to_put == "draw4":
          data_to_server = "DRAW_CARD" + " | " + str(player_id) + " | " + card_to_put + " | " + "4"
          client_socket.send(data_to_server.encode())
          data = client_socket.recv(1024).decode()
          print('Received from server: ' + data)
          format_data = data.split(" | ")
          
        if card_to_put == "wild":
          set_color = input("Set the color: ")
          if set_color == "red" or set_color == "blue" or set_color == "green" or set_color == "yellow":
            data_to_server = "PUT_CARD" + " | " + str(player_id) + " | " + card_to_put + " | " + set_color
            client_socket.send(data_to_server.encode())
            data = client_socket.recv(1024).decode()
            print('Received from server: ' + data)
            format_data = data.split(" | ")
               
          
        
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
          print("Type 'quit' to quit game")
          print("Type 'buy' to buy cards")
          print("Type 'put' to put a card ")
          message = input(' -> ')  # again take input
  
        else:
         print("Card don`t match the table card")
         print("Type 'quit' to quit game")
         print("Type 'buy' to buy cards")
         print("Type 'put' to put a card ")
         message = input(' -> ')  # again take input  # again take input
        
      elif(message == "buy"):
        print("You don't have a card to play, drawing...")
        data_to_server = "BUY_CARD" + " | " + str(player_id)
        client_socket.send(data_to_server.encode())
        data = client_socket.recv(1024).decode()
        
        print('Received from server: ' + data)
        
        format_data = data.split(" | ")
        print(format_data)
        
        if(format_data[3] == "success"):
          print("Card was bought sucessfully")
          all_cards = format_data[2].split(", ")
          for card in all_cards:
             player_hand.append(Card(card.split(" ")[1], card.split(" ")[0]))
          print("Your hand is: ")
          print_deck(player_hand)
          print("Type 'quit' to quit game")
          print("Type 'buy' to buy cards")
          print("Type 'put' to put a card ")
          message = input(' -> ')  # again take input
        else:
          print("Something went wrong!")
          print("Type 'quit' to quit game")
          print("Type 'buy' to buy cards")
          print("Type 'put' to put a card ")
          message = input(' -> ')  # again take input
        
        
      else:
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection
    
if __name__ == '__main__':
    client_program()
