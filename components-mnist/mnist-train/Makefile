ENV_DIR = env

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
	@python main.py --help

debug:
	@pytest --pdb

.PHONY: deps* lint test debug clean install
