import numpy as np
import pandas as pd

# Set the path to the CSV file containing the hand gesture labels
path_to_labels = 'labels.csv'

# Load the hand gesture labels into a pandas DataFrame
labels_df = pd.read_csv(path_to_labels)

# Convert the hand gesture labels to a NumPy array
labels = labels_df['gesture'].values

# Define the hand gesture classes
gesture_classes = ['fist', 'left', 'open', 'right']

# Convert the hand gesture labels to one-hot encoded vectors
one_hot_labels = np.zeros((len(labels), len(gesture_classes)))
for i, label in enumerate(labels):
    class_index = gesture_classes.index(label)
    one_hot_labels[i, class_index] = 1

# Save the one-hot encoded labels to a NumPy array file
np.save('train_labels.npy', one_hot_labels)
