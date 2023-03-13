# This is server code to send video frames over UDP
import socket
import numpy as np
import time
import base64
import RPi.GPIO as GPIO

GPIO.cleanup()
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

mov0 = 5
mov1 = 6
mov2 = 13
switch = 19

switch_state = 0

GPIO.setup(mov0, GPIO.OUT) # mov0 pin set as output
GPIO.setup(mov1, GPIO.OUT) # mov1 pin set as output
GPIO.setup(mov2, GPIO.OUT) # mov2 pin set as output

GPIO.setup(switch, GPIO.OUT) # switch set to output

BUFF_SIZE = 524288
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

host_ip = 'raspberrypi.local'
socket_address = (host_ip, 9999)
print(host_ip)

server_socket.bind(socket_address)
print('Listening at:', socket_address)

# vid = cv2.VideoCapture(0)
GPIO.output(mov0, GPIO.LOW)
GPIO.output(mov1, GPIO.LOW)
GPIO.output(mov2, GPIO.LOW)

#starts in manual mode
GPIO.output(switch, GPIO.LOW)

while True:
    msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
    print('connected from',client_addr)
    #forward
    if msg == b'w':
        print('w')
        GPIO.output(mov0, GPIO.LOW)
        GPIO.output(mov1, GPIO.LOW)
        GPIO.output(mov2, GPIO.HIGH)
    #LEFT
    elif msg == b'a':
        print('a')
        GPIO.output(mov0, GPIO.LOW)
        GPIO.output(mov1, GPIO.HIGH)
        GPIO.output(mov2, GPIO.LOW)
    #RIGHT
    elif msg == b'd':
        print('d')
        GPIO.output(mov0, GPIO.LOW)
        GPIO.output(mov1, GPIO.HIGH)
        GPIO.output(mov2, GPIO.HIGH)
    #LEFT SPIN
    elif msg == b'q':
        print('q')
        GPIO.output(mov0, GPIO.HIGH)
        GPIO.output(mov1, GPIO.LOW)
        GPIO.output(mov2, GPIO.LOW)
    # RIGHT SPIN
    elif msg == b'e':
        print('e')
        GPIO.output(mov0, GPIO.HIGH)
        GPIO.output(mov1, GPIO.LOW)
        GPIO.output(mov2, GPIO.HIGH)
    #STOP
    elif msg == b'x':
        print('x')
        GPIO.output(mov0, GPIO.LOW)
        GPIO.output(mov1, GPIO.LOW)
        GPIO.output(mov2, GPIO.LOW)
        
	#SWITCH
    elif msg == b'p':
        print('switching modes')
        if switch_state == 0:
            GPIO.output(switch, GPIO.HIGH)
            switch_state = 1
        else:
            GPIO.output(switch, GPIO.LOW)
            switch_state = 0
