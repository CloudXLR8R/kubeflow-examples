# Kubeflow Components
These [Kubeflow Components](https://www.kubeflow.org/docs/pipelines/overview/concepts/component/) are the building blocks for the [Kubeflow pipelines](./../pipelines).

## CI
### Packaging Kubeflow Components
Every subfolder containing a `Dockerfile` will get packaged as a kubeflow component and uploaded to AWS ERC by the CI process. Images are tagged using the git commit SHA. Example list of ECR repos createed from a commit to master branch:
```
REPOSITORY                                                                              TAG                                        IMAGE ID            CREATED             SIZE
<aws_account_id>.dkr.ecr.eu-west-2.amazonaws.com/example-kubeflow-app/components/sum        dac061c4d721b826cfde8fdd40be5a62745950ab   71fcf9c41d3a        1 second ago        231MB
<aws_account_id>.dkr.ecr.eu-west-2.amazonaws.com/example-kubeflow-app/components/readfile   dac061c4d721b826cfde8fdd40be5a62745950ab   45b95f4e1f34        9 seconds ago       231MB
<aws_account_id>.dkr.ecr.eu-west-2.amazonaws.com/example-kubeflow-app/components/movefile   dac061c4d721b826cfde8fdd40be5a62745950ab   6b3c6ce812d0        24 seconds ago      145MB
```
----------------------------------------
## Quickstart Create New Component
Copy one of the existing components and update the files as necessary. The [`readfile` component `README`](./readfile) has instructions for local development.
```console
$ cp -r readfile mynewcomponent
```

----------------------------------------

## Example Component Directory Layout
The only required file is the `Dockerfile` but this shows a typical simple component's contents.
```
.
├── dev-requirements.in
├── dev-requirements.txt
├── Dockerfile
├── Makefile
├── readfile.py
├── README.md
├── requirements.in
├── requirements.txt
└── tests
    ├── __init__.py
    └── readfile_test.py
```

----------------------------------------

### Running Unit Tests
In order for a component's tests to run in CI its directory must contain a `Makefile` with a `make test` recipe. If it contains a `Makefile` which does not have a `make test` recipe then CI will fail.

----------------------------------------

## Authoring Components
Components should be idemopotent, that is they should not have side effects and be able to be re-run with the same inputs and produce the same outputs.

### Best practices
Follow the official kubeflow best practices when [writing components](https://www.kubeflow.org/docs/pipelines/sdk/best-practices/).

### Passing data between Components
> To output any piece of data, the component program must write the output data to some location and inform the system about that location so that the system can pass the data between steps. The program should accept the paths for the output data as command-line arguments. That is, you should not hardcode the paths.
See the rest of the [official guide on creating re-usable components](https://www.kubeflow.org/docs/pipelines/sdk/component-development/)
