import json


def gen_metadata(tensorboard_log_dir):
    return {
        "outputs": [
            {
                "type": "tensorboard",
                "source": tensorboard_log_dir,
            }
        ]
    }


def write_metadata(
    metadata_file: str,
    bucket: str,
    bucket_dir: str,
):
    tensorboard_log_dir = f"s3://{bucket}/{bucket_dir}"
    with open(metadata_file, "w") as f:
        json.dump(gen_metadata(tensorboard_log_dir), f)


# def gen_kf_output(metadata):
#     print_output = namedtuple("output", ["mlpipeline_ui_metadata"])
#     return print_output(json.dumps(metadata))


# def gen_timestamp() -> str:
#     return str(int(datetime.datetime.now().timestamp()))
# def gen_timestamp(time) -> str:
#     return time.strftime("%Y%m%d-%H%M%S")


# eg time = datetime.datetime.now()
# def gen_log_dirname(log_dir, timestamp) -> str:
#     return .join(log_dir, "tensorboard", "fit", timestamp)
