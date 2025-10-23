SHELL := /bin/bash
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: venv install lint format type test check clean

venv:
python -m venv $(VENV)

install: venv
$(PIP) install -U pip
if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi
if [ -f requirements-dev.txt ]; then $(PIP) install -r requirements-dev.txt; fi

lint:
$(VENV)/bin/ruff check src tests

format:
$(VENV)/bin/black src tests

type:
$(VENV)/bin/mypy src

test:
$(VENV)/bin/pytest

check: lint type test

clean:
rm -rf .pytest_cache .ruff_cache .mypy_cache dist build
