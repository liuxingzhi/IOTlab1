import socket
import os
import signal
import cv2
from detect import detect


def sigint_handler(signum, frame):
    print(f"received signal {signum}, {frame}")
    exit(0)


signal.signal(signal.SIGINT, sigint_handler)

os.system("rm 123.png; touch 123.png")
TCP_IP = '10.42.0.1'
TCP_PORT_1 = 5001
TCP_PORT_2 = 5002
BUFFER_SIZE = 1024 * 1024

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s1.bind((TCP_IP, TCP_PORT_1))
s1.listen(1)
s2.bind((TCP_IP, TCP_PORT_2))
s2.listen(1)

conn1, addr1 = s1.accept()
print("1 connection address:", addr1)
conn2, addr2 = s2.accept()
print("2 connection address:", addr2)

count = 0
while True:
    png_size = -1
    distance = -1
    try:
        data1 = conn1.recv(BUFFER_SIZE)
        data2 = conn2.recv(BUFFER_SIZE)
        if not data1 or not data2:
            break
        if data1.startswith(b"BYE") or data2.startswith(b"BYE"):
            break

        if data1.startswith(b"SIZE"):
            png_size = int(data1.decode().split()[-1])
            conn1.send("GOT SIZE".encode())

        if data2.startswith(b"DISTANCE"):
            distance = int(data2.decode().split()[-1])
            conn1.send("GOT DISTANCE".encode())

        if png_size == -1:
            with open("123.png", "ab") as f:
                f.write(data1)
        count += 1
        print(count)
        conn1.send(f"{count}".encode())


    except Exception as e:
        print(type(e))
conn1.close()
