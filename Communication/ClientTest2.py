# This is client code to receive video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64
import struct
from datetime import datetime

BUFF_SIZE = 524288
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_ip = '127.0.0.1'
print(host_ip) 
port = 9999
message = b'Hope you get this'

client_socket.sendto(message,(host_ip,port))
previous_timeframe = 0
new_timeframe = 0



while True:

	# Recieve packet
	full_packet,temp = client_socket.recvfrom(BUFF_SIZE)

	#get header
	udp_header = full_packet[:8]

	#get data
	packet = full_packet[8:]

	#unpack header
	udp_header = struct.unpack('d', udp_header)

	#decode video
	data = base64.b64decode(packet,' /')
	stringData = np.frombuffer(data, dtype=np.uint8) 
	#npdata = np.fromstring(data,dtype=np.uint8)
	frame = cv2.imdecode(stringData,1)
	
	# Used to get FPS
	new_timeframe = time.time()
	fps = 1/(new_timeframe-previous_timeframe)
	previous_timeframe=new_timeframe
	fps=int(fps)

	# used to get latency
	dt = datetime.now()
	ts = datetime.timestamp(dt)

	# putting text on the window
	cv2.putText(frame,str(fps),(10,30), cv2.FONT_HERSHEY_SIMPLEX,1,(25,255,0),4)
	cv2.putText(frame, "S Time: " + str(udp_header[0]) + "s",(10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(25,255,0), 2)
	cv2.putText(frame, "C Time: " + str(ts) + "s",(10,80) , cv2.FONT_HERSHEY_SIMPLEX, 0.5,(25,255,0), 2)
	cv2.putText(frame, "Delay: " + str(ts-udp_header[0]) + "s",(10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(25,255,0), 2)

	# Display video
	cv2.imshow("CLIENT VIDEO",frame)
	
	# Press q to exit the window
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		client_socket.close()
		break
