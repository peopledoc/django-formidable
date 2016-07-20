ifeq (, $(shell which isort))
install-isort:
	pip install isort
else
install-isort:
	@echo ✓ isort installed
endif

.PHONY: check-python-imports
check-python-imports: install-isort
	@cat setup.cfg
	isort --check-only --recursive --verbose formidable
