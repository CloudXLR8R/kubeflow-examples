[![CircleCI](https://circleci.com/gh/CloudXLR8R/kubeflow-examples.svg?style=svg)](https://circleci.com/gh/CloudXLR8R/kubeflow-examples)

# Kubeflow Examples
Example kubeflow pipelines for use with Cloud XLR8R's [managed Kubeflow service](https://cloudxlr8r.com/kubeflow). See the [docs](https://docs.cloudxlr8r.com/) or [XLR8R's blog](https://cloudxlr8r.com/blog) for tutorials on how to use these.

### Kubeflow v1.1.2+ (December 2020)
A lot of tutorials on the web use [`dsl.ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.dsl.html#kfp.dsl.ContainerOp) which is to be deprecated (compiler warning added in kubeflow pipelines [v1.1.2](https://github.com/kubeflow/pipelines/blob/1.2.0/CHANGELOG.md#112-2020-12-14) released on 14 December 2020). The examples in this repo use the new syntax (ie *not* using `dsl.ContainerOp`).

-----------------------------------------------------------

## Pipelines
### AWS
#### [AWS MNIST Fashion](./pipelines/aws_mnist.py)
1. Downloads dataset from AWS S3 and persists into a PVC for passing between steps
2. Trains the model using Keras and exports the tensorboard logs to AWS S3
3. Evaluates the model on the test dataset and prints the accuracy metric for display in the Kubeflow dashboard
4. Exports the model to AWS S3
#### [AWS S3](./pipelines/aws_s3.py)
1. Lists the contents of an AWS S3 bucket path.
2. Primarily used to check AWS credentials supplied to [`use_aws_secret`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.extensions.html?highlight=use_aws_secret#kfp.aws.use_aws_secret) have the correct permissions.

## Jupyter Notebooks
### AWS MNIST Fashion
#### [Vanilla](./notebooks/mnist_vanilla.ipynb)
A notebook for pure local development (does not use kubeflow).
1. Downloads dataset from AWS S3 and persists locally
2. Trains model and saves tensorboard logs
3. Evaluates model accuracy
4. Launches tensorboard server
5. Launches tensorflow serving API
6. Queries API
#### [Local Development](./notebooks/mnist_local_kf_pipeline.ipynb)
A notebook that can be used to develop locally in your IDE of choice (eg VSCode). It performs the same steps as the vanilla notebook except it uses [Kubeflow lightweight functions](https://www.kubeflow.org/docs/pipelines/sdk/python-function-components/) to run the steps using a kubeflow pipeline and exports the tensorboard logs to AWS S3.
#### [Server Development](./notebooks/mnist_server_kf_pipeline.ipynb)
A notebook designed to be uploaded to a jupyter notebook running in the cloud (ie via a notebook node launched via the kubeflow dashboard). Performs the same tasks as the local development notebook.
