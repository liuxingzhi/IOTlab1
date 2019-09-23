import socket
import os
import random

# os.system("rm 123.png; touch 123.png")
UDP_IP = '10.42.0.1'
UDP_PORT = 5005
UDP_BUFFER_SIZE = 1024

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2.bind((UDP_IP, UDP_PORT))
# s.listen(1)

# conn, addr = s.accept()
# print("connection address:", addr)
# random.randint(0, 1)
s2.sendto(str(1).encode("UTF-8"), ("10.42.0.237", 5005))
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
while True:
    # s.sendto(str(1).encode("UTF-8"), ("10.42.0.237", 5005))
    try:
        distance, address = s2.recvfrom(UDP_BUFFER_SIZE)
        # if not data:
        #     break
        # with open("123.png", "ab") as f:
        #     f.write(data)
        # s.sendto("received".encode("UTF-8"), address)
        if distance:
            print(distance, int(distance.decode()))

            s2.sendto(str(1).encode("UTF-8"), address)
    except:
        pass
# conn.close()
