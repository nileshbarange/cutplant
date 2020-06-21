import socket
from time import sleep

#laptop IP address to connect to
host = '192.168.1.3'
port = 5560

def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((host, port))

def sendReceive(s, message):
    s.send(str.encode(message))
    reply = s.recv(1024)
    print("We received reply")
    print("Send closing message")
    s.send(str.encode("EXIT"))
    s.close()
    reply = reply.decode('utf-8')
    return reply

def transmit(message):
    s = setupSocket()
    response = sendReceive(s, message)


