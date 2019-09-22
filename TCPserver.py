import socket
import os
import signal
import cv2
from detect import detect
from typing import List
import numpy as np

count_img = 1


def sigint_handler(signum, frame):
    print("received signal {signum}, {frame}".format(signum=signum, frame=frame))
    exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def decode_numpy_array(data):
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    global count_img
    succ = cv2.imwrite(os.path.join("data", "{count_img}.jpg").format(count_img=count_img), detect(img))
    print(succ)
    count_img += 1


os.system("rm -r data; mkdir data")
# TCP_IP = '10.42.0.1'
TCP_IP = '127.0.0.1'
TCP_PORT = 5006
BUFFER_SIZE = 655535

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s1.bind((TCP_IP, TCP_PORT))
s1.listen(1)

conn, addr = s1.accept()
print("connection address:", addr)
count = 0

img_data = b""
while True:
    size = 0
    try:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        if data.startswith(b"NEXT IMAGE"):
            print("NEXT IMAGE")
            decode_numpy_array(img_data)
        elif data.startswith(b"Bye"):
            break
        elif data.startswith(b"SIZE"):
            if img_data:
                decode_numpy_array(img_data)
            size = int(data.decode().split()[-1])
            print("received bytes: ", size)
            conn.send("GOT SIZE".encode())
            img_data = b""
        else:
            # with open("123.png", "ab") as f:
            # f.write(data)
            img_data += data
            conn.send("GOT IMAGE".encode())

        count += 1
        print(count)
        # conn.send(f"{count}".encode())
    except Exception as e:
        print(type(e))

conn.close()
