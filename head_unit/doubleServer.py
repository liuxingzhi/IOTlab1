import socket
import os
import signal
import cv2
from detect import Detect
from typing import List
import numpy as np
from time import time
import inspect

count_img = 1
count_dis = 1
count_led = 1

# debug purpose
def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


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


# @timeit
# decode image from video stream
def decode_numpy_array(data, d: Detect):
    arr = np.frombuffer(data, np.uint8)
    try:
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    except (cv2.error, UnicodeDecodeError) as e:
        print("wrong at img decoding!!!", lineno())

    global count_img
    try:
        img, label = d.detect(img)
    except (cv2.error, UnicodeDecodeError) as e:
        print("wrong at detection", lineno())

    # cv2.imshow("Camera", img)
    # if cv2.waitKey(1) & 0xff == ord('q'):
    #     return
    succ = cv2.imwrite(os.path.join("data", "{count_img}.jpg").format(count_img=count_img),
                       cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    print(succ)
    count_img += 1
    return label


# prepare opencv and GPU
with Detect() as d:
    os.system("rm -r data; mkdir data")
    os.system("rm -r distance; mkdir distance")
    TCP_IP = '10.42.0.1'
    # TCP_IP = '127.0.0.1'
    TCP_PORT = 5006
    TCP_BUFFER_SIZE = 655535

    UDP_IP = '10.42.0.1'
    UDP_PORT = 5005
    UDP_BUFFER_SIZE = 1024

    ###### initialize TCP server
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s1.bind((TCP_IP, TCP_PORT))
    s1.listen(1)
    conn, addr = s1.accept()
    print("connection address:", addr)

    ###### initialize UDP server
    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2.bind((UDP_IP, UDP_PORT))
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ARDUINO_ADDR = ("10.42.0.237", 5005)
    img_data = b""
    count = 0
    t1 = time()
    s2.sendto(str(False).encode("UTF-8"), ARDUINO_ADDR)
    while True:
        size = 0
        try:
            data = conn.recv(TCP_BUFFER_SIZE)
            if not data:
                break
            if data.startswith(b"NEXT IMAGE"):
                try:
                    print("NEXT IMAGE")
                    # t2 = time()
                    # print("network time ", t2 - t1)
                    # t1 = time()
                    try:
                        label = decode_numpy_array(img_data, d)
                    except Exception as e:
                        print(str(e), "numpy decode error", lineno())

                    try:
                        distance, address = s2.recvfrom(UDP_BUFFER_SIZE)
                        if label and int(distance.decode()) <= 200:
                            s2.sendto(str(label).encode("UTF-8"), ARDUINO_ADDR)
                        else:
                            s2.sendto(str(False).encode("UTF-8"), ARDUINO_ADDR)
                    except:
                        print("arduino sending error", lineno())

                    print(label, distance, int(distance.decode()))
                    # print("HOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWw!")
                    img = np.ones((80, 250, 3)) * 255
                    img = cv2.putText(img, distance.decode() + " cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                      (255, 0, 0), 2)
                    print(cv2.imwrite(os.path.join("data", "distance{count_dis}.jpg").format(count_dis=count_dis), img),
                          "distance status")
                    # print("HATTTTTTTTTTTTTTTTTTTTTTTTT")
                    count_dis += 1

                    if label and int(distance.decode()) <= 200:
                        LED = "ON"
                    else:
                        LED = "OFF"
                    img = np.ones((80, 200, 3)) * 255
                    img = cv2.putText(img, LED, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print(cv2.imwrite(os.path.join("data", "LED{count_led}.jpg").format(count_led=count_led), img),
                          "LED status")
                    count_led += 1
                    print("=================================")
                    # if distance:
                    #     print(distance, int(distance.decode()))
                    #     s2.sendto(str(label).encode("UTF-8"), address)
                    img_data = b""
                except:
                    print("failed at next img trasition,", lineno())

            elif data.startswith(b"Bye"):
                break
            elif data.startswith(b"SIZE"):
                # if img_data:
                #     # if decode_numpy_array(img_data, d):
                #     #     print(True)
                #     # else:
                #     #     print(False)
                #     print("impossible here")
                try:
                    size = int(data.decode().split()[-1])
                except:
                    print("size decode error", lineno())

                print("received bytes: ", size)
                conn.send("GOT SIZE".encode())
                # img_data = b""
            else:
                # with open("123.png", "ab") as f:
                # f.write(data)
                img_data += data
                conn.send("GOT IMAGE".encode())

            count += 1
            # print(count)
            # conn.send(f"{count}".encode())
        except Exception as e:
            print(type(e), e, lineno())

conn.close()
