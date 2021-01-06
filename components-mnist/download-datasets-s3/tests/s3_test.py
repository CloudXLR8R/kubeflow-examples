import boto3
import pytest
from moto import mock_s3
from download import download_s3_url, parse_s3_url


@mock_s3
@pytest.mark.parametrize(
    ("s3_urls", "s3_contents"),
    [
        (
            [
                "https://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz"
            ],
            ["contents_one"],
        ),
    ],
)
def test_get_matching_s3_keys(tmpdir, s3_urls, s3_contents):
    s3 = boto3.client("s3")
    output_dir = tmpdir.mkdir("sub")

    for i, s3_url in enumerate(s3_urls):
        bucket, key = parse_s3_url(s3_url)
        s3.create_bucket(Bucket=bucket)
        s3.put_object(Bucket=bucket, Key=key, Body=s3_contents[i])

    result = download_s3_url(s3_urls, output_dir)

    for i, downloaded in enumerate(result):
        with open(downloaded, "r") as f:
            assert f.read() == s3_contents[i]
