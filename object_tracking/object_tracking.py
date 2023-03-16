import cv2
import sys
import os
import socket
import numpy as np
import time
import base64
import struct
from datetime import datetime

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

TH = 1500

def receive_frame(client_socket):
    BUFF_SIZE = 524288
    full_packet, _ = client_socket.recvfrom(BUFF_SIZE)
    udp_header = full_packet[:8]
    packet = full_packet[8:]
    data = base64.b64decode(packet, ' /')
    stringData = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(stringData, 1)
    return frame

def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    n = 0
    while True:
        frame = receive_frame(client_socket)
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):
        # if n == 0:
            cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)
            n += 1
        # elif key == ord('q'):
        elif n == 1:
            break

    cv2.destroyWindow(window_name)

def tracking(client_socket):
    # Set up tracker.
    # Instead of CSRT, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
             tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.legacy.TrackerMOSSE_create()
        elif tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    # Create CSRT tracker object
    tracker = cv2.TrackerCSRT_create()

    # Set initial bounding box coordinates
    bbox = None

    while True:
        # Capture frame from webcam
        frame = receive_frame(client_socket)

        # If bounding box is not set, prompt user to select object to track
        if bbox is None:
            # ROI box background image
            img = cv2.imread("data/roi_sel/roi_sel_img_0.jpg")
        
            # Uncomment the line below to select a different bounding box
            bbox = cv2.selectROI(img, False)
        
            # Initialize tracker with first frame and bounding box
            tracker.init(frame, bbox)

        # Update tracker with new frame
        success, bbox = tracker.update(frame)

        # If tracking was successful, draw bounding box around object
        if success:
            # Calculate size of object in camera's field of view based on distance
            distance = 100  # Example distance in cm from camera
            object_width = bbox[2]  # Width of object in pixels
            fov_width = 60  # Example field of view width in degrees
            pixel_width = frame.shape[1]  # Width of frame in pixels
            size_in_fov = (object_width / pixel_width) * fov_width
            actual_size = (size_in_fov / 360) * (2 * distance * 100)  # Multiply by 2 to get diameter of object
            
            # Draw bounding box with adjusted size
            bbox = tuple(map(int, bbox))
            cv2.rectangle(frame, bbox, (0, 255, 0), 2)

            # Extract the x, y coordinates of the bounding box
            x, y, w, h = [int(i) for i in bbox]
            center_x, center_y = x + w // 2, y + h // 2

            # Calculate the center zone boundaries
            center_zone_width = 0.2  # example width of center zone as a fraction of the frame width
            center_zone_left = int((1 - center_zone_width) / 2 * frame.shape[1])
            center_zone_right = int((1 + center_zone_width) / 2 * frame.shape[1])

            # Determine if bounding box is in left, right or center zone
            if center_x < center_zone_left:
                print("Bounding box is in left zone.")
                if TH > actual_size:
                    print("Too far")
                    cv2.putText(frame, f"Too far, left zone", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    print("Too close")
                    cv2.putText(frame, f"Too close, left zone", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif center_zone_left <= center_x <= center_zone_right:
                print("Bounding box is in center zone.")
                if TH > actual_size:
                    print("Too far")
                    cv2.putText(frame, f"Too far, center zone", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    print("Too close")
                    cv2.putText(frame, f"Too close, center zone", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                print("Bounding box is in right zone.")
                if TH > actual_size:
                    print("Too far")
                    cv2.putText(frame, f"Too far, right zone", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    print("Too close")
                    cv2.putText(frame, f"Too close, right zone", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display frame with bounding box
        cv2.imshow("Frame", frame)

        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Add this code to create and set up a UDP socket
    BUFF_SIZE = 524288
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_ip = 'raspberrypi.local'
    print(host_ip)
    port = 9999
    message = b'Hope you get this'
    client_socket.sendto(message, (host_ip, port))

    save_frame_camera_key(0, 'data/roi_sel', 'roi_sel_img')
    tracking(client_socket)
