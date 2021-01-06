import argparse
from download import download_data


def parse_arguments():
    parser = argparse.ArgumentParser(description="S3 Object downloader")
    parser.add_argument(
        "-u", "--urls", help="S3 URLs to download. Comma separated list.", required=True
    )
    parser.add_argument(
        "-o",
        "--outdir",
        help="Output directory to save downloaded S3 object(s)",
        required=True,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(f"outdir: {args.outdir}")
    print(f"s3_urls: {args.urls}")
    download_data(args.urls.strip(), args.outdir.strip())
