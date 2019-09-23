# import socket
# import cv2
#
# # TCP_IP = '10.42.0.1'
# TCP_IP = '127.0.0.1'
# TCP_PORT = 5006
# BUFFER_SIZE = 1024
# print("File read")
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
# print("Connected")
#
# vid = cv2.VideoCapture(0)
# count = 0
# while vid.isOpened():
#     count += 1
#     if count == 100:
#         count = 0
#         _, image = vid.read()
#         img_encode = cv2.imencode('.jpg', image)[1].tostring()
#         MESSAGE_SIZE = ("SIZE " + str(len(img_encode))).encode()
#         try:
#             s.sendall(MESSAGE_SIZE)
#             print("Sent size")
#             reply = s.recv(BUFFER_SIZE)
#             print("Got reply {}".format(reply.decode()))
#             if reply.startswith(b'GOT SIZE'):
#                 s.sendall(img_encode)
#                 reply = s.recv(BUFFER_SIZE)
#                 print("Got reply {}".format(reply.decode()))
#             if reply.startswith(b'GOT IMAGE'):
#                 s.sendall(b"BYE")
#                 print('Image sent')
#         finally:
#             # vid.release()
#             # s.close()
#             pass
# print("Message sent")

# ! /home/pi/Files/lab1/lab1/bin python

import socket
import cv2
TCP_IP = '127.0.0.1'
# TCP_IP = '10.42.0.1'
TCP_PORT = 5006
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("Connected")

vid = cv2.VideoCapture(0)
count = 0
while vid.isOpened():
    count += 1
    retval, image = vid.read()
    if count == 10:
        count = 0
        img_encode = cv2.imencode('.jpg', image)[1].tostring()
        MESSAGE_SIZE = ("SIZE " + str(len(img_encode))).encode()
        try:
            s.sendall(MESSAGE_SIZE)
            print("Sent size")
            reply = s.recv(BUFFER_SIZE)
            print("Got reply {}".format(reply.decode()))
            if reply.startswith(b'GOT SIZE'):
                s.sendall(img_encode)
                reply = s.recv(BUFFER_SIZE)
                print("Got reply {}".format(reply.decode()))
            if reply.startswith(b'GOT IMAGE'):
                s.sendall(b"NEXT IMAGE")
                print('Image sent')
        except:
            pass

print("Message sent")
