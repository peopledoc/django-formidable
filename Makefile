BROCCOLI=./node_modules/.bin/broccoli

serve: clean-build
	$(BROCCOLI) serve

s: serve

build: clean-build
	$(BROCCOLI) build dists

clean-build:
	rm -Rf dist

clean-deps:
	rm -Rf bower_components
	rm -Rf node_modules

install:
	bower install --quiet
	npm install --quiet

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build        to build the public files"
	@echo "  serve (s)    to start the development server"
	@echo "  clean-build  to clean build files"
	@echo "  clean-deps   to clean dependencies files"
	@echo "  install      to install dependencies"
