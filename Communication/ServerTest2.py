# This is server code to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64


BUFF_SIZE = 524288
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

host_ip = '127.0.0.1'
socket_address = (host_ip, 9999)
print(host_ip)

server_socket.bind(socket_address)
print('Listening at:',socket_address)

vid = cv2.VideoCapture(0)

while True:
	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
	print('connected from',client_addr)
	
	while(vid.isOpened()):
		temp,frame = vid.read()
		frame = imutils.resize(frame, width = 600)
		#frame = cv2.resize(frame, (720, 480))
		encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
		message = base64.b64encode(buffer)
		server_socket.sendto(message,client_addr)
	
		cv2.imshow('TRANSMITTING VIDEO',frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			server_socket.close()
			break
		
