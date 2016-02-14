# Python settings
PYTHON_MAJOR := 2
PYTHON_MINOR := 7

# Project settings (automatically detected from files/directories)
PROJECT := BarCampDemo
PACKAGE := demo
SOURCES := Makefile setup.py $(shell find $(PACKAGE) -name '*.py')
REQUIREMENTS_DEV := requirements/dev.txt
REQUIREMENTS_PROD := requirements/prod.txt

SYS_PYTHON := python$(PYTHON_MAJOR).$(PYTHON_MINOR)
SYS_VIRTUALENV := virtualenv

# virtualenv paths (automatically detected from the system Python)
ENV := env
BIN := $(ENV)/bin

# virtualenv executables
PYTHON := $(BIN)/python
PIP := $(BIN)/pip
PEP8 := $(BIN)/pep8
FLAKE8 := $(BIN)/flake8
PEP257 := $(BIN)/pydocstyle
PYLINT := $(BIN)/pylint
PYTEST := "$(BIN)/py.test"
COVERAGE := $(BIN)/coverage
ACTIVATE := $(BIN)/activate
HONCHO := . $(ACTIVATE); $(BIN)/honcho

HONCHO_CONFIG := .env

# Flags for PHONY targets
DEPENDS := $(ENV)/depends
ALL := $(ENV)/.all

# Main Targets ###############################################################

.PHONY: all
all: depends $(ALL)
$(ALL): $(SOURCES)
	$(MAKE) check
	touch $(ALL)  # flag to indicate all setup steps were successful

.PHONY: ci
ci: pep8 pep257 test tests

# Development Installation ###################################################

.PHONY: env
env: .virtualenv

.PHONY: .virtualenv
.virtualenv: $(PIP)
$(PIP):
	$(SYS_VIRTUALENV) --python $(SYS_PYTHON) $(ENV)

.PHONY: depends
depends: env $(DEPENDS)
$(DEPENDS): $(REQUIREMENTS_DEV) $(REQUIREMENTS_PROD)
	$(PIP) install -r $(REQUIREMENTS_DEV)
	touch $(DEPENDS)  # flag to indicate dependencies are installed

# Static Analysis ############################################################

.PHONY: check
check: flake8

.PHONY: pep8
pep8: depends
	$(PEP8) $(PACKAGE)

.PHONY: flake8
flake8: depends
	$(FLAKE8) $(PACKAGE)

.PHONY: pep257
pep257: depends
	$(PEP257) $(PACKAGE) --ignore=D102

.PHONY: pylint
pylint: depends
	$(PYLINT) $(PACKAGE) --rcfile=.pylintrc

# Testing ####################################################################

.PHONY: test
test: depends
	$(COVERAGE) run --source $(PACKAGE) -m py.test tests
	$(COVERAGE) report -m

.PHONY: tests
tests: depends
	TEST_INTEGRATION=1 $(COVERAGE) run --source $(PACKAGE) -m py.test tests
	$(COVERAGE) report -m

# Development server #########################################################

define HONCHO_CONFIG_CONTENTS
GUNICORN_RELOAD=true
GUNICORN_WORKER_CLASS=gevent
endef

export HONCHO_CONFIG_CONTENTS
$(HONCHO_CONFIG):
	echo "$$HONCHO_CONFIG_CONTENTS" > $@

.PHONY: serve
serve: depends $(HONCHO_CONFIG)
	$(HONCHO) start -e $(HONCHO_CONFIG)

# Database Migrations ########################################################

.PHONY: migrate
migrate: depends
	$(PYTHON) manage.py db migrate

.PHONY: upgrade
upgrade: depends
	$(PYTHON) manage.py db upgrade

.PHONY: downgrade
downgrade: depends
	$(PYTHON) manage.py db downgrade

# Cleanup ####################################################################

.PHONY: clean
clean: .clean-dist .clean-test .clean-build
	rm -rf $(ALL)

.PHONY: clean-all
clean-all: clean .clean-env

.PHONY: .clean-env
.clean-env:
	rm -rf $(ENV)

.PHONY: .clean-build
.clean-build:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: .clean-test
.clean-test:
	rm -rf .coverage

.PHONY: .clean-dist
.clean-dist:
	rm -rf dist build

