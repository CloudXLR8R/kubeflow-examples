import json
from os import path

import tensorflow as tf
from tensorflow import keras

import numpy as np

# from sklearn.metrics import confusion_matrix, accuracy_score

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
        # images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels), 784)
        images = np.frombuffer(imgpath.read(), dtype=np.uint8, offset=16).reshape(
            len(labels), 28, 28
        )

    # normalize by dividing each pixel value by 255.0. This places the pixel value within the range 0 and 1.
    if normalize:
        # x_train = x_train.astype('float32') / 255
        # x_test = x_test.astype('float32') / 255
        images = images / 255.0

    return images, labels


# def write_cm_to_csv(cm, class_labels, cm_path):
#     data = []
#     for target_index, target_row in enumerate(cm):
#         for predicted_index, count in enumerate(target_row):
#             data.append(
#                 (class_labels[target_index], class_labels[predicted_index], count)
#             )

#     df_cm = pd.DataFrame(data, columns=["target", "predicted", "count"])
#     with file_io.FileIO(cm_path, "w") as f:
#         df_cm.to_csv(
#             f, columns=["target", "predicted", "count"], header=False, index=False
#         )


def predict(model, test_images):
    # Define a Softmax layer to define outputs as probabilities
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    predictions = probability_model.predict(test_images)
    return np.ravel(np.matrix(predictions).argmax(1))


def evaluate_model(
    metrics_path: str,
    data_dir: str,
    model_dir: str,
    # metadata_path: str,
    # cm_path: str,
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

    # predictions = predict(model, test_images)
    # cm = confusion_matrix(test_labels, predictions, cm_path)
    # write_cm_to_csv(cm, class_labels)
    # metadata = {
    #   'outputs' : [{
    #     'type': 'confusion_matrix',
    #     'format': 'csv',
    #     'schema': [
    #       {'name': 'target', 'type': 'CATEGORY'},
    #       {'name': 'predicted', 'type': 'CATEGORY'},
    #       {'name': 'count', 'type': 'NUMBER'},
    #     ],
    #     'source': cfm_path,
    #     # Convert vocab to string because for bool values we want "True|False" to match csv data.
    #     'labels': list(map(str, class_labels)),
    #   }]
    # }
    # with open(metadata_path, "w+") as f:
    #   json.dump(metadata, f)
    # metadata = {}

    (loss, accuracy) = model.evaluate(test_images, test_labels)
    metrics = {
        "metrics": [
            {"name": "loss", "numberValue": float(loss), "format": "PERCENTAGE"},
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
        # "output", ["mlpipeline_ui_metadata", "pipeline_metrics"]
        # "pipeline_metrics" is hardcoded value that could be anything
        "output",
        ["pipeline_metrics"],
    )
    return print_output(json.dumps(metrics))
    # return print_output(json.dumps(metadata), json.dumps(metrics))


# evaluate_model(metrics_path, data_dir, model_dir)
# evaluate_model(data_dir, model_dir, metrics_path)
# evaluate_model(data_dir, model_dir, metrics_path, metadata_path, cm_path)
# https://www.tensorflow.org/tfx/tutorials/serving/rest_simple#examine_your_saved_model
