import numpy as np
from PIL import Image
import os

# Set the path to the directory containing the hand images
path_to_images = 'training_images'

# Define the shape of the input images
image_shape = (224, 224, 3)

# Load the hand images into a NumPy array
images = []
for filename in os.listdir(path_to_images):
    img = Image.open(os.path.join(path_to_images, filename))
    img = img.resize(image_shape[:-1])
    img_array = np.array(img)
    images.append(img_array)

# Convert the list of images to a NumPy array
images = np.array(images)

# Save the NumPy array to a file
np.save('train_images.npy', images)
