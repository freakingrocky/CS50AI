import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # Initializing 2 empty lists
    images = []
    labels = []

    # Iterating through all the folders in the directory
    for folder in os.listdir(data_dir):
        # Iterating through all the images in the folder
        for image_path in os.listdir(os.path.join(data_dir, folder)):
            # Reading the image
            image = cv2.imread(os.path.join(data_dir, folder, image_path),
                               cv2.IMREAD_COLOR)
            # Resizing the image
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT),
                               interpolation=cv2.INTER_AREA)
            # Adding image to images list
            images.append(image)
            # Adding corresponding label to the label list (i.e. folder name)
            labels.append(int(folder))

    # Return the images & labels list
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    """Refer to the README.md for the details."""
    model = tf.keras.models.Sequential([
        # Convolutional Layer with 43 fiters, 3*3 kernel, relu activation
        tf.keras.layers.Conv2D(
            43, (3, 3), activation="relu",
            input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        # Convolutional Layer with 43 fiters, 3*3 kernel, relu activation
        tf.keras.layers.Conv2D(
            43, (3, 3), activation="relu",
            input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Convolutional Layer with 43 fiters, 3*3 kernel, relu activation
        tf.keras.layers.Conv2D(
            43, (3, 3), activation="relu",
            input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Max Pooling using 3*3 matrix
        tf.keras.layers.MaxPooling2D(pool_size=3),
        # Flatten units
        tf.keras.layers.Flatten(),
        # Add 2 hidden layers with dropouts in each layer
        tf.keras.layers.Dense(200, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(200, activation="relu"),
        tf.keras.layers.Dropout(0.1),

        # Final layer
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Training the neural network
    model.compile(
        optimizer="adamax",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    # Return the model
    return model


if __name__ == "__main__":
    main()
