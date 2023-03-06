# import random
# from socket import *
# from _thread import *
# from game import Game

# from helpers import create_all_cards
# from player import Player

# host = gethostname()
# port = 55551

# print(f'host: {host}, port: {port}')

# serverSocketPlayer = []

# for i in range(0, 4):
#     serverSocketPlayer.append(socket(AF_INET, SOCK_STREAM))
#     serverSocketPlayer[i].bind((host, port + (i + 1)))
    
#     print(f'Socket player {i}:', serverSocketPlayer[i])

# server = socket(AF_INET, SOCK_STREAM)

# try:
#     server.bind((host, port))
# except socket.error as e:
#     str(e)

# server.listen(4)

# print("Waiting for a connection, Server Started")
  
# def generate_card_for_players():
#     cards = create_all_cards()
#     random.shuffle(cards)
#     return cards[0:11] 
      
# def generate_players():
#     hand = []
#     players = []
#     for i in range(1, 5):
#         hand = generate_card_for_players()
#         players.append(Player(f"Player {i}", hand[i]))
#         print(f"Player {i} created!")

# while True:
#     for i in range(0, 4):
#         serverSocketPlayer[i].listen(4)
#         print("Waiting for a connection, Server Started")
#         connection, address = serverSocketPlayer[i].accept()
#         print("Connected to: ", address)

#         message = connection.recv(2048).decode()
    
#     if (message == 'INICIAR_SALA'):
#         print("Aguardando conexão dos jogadores...")
#         # game = Game()
#         print("ENTROU")
        
                
#     # connection, address = server.accept()
#     # print("Connected to: ", address)

#     # message = connection.recv(2048).decode()
    
from socket import *
from _thread import *
import sys

server = 'localhost'
port = 5555

s = socket(AF_INET, SOCK_STREAM)

server_ip = gethostbyname(server)
print("Server IP: ", server_ip)

try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))
    
s.listen(4)

print("Waiting for a connection...")

def threaded_client(conn):
    global message
    conn.send(str.encode("Connected"))
    reply = ""
    
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            
            if not data:
                conn.send(str.encode("Server: Bye"))
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)
                
            conn.sendall(str.encode(reply))
        except:
            break
        
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    
    start_new_thread(threaded_client, (conn,))