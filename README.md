[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Kubeflow Examples
Example kubeflow pipelines for use with Cloud XLR8R's [managed Kubeflow service](https://cloudxlr8r.com/kubeflow). See the [docs](https://docs.cloudxlr8r.com/) or [XLR8R's blog](https://cloudxlr8r.com/blog) for tutorials on how to use these.


### Up to date examples for Kubeflow v1.1.2+ (December 2020 onwards)
A lot of tutorials you'll find use [`dsl.ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.dsl.html#kfp.dsl.ContainerOp) which is going to be deprecated (compiler warning added in kubeflow pipelines [v1.1.2](https://github.com/kubeflow/pipelines/blob/1.2.0/CHANGELOG.md#112-2020-12-14) released on 14 December 2020). These examples illustrate how you construct pipelines *without* using `dsl.ContainerOp`. A level of dynamic variables at compile time is needed for a CI pipeline to inject the container image URLs. The approach taken here is to use [Jinja](https://github.com/pallets/jinja) templates to achieve this.

-----------------------------------------------------------

## Pipelines

## AWS
### [AWS MNIST Fashion](./pipelines/aws_mnist.py)
1. Downloads dataset from AWS S3 and persists into a PVC for passing between steps
2. Trains the model using Keras and exports the tensorboard logs to AWS S3
3. Evaluates the model on the test dataset and prints the accuracy metric for display in the Kubeflow dashboard
4. Exports the model to AWS S3
### [AWS S3](./pipelines/aws_s3.py)
1. Lists the contents of an AWS S3 bucket path.
2. Primarily used to check AWS credentials supplied to [`use_aws_secret`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.extensions.html?highlight=use_aws_secret#kfp.aws.use_aws_secret) have the correct permissions.
