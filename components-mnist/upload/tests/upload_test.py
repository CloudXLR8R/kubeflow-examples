# import boto3
import pytest

from moto import mock_s3
from s3 import upload_dir


@mock_s3
@pytest.mark.parametrize(
    ("bucket_name", "bucket_dir", "src_dir"),
    [
        (
            "fancybucket",
            "some/path",
            "/tmp/local/path",
        ),
    ],
)
def test_upload_dir(tmpdir, bucket_name, bucket_dir, src_dir):
    assert callable(upload_dir)
    # s3 = boto3.client("s3")
    # output_dir = tmpdir.mkdir("sub")

    # for i, s3_url in enumerate(s3_urls):
    #     bucket, key = parse_s3_url(s3_url)
    #     s3.create_bucket(Bucket=bucket)
    #     s3.put_object(Bucket=bucket, Key=key, Body=s3_contents[i])

    # result = download_s3_url(s3_urls, output_dir)

    # for i, downloaded in enumerate(result):
    #     with open(downloaded, "r") as f:
    #         assert f.read() == s3_contents[i]
