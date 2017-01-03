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
