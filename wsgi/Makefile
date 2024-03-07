# Makefile for python code
# 
# > make help
#
# The following commands can be used.
#
# init:  sets up environment and installs requirements
# install:  Installs development requirements
# format:  Formats the code with autopep8
# lint:  Runs flake8 on src, exit if critical rules are broken
# clean:  Remove build and cache files
# env:  Source venv and environment files for testing
# leave:  Cleanup and deactivate venv
# test:  Run pytest
# run:  Executes the logic

.ONESHELL:

.DEFAULT_GOAL := run 

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
COVERAGE = $(VENV)/bin/coverage

$(VENV)/bin/activate: requirements.txt
    python3 -m venv $(VENV)
    $(PIP) install -r requirements.txt
    touch $(VENV)/bin/activate

setup: $(VENV)/bin/activate ## sets up environment and installs requirements

clean:
    rm -rf *.egg-info
    rm -rf build
    rm -rf dist
    rm -rf .pytest_cache
    # Remove all pycache
    find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
    rm -rf .venv
    rm -rf flake8_report.xml
    rm -rf coverage_report.xml
    rm -rf docs

test: $(VENV)
    pytest . -p no:logging -p no:warnings

test-coverage: $(VENV)
    $(COVERAGE) run -m pytest . -p no:logging -p no:warnings 
    $(COVERAGE) xml -o coverage_report.xml

flake8: $(VENV)
    flake8 . --format=xml --output-file=flake8_report.xml src

docs: $(VENV)
    pdoc --output-dir docs .
    touch docs/.nojekyll  # Pour éviter que GitHub Pages ne traite pas le dossier docs comme un site Jekyll

coverage-check: $(VENV)
    $(COVERAGE) report --fail-under=80 

# fake target
.PHONY: run clean
