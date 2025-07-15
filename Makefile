# ┌───────────────────────────────────────────────────────┐
# │   Makefile for Cython → C-extension → Wheel → Install  │
# └───────────────────────────────────────────────────────┘

# You can override these on the command line, e.g.
#   make PYTHON=python   or   make PIP=~/venv/bin/pip
PYTHON  := python3
PIP     := pip3

# Output directories
BUILD_DIR         := build
CYTHON_BUILD_DIR  := $(BUILD_DIR)/cython
ANNOTATION_DIR    := $(BUILD_DIR)/annotations
DIST_DIR          := dist

# Default target
.PHONY: all
all: wheel

# ──────────────────────────────────────────────────────
# 1) Generate C sources & HTML annotations and compile
# ──────────────────────────────────────────────────────
.PHONY: cython build
cython:
	@echo "→ Cythonizing & building extensions in place…"
	$(PYTHON) setup.py build_ext --inplace

# alias
build: cython

# ──────────────────────────────────────────────────────
# 2) Build a wheel archive
# ──────────────────────────────────────────────────────
.PHONY: wheel
wheel:
	@echo "→ Building wheel via PEP 517 build…"
	$(PYTHON) -m build --wheel --outdir $(DIST_DIR)

# ──────────────────────────────────────────────────────
# 3) Install / reinstall the wheel
# ──────────────────────────────────────────────────────
.PHONY: install
install: wheel
	@echo "→ Installing wheel…"
	$(PIP) install --force-reinstall $(DIST_DIR)/*.whl

# ──────────────────────────────────────────────────────
# 4) Clean up every generated, compiled, or temporary file
# ──────────────────────────────────────────────────────
.PHONY: clean
clean:
	@echo "→ Cleaning build artifacts…"
	rm -rf $(BUILD_DIR) $(DIST_DIR) *.egg-info
	find . -type f \( -name '*.c' -o -name '*.html' \) -delete
