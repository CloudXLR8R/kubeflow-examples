#!/usr/bin/env python
import argparse
from evaluate import evaluate_model


def parse_arguments():
    parser = argparse.ArgumentParser(description="Evaluate trained model")
    parser.add_argument(
        "-d",
        "--datadir",
        help="Datasets directory",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--modeldir",
        help="Model directory",
        required=True,
    )
    parser.add_argument(
        "--metricspath",
        help="Path to save metrics file",
        required=True,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(f"model dir: {args.modeldir}")
    print(f"datasets dir: {args.datadir}")
    print(f"metrics path: {args.metricspath}")
    evaluate_model(args.metricspath, args.datadir, args.modeldir)
