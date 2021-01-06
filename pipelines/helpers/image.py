from os import environ


def component_image_name(name):
    if name == "":
        raise Exception("name of image not passed to function")

    parts = name.split(":")
    if len(parts) == 2:
        name = parts[0]
        tag = parts[1]
    else:
        tag = environ.get("IMAGE_TAG")
        if tag is None:
            raise Exception("IMAGE_TAG environment variable not set")

    registry = environ.get("IMAGE_REGISTRY")
    if registry is None:
        raise Exception("IMAGE_REGISTRY environment variable not set")
    registry = (
        registry
        if not registry.endswith("/") or len("/") == 0
        else registry[: -len("/")]
    )

    repo = environ.get("IMAGE_REPO")
    if repo is None:
        raise Exception("IMAGE_REPO environment variable not set")

    return f"{registry}/{repo}/components/{name}:{tag}"
