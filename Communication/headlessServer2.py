import socket
import numpy as np
import time
import base64
import RPi.GPIO as GPIO
import cv2, imutils
from datetime import datetime
import struct
import os

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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

host_ip = 'raspberrypi.local'
socket_address = (host_ip, 9999)
print(host_ip)

server_socket.bind(socket_address)
print('Listening at:', socket_address)

GPIO.output(mov0, GPIO.LOW)
GPIO.output(mov1, GPIO.LOW)
GPIO.output(mov2, GPIO.LOW)

# Starts in manual mode
GPIO.output(switch, GPIO.LOW)

vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FPS, 20)

previous_timeframe = 0
new_timeframe = 0

# Run OpenCV in headless mode
os.environ['DISPLAY'] = ':0'
os.environ['PYVISTA_OFF_SCREEN'] = 'true'

while True:

    # open vid
    while(vid.isOpened()):
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('connected from', client_addr)

        if msg == 'Hope you get this':
            msg = b'x'

        # Control motor
        if msg == b'w':
            GPIO.output(mov0, GPIO.LOW)
            GPIO.output(mov1, GPIO.LOW)
            GPIO.output(mov2, GPIO.HIGH)
        elif msg == b'a':
            GPIO.output(mov0, GPIO.LOW)
            GPIO.output(mov1, GPIO.HIGH)
            GPIO.output(mov2, GPIO.LOW)
        elif msg == b'd':
            GPIO.output(mov0, GPIO.LOW)
            GPIO.output(mov1, GPIO.HIGH)
            GPIO.output(mov2, GPIO.HIGH)
        elif msg == b'q':
            GPIO.output(mov0, GPIO.HIGH)
            GPIO.output(mov1, GPIO.LOW)
            GPIO.output(mov2, GPIO.LOW)
        elif msg == b'e':
            GPIO.output(mov0, GPIO.HIGH)
            GPIO.output(mov1, GPIO.LOW)
            GPIO.output(mov2, GPIO.HIGH)
        elif msg == b'x':
            GPIO.output(mov0, GPIO.LOW)
            GPIO.output(mov1, GPIO.LOW)
            GPIO.output(mov2, GPIO.LOW)
        elif msg == b'p':
            if switch_state == 0:
                GPIO.output(switch, GPIO.HIGH)
                switch_state = 1
            else:
                GPIO.output(switch, GPIO.LOW)
                switch_state = 0
        else:
            pass

        while(vid.isOpened()):

            temp,frame = vid.read()
            
            fps2 = int(vid.get(cv2.CAP_PROP_FPS))
            print("fps:", fps2)

            # resize vid
            frame = imutils.resize(frame, width = 500)
            #frame = cv2.resize(frame, (720, 480))

            #downscale quality
            encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])

            #encode to base64 (bytes)
            message = base64.b64encode(buffer)

            # get current time in seconds
            dt = datetime.now()
            ts = datetime.timestamp(dt)

            # pack time in header
            udp_header = struct.pack('d', ts)

            # add header and franes and send
            message = udp_header + message
            server_socket.sendto(message,client_addr)
            
            # math to get FPS
            new_timeframe = time.time()
            fps = 1/(new_timeframe-previous_timeframe)
            previous_timeframe=new_timeframe
            fps=int(fps)
