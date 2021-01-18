import pytest
import json
from metadata import (
    gen_metadata,
    write_metadata,
)

from .helpers.temp import get_tmp_filename


@pytest.mark.parametrize(
    ("bucket", "bucket_dir", "expected"),
    [
        ("bucket1", "some/dir", "s3://bucket1/some/dir"),
    ],
)
def test_train_model(bucket, bucket_dir, expected):
    metadata_file = get_tmp_filename("metadata", "json")

    write_metadata(metadata_file, bucket, bucket_dir)

    with open(metadata_file) as f:
        metadata_file_contents = json.load(f)
        assert json.dumps(metadata_file_contents, sort_keys=True) == json.dumps(
            gen_metadata(expected), sort_keys=True
        )
