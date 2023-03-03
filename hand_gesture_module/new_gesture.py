import cv2
import tensorflow as tf
import mediapipe as mp
import numpy as np

# Define the hand gesture classes
GESTURE_CLASSES = ['fist', 'open', 'left', 'right']

# Load the trained model
model = tf.keras.models.load_model('hand_gesture_model.h5')

# Initialize the hand landmark model
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Start the video stream
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB color
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect the hand landmarks in the frame
    results = mp_hands.process(frame)

    # If hand landmarks are detected
    if results.multi_hand_landmarks:
        # Get the coordinates of the hand landmarks
        hand_landmarks = results.multi_hand_landmarks[0].landmark
        hand_landmarks_array = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks])

        # Normalize the coordinates
        hand_landmarks_array[:, 0] = hand_landmarks_array[:, 0] * frame.shape[1]
        hand_landmarks_array[:, 1] = hand_landmarks_array[:, 1] * frame.shape[0]

        # Resize the frame to match the input shape of the model
        frame_resized = cv2.resize(frame, (224, 224))

        # Normalize the pixel values of the image
        frame_normalized = frame_resized / 255.0

        # Add a batch dimension to the image
        frame_batch = np.expand_dims(frame_normalized, axis=0)

        # Predict the hand gesture using the trained model
        gesture_probabilities = model.predict(frame_batch)[0]
        gesture_index = np.argmax(gesture_probabilities)
        gesture_label = GESTURE_CLASSES[gesture_index]

        # Display the gesture label on the frame
        cv2.putText(frame, gesture_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Hand Gesture Recognition', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    # Check for quit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()
