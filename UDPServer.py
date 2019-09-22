import socket
import os

# os.system("rm 123.png; touch 123.png")
UDP_IP = '10.42.0.1'
UDP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((UDP_IP, UDP_PORT))
# s.listen(1)

# conn, addr = s.accept()
# print("connection address:", addr)
while True:
    try:
        data, address = s.recvfrom(BUFFER_SIZE)
        # if not data:
        #     break
        # with open("123.png", "ab") as f:
        #     f.write(data)
        # s.sendto("received".encode("UTF-8"), address)
        if data:
            print(data)
            s.sendto("received".encode("UTF-8"), address)
    except:
        pass
# conn.close()
