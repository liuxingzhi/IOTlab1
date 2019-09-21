import socket
import os
import sh

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind((UDP_IP, UDP_PORT))
# s.listen(1)

# conn, addr = s.accept()
# print("connection address:", addr)
while True:
    try:
        data, address = s.recvfrom(BUFFER_SIZE)
        if not data:
            print("no data")
        else:
            # with open("123.png", "ab") as f:
            #     f.write(data)
            print(data)
            s.sendto("received".encode("UTF-8"), address)
    except:
        pass
# conn.close()
