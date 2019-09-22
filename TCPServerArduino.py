import socket
import os

# os.system("rm 123.png; touch 123.png")
IP = '10.42.0.1'
PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((IP, PORT))
# s.listen(1)

# conn, addr = s.accept()
# print("connection address:", addr)
while True:
    try:
        data = s.recv(BUFFER_SIZE)
        # if not data:
        #     break
        # with open("123.png", "ab") as f:
        #     f.write(data)
        # s.sendto("received".encode("UTF-8"), address)
        if data:
            print(data)
            s.send("received".encode("UTF-8"))
    except:
        pass
# conn.close()
