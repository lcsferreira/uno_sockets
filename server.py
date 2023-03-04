from socket import *
from _thread import *
import sys

host = gethostname()
port = 55551

print(f'host: {host}, port: {port}')

server = socket(AF_INET, SOCK_STREAM)

try:
    server.bind((host, port))
except socket.error as e:
    str(e)

server.listen(4)

print("Waiting for a connection, Server Started")

connected = set()

def threaded_client(con, p):
    con.send(str.encode(str(p)))
    
    while True:
        try:
            data = con.recv(2048).decode()
            
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", data)
            
        except:
            break


while True:
    con, adr = server.accept()
    
    msg = con.recv(1024)
    reply = msg.decode("utf-8")
    
    if not msg:
        print("Disconnected")
        break
    else:
        print("Received: ", msg.decode("utf-8"))
    


# def threaded_client():
#     reply = ""
    
#     while True:
#         try:
#             data = conn.recv(2048)
#             reply = data.decode("utf-8")
            
#             if not data:
#                 print("Disconnected")
#                 break
#             else:
#                 print("Received: ", reply)
#                 print("Sending: ", reply)
                
#             con.sendall(str.encode(reply))
#         except:
#             break
        
#     print("Lost connection")
#     con.close()
         
# while True:
#     conn, addr = server.accept()
#     print("Connected to: ", addr)
    
#     start_new_thread(threaded_client, (conn,))    