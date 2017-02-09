# target: help - Display callable targets.
.PHONY: help
help:
	@echo "Reference card for usual actions in development environment."
	@echo "Here are available targets:"
	@egrep -o "^# target: (.+)" [Mm]akefile  | sed 's/# target: / * /'


# target: install-isort - install the Python package `isort`
ifeq (, $(shell which isort))
install-isort:
	pip install isort
else
install-isort:
	@echo ✓ isort installed
endif

# target: check-python-imports - checks if the python imports are correctly sorted
.PHONY: check-python-imports
check-python-imports: install-isort
	@cat setup.cfg
	isort --check-only --recursive --verbose formidable

# target: test - run all tests (unittests + linters)
.PHONY: test
test:
	tox -r

# target: docs - build the sphinx documentation
.PHONY: docs
docs:
	tox -e docs

# Crowdin-related commands
crowdin-venv:
	virtualenv .crowdin
	./.crowdin/bin/pip install crowdin-cli-py

# target: crowdin-build-yaml - generate the crowdin.yaml file out of the template and the secret API key.
# Note: if you have no .crowdin-cli-key and no access to formidable crowdin project, it's probably because you're not allowed to.
crowdin-build-yaml: crowdin.yaml.tmpl .crowdin-cli-key
	python -c "content = open('crowdin.yaml.tmpl').read(); key = open('.crowdin-cli-key').read().strip(); content = content.replace('CROWDIN-API-KEY', key); open('crowdin.yaml', 'w').write(content)"
