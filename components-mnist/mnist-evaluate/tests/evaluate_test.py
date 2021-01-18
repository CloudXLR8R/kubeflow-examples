import pytest

from evaluate import evaluate_model


@pytest.mark.parametrize(
    ("model_name"),
    [
        ("test"),
    ],
)
def test_evaluate_model(
    model_name,
):
    assert callable(evaluate_model)
