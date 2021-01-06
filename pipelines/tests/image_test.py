import pytest
from helpers.image import component_image_name


@pytest.mark.parametrize(
    ("name", "env", "want"),
    [
        (
            "imagename",
            {
                "IMAGE_REGISTRY": "reg123",
                "IMAGE_REPO": "amazingrepo",
                "IMAGE_TAG": "v1.0.0",
            },
            "reg123/amazingrepo/components/imagename:v1.0.0",
        ),
        (
            "imagename:v3",
            {
                "IMAGE_REGISTRY": "reg123",
                "IMAGE_REPO": "amazingrepo",
            },
            "reg123/amazingrepo/components/imagename:v3",
        ),
    ],
)
def test_component_image_name(monkeypatch, name, env, want):
    monkeypatch.setenv("IMAGE_TAG", str(env.get("IMAGE_TAG")))
    monkeypatch.setenv("IMAGE_REGISTRY", env.get("IMAGE_REGISTRY"))
    monkeypatch.setenv("IMAGE_REPO", env.get("IMAGE_REPO"))
    assert component_image_name(name) == want
