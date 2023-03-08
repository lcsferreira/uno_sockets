# from socket import *

# host = gethostname()
# port = 55552

# cli = socket(AF_INET, SOCK_STREAM)
# cli.connect((host, port))

# while 1:
#     msg = input("Enter message: ")
#     cli.send(msg.encode())

import socket
import sys


class Client:
    CLIENT_IP = '127.0.0.1'
    CLIENT_PORT = 5556
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = self.CLIENT_IP
        self.port = self.CLIENT_PORT
        self. addr = (self.host, self.port)
        self.id = self.connect()
        
    def connect(self):
        print(self.addr)
        self.client.connect(self.addr)
        
        return self.client.recv(2048).decode()

    def client(self):
        return self.client

    def getID(self):
        return self.id

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return print(str(e))