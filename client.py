from socket import *

host = gethostname()
port = 55551

cli = socket(AF_INET, SOCK_STREAM)
cli.connect((host, port))

while 1:
    msg = input("Enter message: ")
    cli.send(msg.encode())