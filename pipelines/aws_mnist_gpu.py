from jinja2 import Environment, FileSystemLoader

from kfp import compiler
from kfp import dsl
from kfp.components import load_component_from_text
from kfp.aws import use_aws_secret

from helpers.image import component_image_name
from helpers.tmp import get_tmp_dir


env = Environment(  # nosec
    # https://jinja.palletsprojects.com/en/2.11.x/api/#jinja2.DictLoader
    loader=FileSystemLoader("./components-templates"),
)


def downloadOp(datasets_dir):
    template = env.get_template("download-datasets-s3.yaml.j2")
    component = template.render(
        image=component_image_name("download-datasets-s3"),
        output_dir=datasets_dir,
    )
    return load_component_from_text(component)


def trainOp(model_dir):
    template = env.get_template("mnist-train.yaml.j2")
    component = template.render(
        image=component_image_name("mnist-train"),
        model_dir=model_dir,
        log_dir=get_tmp_dir("log"),
    )
    return load_component_from_text(component)


def evaluateOp():
    template = env.get_template("mnist-evaluate.yaml.j2")
    component = template.render(
        image=component_image_name("mnist-evaluate"),
    )
    return load_component_from_text(component)


def exportOp():
    template = env.get_template("upload-s3.yaml.j2")
    component = template.render(
        image=component_image_name("upload"),
    )
    return load_component_from_text(component)


@dsl.pipeline(
    name="mnist_pipeline",
    description="Train an mnist fashion classification model and export to AWS S3",
)
def pipeline(  # nosec
    aws_secret_name: str = "aws-s3-data-secret-kfaas-demo",
    model_name: str = "mnist-fashion",
    model_version: str = "1",
    epochs: int = 10,
    bucket: str = "kfaas-demo-data-sandbox",
    bucket_dir_model: str = "demo/models",
    bucket_dir_tensorboard: str = "demo/tensorboard",
):

    gpus = 1
    mnt_path = "/mnt"
    datasets_dir = "/mnt/datasets"
    model_dir = "/mnt/model"
    mnist_data_s3_urls = [
        "https://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz",
        "https://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-labels-idx1-ubyte.gz",
        "https://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-images-idx3-ubyte.gz",
        "https://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-labels-idx1-ubyte.gz",
    ]

    aws_secret = use_aws_secret(
        aws_secret_name, "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"
    )

    vop = dsl.VolumeOp(
        name="create_volume",
        resource_name="data-volume",
        size="1Gi",
        modes=dsl.VOLUME_MODE_RWO,
    )

    download_op = downloadOp(datasets_dir)
    download_task = download_op(urls=(",").join(mnist_data_s3_urls)).add_pvolumes(
        {mnt_path: vop.volume}
    )

    train_op = trainOp(model_dir)
    train_task = (
        train_op(
            datadir=datasets_dir,
            epochs=epochs,
            bucket=bucket,
            bucketdir=f"{bucket_dir_tensorboard}/{model_name}/{model_version}/{dsl.RUN_ID_PLACEHOLDER}",
        )
        .set_gpu_limit(gpus)
        .add_pvolumes({mnt_path: download_task.pvolume})
        .apply(aws_secret)
    )
    train_task.after(download_task)

    evaluate_op = evaluateOp()
    evaluate_task = evaluate_op(datadir=datasets_dir, modeldir=model_dir).add_pvolumes(
        {mnt_path: train_task.pvolume}
    )
    evaluate_task.after(train_task)
    vop.delete().after(evaluate_task)

    export_op = exportOp()
    export_task = (
        export_op(
            srcdir=model_dir,
            bucket=bucket,
            bucketdir=f"{bucket_dir_model}/{model_name}/{model_version}",
        )
        .add_pvolumes({mnt_path: evaluate_task.pvolume})
        .apply(aws_secret)
    )
    export_task.after(evaluate_task)


if __name__ == "__main__":
    package_name = __file__.replace(".py", ".zip")
    compiler.Compiler().compile(pipeline, package_name)
