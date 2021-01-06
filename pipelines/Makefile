ENV_DIR = env

env:
	@python3 -m venv ${ENV_DIR}

pipeline:
	@python ${PIPELINE}.py
	@unzip -o ${PIPELINE}.zip

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
	@rm -rf compiled
	@rm -rf *.zip
	@rm -rf *.yaml

test:
	@python -m pytest

debug:
	@pytest --pdb

.PHONY: deps* lint test debug clean pipeline
