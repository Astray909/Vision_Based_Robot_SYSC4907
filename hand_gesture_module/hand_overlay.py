import cv2
import mediapipe as mp
import math

import socket
import base64
import numpy as np
import struct

BUFF_SIZE = 524288
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_ip = 'raspberrypi.local'
print(host_ip) 
port = 9999
message = b'Connection successful'

client_socket.sendto(message,(host_ip,port))

# Initialize mediapipe hand model
mp_hands = mp.solutions.hands

# Initialize webcam
cap = cv2.VideoCapture(0)

# Define drawing utility function
def draw_landmarks(image, hand_landmarks):
    for landmark in hand_landmarks.landmark:
        x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

# Define function to check if hand is open or closed and pointing direction
def get_hand_status(hand_landmarks):
    # Check distance between thumb and index finger
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2 + (thumb_tip.z - index_tip.z)**2)
    # Check if index and thumb are both extended
    if (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y):
        return "open"
    else:
        return "closed"

def track_gestures():
    # Start capturing frames from webcam
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7) as hands:

        while True:
            # Receive packet
            full_packet,temp = client_socket.recvfrom(BUFF_SIZE)

            # Get header
            udp_header = full_packet[:8]

            # Get data
            packet = full_packet[8:]

            # Unpack header
            udp_header = struct.unpack('d', udp_header)

            # Decode video
            data = base64.b64decode(packet,' /')
            stringData = np.frombuffer(data, dtype=np.uint8) 
            frame = cv2.imdecode(stringData,1)

            # Flip the frame horizontally for natural selfie-view display
            frame = cv2.flip(frame, 1)

            # Convert image to RGB for mediapipe processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Run the hand detection model on the image
            results = hands.process(image)

            lo = False
            ro = False
            lc = False
            rc = False
            # Draw landmarks and predict hand status and direction on the image
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    draw_landmarks(frame, hand_landmarks)
                    hand_status = get_hand_status(hand_landmarks)
                    if hand_landmarks == results.multi_hand_landmarks[0]:
                        cv2.putText(frame, "left " + hand_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        if hand_status == "open":
                            lo = True
                            lc = False
                        else:
                            lo = False
                            lc = True
                    elif hand_landmarks == results.multi_hand_landmarks[1]:
                        cv2.putText(frame, "right " + hand_status, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        if hand_status == "open":
                            ro = True
                            rc = False
                        else:
                            ro = False
                            rc = True

            if (lo and ro):
                print("forward")
                client_socket.sendto(b'w',(host_ip,port))
            elif (lc and rc):
                print("stop")
                client_socket.sendto(b'x',(host_ip,port))
            elif (lo and rc):
                print("right")
                client_socket.sendto(b'd',(host_ip,port))
            elif (lc and ro):
                print("left")
                client_socket.sendto(b'a',(host_ip,port))

            # Show the image with landmarks and hand status overlaid
            cv2.imshow("Hand Landmarks", frame)

            # Exit program when 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    
    BUFF_SIZE = 524288
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    host_ip = 'raspberrypi.local'
    print(host_ip) 
    port = 9999
    message = b'Hope you get this'

    client_socket.sendto(message,(host_ip,port))
    previous_timeframe = 0
    new_timeframe = 0 
    track_gestures()
