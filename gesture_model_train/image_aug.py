import numpy as np
import imgaug.augmenters as iaa

# Load the hand gesture images from the train_images.npy file
images = np.load('train_images.npy')

# Define the data augmentation pipeline using the imgaug library
aug_pipeline = iaa.Sequential([
    iaa.Affine(scale=(0.5, 1.5)),
    iaa.Fliplr(0.5),
    iaa.GaussianBlur(sigma=(0, 3.0)),
    iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
])

# Apply the data augmentation pipeline to the images
aug_images = aug_pipeline(images=images)

# Save the augmented images to a new numpy array file
np.save('augmented_images.npy', aug_images)

# Load the original hand gesture images from the train_images.npy file
original_images = np.load('train_images.npy')

# Load the augmented images from the augmented_images.npy file
augmented_images = np.load('augmented_images.npy')

# Combine the original images and the augmented images into a single numpy array
combined_images = np.concatenate((original_images, augmented_images), axis=0)

# Save the combined images to a new numpy array file
np.save('combined_images.npy', combined_images)
