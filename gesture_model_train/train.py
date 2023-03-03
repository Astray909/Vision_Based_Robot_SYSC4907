import mediapipe as mp
import tensorflow as tf
import numpy as np

# Define the hand gesture classes
GESTURE_CLASSES = ['fist', 'open', 'left', 'right']

# Load the pre-built hand landmark model
mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

# Load the training data
train_images = np.load('train_images.npy')
# train_images = np.load('combined_images.npy')
train_labels = np.load('train_labels.npy')

# Define the model architecture
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(224, 224, 3)),
    tf.keras.layers.Conv2D(16, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(GESTURE_CLASSES), activation='softmax')
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(train_images, train_labels, epochs=10, validation_split=0.2)

# Save the trained model
model.save('hand_gesture_model.h5')
