import time
import datetime
import base64
import struct
import socket
from PIL import Image
import io

BUFF_SIZE = 524288
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

host_ip = 'raspberrypi.local'
socket_address = (host_ip, 9999)
print(host_ip)

server_socket.bind(socket_address)
print('Listening at:',socket_address)

vid = None
previous_timeframe = 0
new_timeframe = 0

def make_720p():
    pass # no-op

while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    print('connected from', client_addr)

    # open video capture device
    vid = open('/dev/video0', 'rb')

    # read frames from video capture device
    while True:
        # read the frame
        frame = vid.read(640*480*3)

        # resize the frame
        frame = Image.frombytes('RGB', (640, 480), frame).resize((500, 500))

        # downscale quality
        buffer = io.BytesIO()
        frame.save(buffer, format='JPEG', quality=80)
        message = base64.b64encode(buffer.getvalue())

        # get current time in seconds
        dt = datetime.datetime.now()
        ts = datetime.datetime.timestamp(dt)

        # pack time in header
        udp_header = struct.pack('d', ts)

        # add header and frames and send
        message = udp_header + message
        server_socket.sendto(message, client_addr)

        # math to get FPS
        new_timeframe = time.time()
        fps = 1 / (new_timeframe - previous_timeframe)
        previous_timeframe = new_timeframe
        fps = int(fps)

        # put fps on screen
        print(fps)

        key = input("Press 'q' to exit...")
        if key == 'q':
            vid.close()
            server_socket.close()
            break
