import pytest
from os import path

from train import train_model, gen_log_dirname


@pytest.mark.parametrize(
    ("data_dir", "model_file"),
    [
        ("tests/datasets", "saved_model.pb"),
    ],
)
def test_train_model(tmpdir, data_dir, model_file):
    model_dir = tmpdir.mkdir("model")
    log_dir = tmpdir.mkdir("log")
    tensorboard_log_dir = gen_log_dirname(log_dir)

    assert (
        train_model(model_dir, data_dir, log_dir) == tensorboard_log_dir  # noqa: W503
    )

    assert path.isfile(path.join(model_dir, model_file))
