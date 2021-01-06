from kfp import compiler
from kfp import dsl
from kfp.components import load_component_from_file
from kfp.aws import use_aws_secret


def checkS3AccessOp():
    return load_component_from_file("components/test-access-aws-s3.yaml")


@dsl.pipeline(
    name="mnist_pipeline",
    description="Train and deploy mnist fashion classification",
)
def pipeline(  # nosec
    aws_secret_name: str = "aws-s3-data-secret-kfaas-demo",
    bucket: str = "kfaas-demo-data-sandbox",
    bucket_dir: str = "demo",
):
    aws_secret = use_aws_secret(
        aws_secret_name, "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"
    )

    check_s3_access_op = checkS3AccessOp()
    check_s3_access_op(
        s3_path=f"s3://{bucket}/{bucket_dir}",
    ).apply(aws_secret)


if __name__ == "__main__":
    package_name = __file__.replace(".py", ".zip")
    compiler.Compiler().compile(pipeline, package_name)
