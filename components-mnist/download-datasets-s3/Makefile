ENV_DIR = env
DATA_DIR = tmp
S3_URLS = 'https://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz,https://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-labels-idx1-ubyte.gz,https://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-images-idx3-ubyte.gz,https://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-labels-idx1-ubyte.gz'

env:
	@python3 -m venv ${ENV_DIR}

deps-update: deps
	@pip-compile --upgrade requirements.in
	@pip-compile --upgrade dev-requirements.in
	@pip-sync requirements.txt dev-requirements.txt

deps:
	@python -m pip install pip-tools

install:
	@pip install -r requirements.txt
	@pip install -r dev-requirements.txt

clean:
	@rm -rf tmp

clean-env:
	@rm -rf .tox
	@rm -rf ${ENV_DIR}

test:
	@python -m pytest

test-manual:
	@python main.py --outdir ${DATA_DIR} --urls ${S3_URLS}

debug:
	@pytest --pdb

.PHONY: deps* lint test debug clean install
