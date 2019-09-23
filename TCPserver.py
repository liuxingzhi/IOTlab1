import socket
import os
import signal
import cv2
from detect import Detect
from typing import List
import numpy as np
from time import time

count_img = 1


def timeit(func):
    """一个计时器"""
    import time
    def wrapper(*args, **kwargs):
        start = time.clock()
        response = func(*args, **kwargs)
        end = time.clock()
        print('time spend:', end - start)
        return response

    return wrapper


def sigint_handler(signum, frame):
    print("received signal {signum}, {frame}".format(signum=signum, frame=frame))
    exit(0)


signal.signal(signal.SIGINT, sigint_handler)


@timeit
def decode_numpy_array(data, d: Detect):
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    global count_img
    img, label = d.detect(img)
    # cv2.imshow("Camera", img)
    # if cv2.waitKey(1) & 0xff == ord('q'):
    #     return
    succ = cv2.imwrite(os.path.join("data", "{count_img}.jpg").format(count_img=count_img),
                       cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    print(succ)
    count_img += 1
    return label


os.system("rm -r data; mkdir data")
TCP_IP = '10.42.0.1'
# TCP_IP = '127.0.0.1'
TCP_PORT = 5006
TCP_BUFFER_SIZE = 65535

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s1.bind((TCP_IP, TCP_PORT))
s1.listen(1)

conn, addr = s1.accept()
print("connection address:", addr)
count = 0

img_data = b""

t1 = time()
with Detect() as d:
    while True:
        size = 0
        try:
            data = conn.recv(TCP_BUFFER_SIZE)
            if not data:
                break
            if data.startswith(b"NEXT IMAGE"):
                print("NEXT IMAGE")
                t2 = time()
                print("network time ", t2 - t1)
                t1 = time()
                if decode_numpy_array(img_data, d):
                    print(True)
                else:
                    print(False)
            elif data.startswith(b"Bye"):
                break
            elif data.startswith(b"SIZE"):
                if img_data:
                    if decode_numpy_array(img_data, d):
                        print(True)
                    else:
                        print(False)
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
            # print(count)
            # conn.send(f"{count}".encode())
        except Exception as e:
            print(type(e), e)
    conn.close()
