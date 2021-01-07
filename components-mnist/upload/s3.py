import boto3
from botocore.exceptions import ClientError
import os


def get_s3_client():
    # allow s3 connection without creds
    if "AWS_ACCESS_KEY_ID" not in os.environ:
        from botocore import UNSIGNED
        from botocore.client import Config

        return boto3.client("s3", config=Config(signature_version=UNSIGNED))
    return boto3.client("s3")


def upload_file(s3_client, file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    return s3_client.upload_file(file_name, bucket, object_name)


def bucket_exists(s3_client, bucket_name):
    exists = True
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            exists = False
    return exists


def upload_dir(
    src_dir: str,
    bucket_name: str,
    bucket_dir: str,
):
    s3_client = get_s3_client()

    if not bucket_exists(s3_client, bucket_name):
        raise Exception(f"Bucket: {bucket_name} does not exist")

    for root, dirs, files in os.walk(src_dir):
        for name in files:
            local_path = os.path.join(root, name)
            upload_file(
                s3_client,
                local_path,
                bucket_name,
                f"{bucket_dir}/{os.path.relpath(local_path, src_dir)}",
            )

    print(f"Objects uploaded: {bucket_name}:")
    response = s3_client.list_objects(Bucket=bucket_name, Prefix=bucket_dir)
    for file in response["Contents"]:
        print(f"{bucket_name}/{file['Key']}")
