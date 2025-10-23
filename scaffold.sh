#!/usr/bin/env bash
set -euo pipefail

ROOT="python-learning-program"
mkdir -p "$ROOT"/{src/app,tests,.github/workflows,resources}

# .gitignore
cat > "$ROOT/.gitignore" << 'EOT'
.venv/
__pycache__/
*.pyc
.DS_Store
.pytest_cache/
.ruff_cache/
.mypy_cache/
.env
dist/
build/
.idea/
.vscode/
EOT

# pyproject.toml (habilitamos 3.10+; puedes editar luego a 3.14)
cat > "$ROOT/pyproject.toml" << 'EOT'
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "python-learning-program"
version = "0.1.0"
description = "Programa de aprendizaje de Python 2025 (plantilla)"
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[tool.black]
line-length = 100
target-version = ["py310","py311","py312","py313"]

[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E","F","W","I","UP","B"]
ignore = ["E203","E501"]
src = ["src"]
exclude = ["dist","build",".venv",".mypy_cache",".ruff_cache"]

[tool.pytest.ini_options]
addopts = "-q"
testpaths = ["tests"]
EOT

# requirements
cat > "$ROOT/requirements.txt" << 'EOT'
# Dependencias de runtime (puede quedar vacío al inicio)
EOT

cat > "$ROOT/requirements-dev.txt" << 'EOT'
pytest>=7.0
black>=24.0
ruff>=0.5.0
mypy>=1.8.0
EOT

# Makefile (si no tienes 'make', más abajo te dejo comandos equivalentes)
cat > "$ROOT/Makefile" << 'EOT'
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
EOT

# pytest, editorconfig, env de ejemplo
cat > "$ROOT/pytest.ini" << 'EOT'
[pytest]
addopts = -q
testpaths = tests
EOT

cat > "$ROOT/.editorconfig" << 'EOT'
root = true
[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true
EOT

cat > "$ROOT/.env.example" << 'EOT'
APP_ENV=development
LOG_LEVEL=INFO
EOT

# CI opcional (GitHub Actions)
cat > "$ROOT/.github/workflows/ci.yml" << 'EOT'
name: CI
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkoutv4
      - uses: actions/setup-pythonv5
        with:
          python-version: '3.12'
      - name: Instalar dependencias
        run: |
          python -m pip install -U pip
          pip install -r requirements-dev.txt
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Lint
        run: ruff check src tests
      - name: Format (check)
        run: black --check src tests
      - name: Tests
        run: pytest -q
EOT

# Código de ejemplo + test que debe pasar
cat > "$ROOT/src/app/__init__.py" << 'EOT'
# Paquete de ejemplo
EOT

cat > "$ROOT/src/app/hello.py" << 'EOT'
def greeting(name: str) -> str:
    return f"Hola, {name}!"
EOT

cat > "$ROOT/tests/test_hello.py" << 'EOT'
from app.hello import greeting

def test_greeting():
    assert greeting("Python") == "Hola, Python!"
EOT

# Placeholders para tus documentos (pégalos luego)
cat > "$ROOT/README.md" << 'EOT'
# (Pega aquí el "Plan de Estudio Secuencial de Python 2025  Documento operativo (010)")
EOT

cat > "$ROOT/Calendario.md" << 'EOT'
# (Pega aquí el "Calendario del Programa (24 semanas)")
EOT

cat > "$ROOT/resources/videos.md" << 'EOT'
# (Pega aquí el índice maestro de videos  fuente única de verdad)
EOT

echo "-------------------------------------------"
echo "Plantilla creada en: $ROOT"
echo "Siguientes pasos:"
echo "  cd $ROOT"
echo "  # (elige A o B)"
echo "  # A) Con make:"
echo "  #    make install && make check"
echo "  # B) Sin make (comandos equivalentes):"
echo "  #    python -m venv .venv && source .venv/Scripts/activate"
echo "  #    python -m pip install -U pip"
echo "  #    pip install -r requirements-dev.txt"
echo "  #    ruff check src tests && black --check src tests && pytest -q"
echo "-------------------------------------------"
EOT
