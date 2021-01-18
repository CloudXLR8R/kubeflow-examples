from os import path, environ, makedirs
from urllib.parse import urlparse
from pathlib import Path
from typing import List

import boto3


def get_s3_client():
    # allow s3 connection without creds
    if "AWS_ACCESS_KEY_ID" not in environ:
        from botocore import UNSIGNED
        from botocore.client import Config

        return boto3.client("s3", config=Config(signature_version=UNSIGNED))
    return boto3.client("s3")


def download_s3(bucket, key, outdir):
    s3 = get_s3_client()
    s3_object = s3.get_object(Bucket=bucket, Key=key)
    stream = s3_object["Body"]
    outfile = path.join(outdir, key)
    # filepath = path.abspath(outfile)
    parent_dir = path.dirname(outfile)
    Path(parent_dir).mkdir(parents=True, exist_ok=True)
    with open(outfile, "wb+") as f:
        f.write(stream.read())
    print(f"file saved to: {outfile}")
    return outfile


def parse_s3_url(url):
    print(f"downloading: {url}")
    u = urlparse(url)
    bucket = u.netloc.split(".")[0]
    key = u.path.strip("/")
    return bucket, key


def download_s3_url(data_urls: List[str], data_dir: str):
    """Download objects from S3"""

    import pprint

    pprint.pprint("data_urls")
    pprint.pprint(data_urls)
    pprint.pprint(f"data_dir: {data_dir}")

    if not path.exists(data_dir):
        makedirs(data_dir)

    saved_files = []

    for data_url in data_urls:
        pprint.pprint(f"data_url: {data_url}")
        bucket, key = parse_s3_url(data_url)
        pprint.pprint(f"bucket: {bucket}")
        pprint.pprint(f"key: {key}")

        saved_file = download_s3(bucket, key, data_dir)
        saved_files.append(saved_file)

    return saved_files


def download_data(data_urls: str, data_dir: str):
    # data_urls must be type string because kubeflow has no registered serializers for type "typing.List[str]"

    print(f"data_urls: {data_urls}")
    print(f"data_dir: {data_dir}")
    s3_urls = data_urls.split(",")
    saved_files = download_s3_url(s3_urls, data_dir)
    print("downloads complete")
    return saved_files
