# This is client code to receive video frames over UDP
import socket
import numpy as np
import time
import base64

from pynput.keyboard import Key, Listener

BUFF_SIZE = 524288
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_ip = '192.168.0.111'
print(host_ip) 
port = 9999
message = b'Connection successful'

client_socket.sendto(message,(host_ip,port))

def on_press(key):
    #print('{0} pressed'.format(
        #key))
    check_key(key)

def on_release(key):
    #print('{0} release'.format(
       # key))
    if key == Key.esc:
        # Stop listener
        return False
    client_socket.sendto(b'x',(host_ip,port))

def check_key(key):
    if key.char == 'w':
        print(key)
        client_socket.sendto(b'w',(host_ip,port))
    elif key.char == 'a':
        print(key)
        client_socket.sendto(b'a',(host_ip,port))
    elif key.char == 's':
        print(key)
        client_socket.sendto(b's',(host_ip,port))
    elif key.char == 'd':
        print(key)
        client_socket.sendto(b'd',(host_ip,port))
    elif key.char == 'q':
        print(key)
        client_socket.sendto(b'q',(host_ip,port))
    elif key.char == 'e':
        print(key)
        client_socket.sendto(b'e',(host_ip,port))
    elif key.char == 'z':
        print(key)
        client_socket.sendto(b'z',(host_ip,port))
    elif key.char == 'c':
        print(key)
        client_socket.sendto(b'c',(host_ip,port))
    elif key.char == 'x':
        print(key)
        client_socket.sendto(b'x',(host_ip,port))

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
