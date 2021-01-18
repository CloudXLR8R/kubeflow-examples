import json
from os import path

import tensorflow as tf
from tensorflow import keras

import numpy as np

from typing import NamedTuple
from collections import namedtuple


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


def predict(model, test_images):
    # Define a Softmax layer to define outputs as probabilities
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    predictions = probability_model.predict(test_images)
    return np.ravel(np.matrix(predictions).argmax(1))


def evaluate_model(
    metrics_path: str,
    data_dir: str,
    model_dir: str,
) -> NamedTuple(
    "output",  # noqa: F821
    # https://www.kubeflow.org/docs/pipelines/sdk/pipelines-metrics/
    # The output name must be MLPipeline Metrics or MLPipeline_Metrics (case does not matter).
    [
        ("mlpipeline_ui_metadata", "UI_metadata"),  # noqa: F821
        ("mlpipeline_metrics", "Metrics"),  # noqa: F821
    ],
):

    test_images, test_labels = load_mnist(data_dir, kind="t10k", normalize=False)
    model = keras.models.load_model(model_dir)
    (loss, accuracy) = model.evaluate(test_images, test_labels)
    print(f"loss = {loss}")
    metrics = {
        "metrics": [
            {
                "name": "accuracy",
                "numberValue": float(accuracy),
                "format": "PERCENTAGE",
            },
        ]
    }
    with open(metrics_path, "w+") as f:
        json.dump(metrics, f)

    print_output = namedtuple(
        # "pipeline_metrics" is hardcoded value that could be anything
        "output",
        ["pipeline_metrics"],
    )
    return print_output(json.dumps(metrics))
