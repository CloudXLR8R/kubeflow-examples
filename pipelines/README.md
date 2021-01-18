# Kubeflow Pipelines


### TLDR Importing Component Images Into Pipeline
Use `component_image_name` helper function for images defined in this github repository but not for those where the source code lives elsewhere eg `myotherreg/repo:v1.0.0`.

#### `component_image_name` helper function
In order to import components *defined in this github repository* you must reference their image using the `component_image_name` helper function. This function creates the full ECR image path using environment variables which are automatically set in CI. Normally you will just pass the component name to the `component_image_name` helper function but optionally you can specify the tag (only recommended for local development). See the [helper's unit tests](tests/image_test.py) for more examples.

```python
def downloadOp(datasets_dir):
    template = env.get_template("download-datasets-s3.yaml.j2")
    component = template.render(
        image=component_image_name("download-datasets-s3"),
        output_dir=datasets_dir,
    )
    return load_component_from_text(component)
```

--------------------------------------------------
## Local Development
### Quickstart
```console
$ make env
$ source env/bin/activate
$ make deps deps-update
$ pip install -r requirements.txt
```
### Compiling Pipelines
```console
$ vi .env.example
$ source .env.example
$ make pipeline
$ less pipeline.yaml
```
