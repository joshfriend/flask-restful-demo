# Python settings
PYTHON_MAJOR := 2
PYTHON_MINOR := 7

# Project settings (automatically detected from files/directories)
PROJECT := BarCampDemo
PACKAGE := demo
SOURCES := Makefile setup.py $(shell find $(PACKAGE) -name '*.py')
REQUIREMENTS_DEV := requirements/dev.txt
REQUIREMENTS_PROD := requirements/prod.txt

# System paths (automatically detected from the system Python)
PLATFORM := $(shell python -c 'import sys; print(sys.platform)')
ifneq ($(findstring win32, $(PLATFORM)), )
	SYS_PYTHON_DIR := C:\\Python$(PYTHON_MAJOR)$(PYTHON_MINOR)
	SYS_PYTHON := $(SYS_PYTHON_DIR)\\python.exe
	SYS_VIRTUALENV := $(SYS_PYTHON_DIR)\\Scripts\\virtualenv.exe
	# https://bugs.launchpad.net/virtualenv/+bug/449537
	export TCL_LIBRARY=$(SYS_PYTHON_DIR)\\tcl\\tcl8.5
else
	SYS_PYTHON := python$(PYTHON_MAJOR)
	SYS_VIRTUALENV := virtualenv
endif

# virtualenv paths (automatically detected from the system Python)
ENV := env
ifneq ($(findstring win32, $(PLATFORM)), )
	BIN := $(ENV)/Scripts
	OPEN := cmd /c start
else
	BIN := $(ENV)/bin
	ifneq ($(findstring cygwin, $(PLATFORM)), )
		OPEN := cygstart
	else
		OPEN := open
	endif
endif

# virtualenv executables
PYTHON := $(BIN)/python
PIP := $(BIN)/pip
PEP8 := $(BIN)/pep8
FLAKE8 := $(BIN)/flake8
PEP257 := $(BIN)/pep257
PYLINT := $(BIN)/pylint
PYTEST := "$(BIN)/py.test"
COVERAGE := $(BIN)/coverage

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

.PHONY: serve
serve: depends
	$(PYTHON) manage.py runserver

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

