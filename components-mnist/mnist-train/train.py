from os import path

import tensorflow as tf
from tensorflow import keras


def gen_log_dirname(log_dir) -> str:
    return path.join(log_dir, "tensorboard", "fit")


def load_mnist(filepath, kind, normalize=True):
    import gzip
    import numpy as np

    """Load MNIST data from `filepath`"""
    labels_path = path.join(filepath, f"{kind}-labels-idx1-ubyte.gz")
    images_path = path.join(filepath, f"{kind}-images-idx3-ubyte.gz")

    with gzip.open(labels_path, "rb") as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)

    with gzip.open(images_path, "rb") as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(
            len(labels), 28, 28
        )

    # normalize by dividing each pixel value by 255.0. This places the pixel value within the range 0 and 1.
    if normalize:
        images = images / 255.0

    return images, labels


def learning_rate(batch_size):
    # gradually reduce the learning rate during training
    return keras.optimizers.schedules.InverseTimeDecay(
        0.001, decay_steps=batch_size * 1000, decay_rate=1, staircase=False
    )


def create_model(batch_size):
    model = keras.Sequential(
        [
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(10),
        ]
    )
    model.compile(
        optimizer=keras.optimizers.Adam(
            # learning_rate=1e-3,
            learning_rate=learning_rate(batch_size),
        ),
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    model.summary()
    return model


def train_model(
    model_dir: str,
    data_dir: str,
    log_dir: str,
    epochs: int = 5,
) -> str:  # noqa: F821
    """Trains a model and saves to model dir and returns path to tensorboard logs."""

    train_images, train_labels = load_mnist(data_dir, kind="train", normalize=True)
    test_images, test_labels = load_mnist(data_dir, kind="t10k", normalize=True)

    tensorboard_log_dir = gen_log_dirname(log_dir)

    batch_size = len(train_images)
    model = create_model(batch_size)
    model.fit(
        x=train_images,
        y=train_labels,
        epochs=epochs,
        shuffle=True,
        # tensorboard args
        validation_data=(test_images, test_labels),
        callbacks=[
            tf.keras.callbacks.TensorBoard(
                log_dir=tensorboard_log_dir, histogram_freq=1
            )
        ],
    )

    model.save(model_dir, include_optimizer=True)
    return tensorboard_log_dir
