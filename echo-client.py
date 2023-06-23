# echo-client.py
# Win Terminal $netstat -ano

import socket

HOST = "192.168.178.101"  # The server's hostname or IP address
PORT = 65432 # The port used by the server 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Conncting")
    s.connect((HOST, PORT))
    print("connected")
    s.sendall(b"BalticMaterials")
    data = s.recv(1024)

print(f"Received {data!r}")