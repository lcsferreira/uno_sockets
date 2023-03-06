import random
from socket import *
from _thread import *
from game import Game

from helpers import create_all_cards
from player import Player

host = gethostname()
port = 55551

print(f'host: {host}, port: {port}')

serverSocketPlayer = []

for i in range(0, 4):
    serverSocketPlayer.append(socket(AF_INET, SOCK_STREAM))
    serverSocketPlayer[i].bind((host, port + (i + 1)))
    
    print(f'Socket player {i}:', serverSocketPlayer[i])

server = socket(AF_INET, SOCK_STREAM)

try:
    server.bind((host, port))
except socket.error as e:
    str(e)

server.listen(2)

print("Waiting for a connection, Server Started")
  
def generate_card_for_players():
    cards = create_all_cards()
    random.shuffle(cards)
    return cards[0:11] 
      
def generate_players():
    hand = []
    players = []
    for i in range(1, 5):
        hand = generate_card_for_players()
        players.append(Player(f"Player {i}", hand[i]))
        print(f"Player {i} created!")

while True:
    for i in range(0, 4):
        serverSocketPlayer[i].listen(4)
        print("Waiting for a connection, Server Started")
        connection, address = serverSocketPlayer[i].accept()
        print("Connected to: ", address)

        message = connection.recv(2048).decode()
    
    if (message == 'INICIAR_SALA'):
        print("Aguardando conexão dos jogadores...")
        # game = Game()
        print("ENTROU")
        
                
    # connection, address = server.accept()
    # print("Connected to: ", address)

    # message = connection.recv(2048).decode()
    
        
