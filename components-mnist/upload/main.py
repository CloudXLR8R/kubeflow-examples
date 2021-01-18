import argparse

from s3 import upload_dir


def parse_arguments():
    parser = argparse.ArgumentParser(description="Upload model to S3")
    parser.add_argument("-b", "--bucket", help="S3 bucket", required=True)
    parser.add_argument(
        "-d",
        "--bucketdir",
        help="S3 bucket directory to save to",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--srcdir",
        help="local source directory of files to upload",
        required=True,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(f"src dir: {args.srcdir}")
    upload_dir(args.srcdir.strip(), args.bucket.strip(), args.bucketdir.strip())
