runserver:
	python manage.py runserver

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  runserver to run the development server"
	@echo "  populate  to setup the database with fixtures"
	@echo "  install   install the demo site in your current virtualenv"

install-requirements:
	cd .. ; pip install -e ./
	pip install -r requirements-demo.pip

migrate:
	python manage.py migrate

populate:
	python manage.py populate fixtures/*.json

install: install-requirements migrate populate
