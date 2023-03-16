import cv2
import mediapipe as mp
import math

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
def is_hand_open(hand_landmarks):
    # Check distance between thumb and index finger
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2 + (thumb_tip.z - index_tip.z)**2)
    # Check if index and thumb are both extended
    if (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y and
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y):
        return "Open"
    else:
        return "Closed"

# Start capturing frames from webcam
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7) as hands:

    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for natural selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert image to RGB for mediapipe processing
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run the hand detection model on the image
        results = hands.process(image)

        # Draw landmarks and predict hand status and direction on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks)
                hand_status = is_hand_open(hand_landmarks)
                cv2.putText(frame, hand_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the image with landmarks and hand status overlaid
        cv2.imshow("Hand Landmarks", frame)

        # Exit program when 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()