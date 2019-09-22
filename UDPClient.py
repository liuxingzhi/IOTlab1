import socket

UDP_IP = '10.42.0.1'
UDP_PORT = 5005
BUFFER_SIZE = 1024 * 1024 * 10
# with open("studentID.jpg","rb") as f:
#     MESSAGE = f.read()
MESSAGE = b"hello!!!"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((UDP_IP, UDP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print("Message sent!")
