# This is server code to send video frames over UDP
import socket
import time
import base64
from datetime import datetime
import struct
import numpy as np
import io
import picamera

BUFF_SIZE = 524288
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

host_ip = 'raspberrypi.local'
socket_address = (host_ip, 9999)
print(host_ip)

server_socket.bind(socket_address)
print('Listening at:',socket_address)

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 24
    time.sleep(2)
    stream = io.BytesIO()
    for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
        stream.seek(0)
        message = base64.b64encode(stream.getvalue())
        
        # get current time in seconds
        dt = datetime.now()
        ts = datetime.timestamp(dt)

        # pack time in header
        udp_header = struct.pack('d', ts)

        # add header and frames and send
        message = udp_header + message
        server_socket.sendto(message, socket_address)

        # reset stream for next frame
        stream.seek(0)
        stream.truncate()

        # put fps on screen
        fps = int(camera.framerate)
        print("fps:", fps)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break
