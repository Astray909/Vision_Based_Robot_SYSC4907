from PIL import Image
import os

# Set the directory path to the folder containing the images to be resized
directory_path = "training_images"

# Set the new size for the images
new_size = (224, 224)

# Loop through each file in the directory and resize it
for filename in os.listdir(directory_path):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
        # Open the image file
        image = Image.open(os.path.join(directory_path, filename))

        # Resize the image
        resized_image = image.resize(new_size)

        # Save the resized image with the same filename
        resized_image.save(os.path.join(directory_path, filename))
