# This is server code to send video frames over UDP
import socket
import numpy as np
import time
import base64


#0000STOP
#0001STRAIGHT
#0010BACK
#0011LEFT
#0100RIGHT
#0101LEFTC
#0110RIGHTC
#0111LEFTB
#1000RIGHTB
import RPi.GPIO as GPIO

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

mov0 = 5
mov1 = 6
mov2 = 13
mov3 = 19

GPIO.setup(mov0, GPIO.OUT) # mov0 pin set as output
GPIO.setup(mov1, GPIO.OUT) # mov1 pin set as output
GPIO.setup(mov2, GPIO.OUT) # mov2 pin set as output
GPIO.setup(mov3, GPIO.OUT) # mov3 pin set as output

BUFF_SIZE = 524288
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

host_ip = '192.168.0.111'
socket_address = (host_ip, 9999)
print(host_ip)

server_socket.bind(socket_address)
print('Listening at:',socket_address)

# vid = cv2.VideoCapture(0)
GPIO.output(mov0, GPIO.LOW)
GPIO.output(mov1, GPIO.LOW)
GPIO.output(mov2, GPIO.LOW)
GPIO.output(mov3, GPIO.LOW)

while True:
	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
	print('connected from',client_addr)
	if msg == b'w':
		print('w')
		GPIO.output(mov0, GPIO.LOW)
		GPIO.output(mov1, GPIO.LOW)
		GPIO.output(mov2, GPIO.LOW)
		GPIO.output(mov3, GPIO.HIGH)
	elif msg == b's':
		print('s')
		GPIO.output(mov0, GPIO.LOW)
		GPIO.output(mov1, GPIO.LOW)
		GPIO.output(mov2, GPIO.HIGH)
		GPIO.output(mov3, GPIO.LOW)
	elif msg == b'a':
		print('a')
		GPIO.output(mov0, GPIO.LOW)
		GPIO.output(mov1, GPIO.LOW)
		GPIO.output(mov2, GPIO.HIGH)
		GPIO.output(mov3, GPIO.HIGH)
	elif msg == b'd':
		print('d')
		GPIO.output(mov0, GPIO.LOW)
		GPIO.output(mov1, GPIO.HIGH)
		GPIO.output(mov2, GPIO.LOW)
		GPIO.output(mov3, GPIO.LOW)
	elif msg == b'q':
		print('q')
		GPIO.output(mov0, GPIO.LOW)
		GPIO.output(mov1, GPIO.HIGH)
		GPIO.output(mov2, GPIO.LOW)
		GPIO.output(mov3, GPIO.HIGH)
	elif msg == b'e':
		print('e')
		GPIO.output(mov0, GPIO.LOW)
		GPIO.output(mov1, GPIO.HIGH)
		GPIO.output(mov2, GPIO.HIGH)
		GPIO.output(mov3, GPIO.LOW)
	elif msg == b'z':
		print('z')
		GPIO.output(mov0, GPIO.LOW)
		GPIO.output(mov1, GPIO.HIGH)
		GPIO.output(mov2, GPIO.HIGH)
		GPIO.output(mov3, GPIO.HIGH)
	elif msg == b'c':
		print('c')
		GPIO.output(mov0, GPIO.HIGH)
		GPIO.output(mov1, GPIO.LOW)
		GPIO.output(mov2, GPIO.LOW)
		GPIO.output(mov3, GPIO.LOW)
	elif msg == b'x':
		print('x')
		GPIO.output(mov0, GPIO.LOW)
		GPIO.output(mov1, GPIO.LOW)
		GPIO.output(mov2, GPIO.LOW)
		GPIO.output(mov3, GPIO.LOW)
