import argparse
from train import train_model
from metadata import write_metadata
from s3 import upload_dir


def parse_arguments():
    parser = argparse.ArgumentParser(description="Mnist Model trainer")
    parser.add_argument(
        "-d",
        "--datadir",
        help="Datasets directory",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--outdir",
        help="Output directory to save trained model",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--logdir",
        help="Output directory to save training logs",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--metadatafile",
        help="File to save kubeflow metrics JSON",
        required=True,
    )
    parser.add_argument(
        "-e",
        "--epochs",
        type=int,
        help="Number of epochs to train the model for",
        required=True,
    )
    parser.add_argument(
        "-b",
        "--bucket",
        help="S3 bucket to upload tensorboard logs",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--bucketdir",
        help="S3 bucket dir to upload tensorboard logs",
        required=True,
    )
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_arguments()
    print(f"model dir: {args.outdir}")
    print(f"datasets dir: {args.datadir}")
    print(f"log dir: {args.logdir}")
    print(f"metadatafile: {args.metadatafile}")
    print(f"epochs: {args.epochs}")
    print(f"bucket: {args.bucket}")
    print(f"bucket dir: {args.bucketdir}")

    # train model
    tensorboard_log_dir = train_model(
        args.outdir,
        args.datadir,
        args.logdir,
        args.epochs,
    )

    # upload tensorboard logs to s3
    upload_dir(tensorboard_log_dir, args.bucket, args.bucketdir)

    # write metdata file pointing to tensorboard logs hosted on S3
    write_metadata(args.metadatafile, args.bucket, args.bucketdir)
