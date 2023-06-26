#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
#host = socket.gethostname() # Get local machine name
host = "192.168.178.100"
port = 5560            # Reserve a port for your service.

s.connect((host, port))
print (s.recv(1024))
s.close()                     # Close the socket when done