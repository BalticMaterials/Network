#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = '192.168.178.101' # Get local machine name
port = 5560               # Reserve a port for your service.
s.bind((host, port))        # Bind to the port


s.listen(10)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ('Got connection from', addr)
   c.close()                # Close the connection