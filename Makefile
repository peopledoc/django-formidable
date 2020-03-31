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

# target: serve-docs - use a tiny HTTP static server for browsing the doc
.PHONY: serve-docs
serve-docs:
	cd docs/build/html; python3 -m http.server

# target: swagger-statics - rebuild the swagger statics needed to display the swagger specs
.PHONY: swagger-statics
swagger-statics:
	tox -e swagger-statics
