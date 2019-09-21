import socket

TCP_IP = '10.42.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024 * 1024 * 10
with open("studentID.jpg","rb") as f:
    MESSAGE = f.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print("Message sent!")
