from socket import socket, AF_INET, SOCK_DGRAM

ADDRESS1 = "192.168.137.8" # IPaddress
ADDRESS2 = "192.168.137.9" # IPaddress
ADDRESS3 = "192.168.137.10" # IPaddress
ADDRESS4 = "192.168.137.11" # IPaddress
ADDRESS5 = "192.168.137.12" # IPaddress
ADDRESS6 = "192.168.137.13" # IPaddress
#ADDRESS = "127.0.0.1" # IPaddress
PORT = 10000

s = socket(AF_INET, SOCK_DGRAM)
while True:
    msg = input("> ")
    s.sendto(msg.encode(), (ADDRESS1, PORT))
s.close()