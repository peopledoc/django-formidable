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

PYTHON3 := $(shell command -v python3 2> /dev/null)
# target: serve-docs - use a tiny HTTP static server for browsing the doc
.PHONY: serve-docs
serve-docs:
ifdef PYTHON3
	cd docs/build/html; python3 -m http.server
else
	cd docs/build/html; python -m SimpleHTTPServer
endif

# target: swagger-statics - rebuild the swagger statics needed to display the swagger specs
.PHONY: swagger-statics
swagger-statics:
	tox -e swagger-statics

##################### Crowdin-related commands

# target: crowdin-venv - create the crowdin-ready virtualenv
.PHONY: crowdin-venv
crowdin-venv:
	mkdir -p formidable/locale
	virtualenv .crowdin
	./.crowdin/bin/pip install -e .
	./.crowdin/bin/pip install crowdin-cli-py

# target: crowdin-build-yaml - generate the crowdin.yaml file out of the template and the secret API key.
# Note: if you have no .crowdin-cli-key and no access to formidable crowdin project, it's probably because you're not allowed to.
crowdin-build-yaml: crowdin.yaml.tmpl .crowdin-cli-key
	python -c "content = open('crowdin.yaml.tmpl').read(); key = open('.crowdin-cli-key').read().strip(); content = content.replace('CROWDIN-API-KEY', key); open('crowdin.yaml', 'w').write(content)"

# target: crowdin-setup - Set the crowdin environment up.
crowdin-setup: crowdin-venv crowdin-build-yaml

# "fake" target that would build the crowdin env if needed
crowdin-check:
	if [ ! -f ./.crowdin/bin/crowdin-cli-py ]; \
	then make crowdin-venv; \
	fi

# target: crowdin-gettext-makemessages - generate .po files for all the available languages - NEEDS CROWDIN CREDENTIALS
crowdin-gettext-makemessages: crowdin-check
	cd formidable; ../.crowdin/bin/django-admin makemessages --no-obsolete `.crowdin/bin/crowdin-cli-py list translations | cut -d '/' -f 1 | sed 's/.*/-l & /'`; cd ..

# target: gettext-makemessages - generate .po files for all the available languages
gettext-makemessages: crowdin-check
	cd formidable; ../.crowdin/bin/django-admin makemessages --all; cd ..

# target: gettext-compilemessages - compile .mo files for available translations
gettext-compilemessages: crowdin-check
	cd formidable; ../.crowdin/bin/django-admin compilemessages; cd ..

# target: crowdin-upload - Upload updated strings to crowdin.com
crowdin-upload: crowdin-check
	./.crowdin/bin/crowdin-cli-py upload sources

# target: crowdin-download - Download the translations from crowdin.com
crowdin-download: crowdin-check
	./.crowdin/bin/crowdin-cli-py download

# target: crowdin-download-compile - Download the translations from crowdin.com *and* convert them into .mo files.
crowdin-download-compile: crowdin-download gettext-compilemessages
