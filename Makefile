# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
SRC = ./src/main.py
EXE_NAME = main

# Default target
.DEFAULT_GOAL := help

.PHONY: help setup run build clean

help:
	@echo "Available targets:"
	@echo "  make setup   - Create virtual env and install dependencies"
	@echo "  make run     - Run main.py (requires setup)"
	@echo "  make build   - Build executable with PyInstaller (requires setup)"
	@echo "  make clean   - Remove all generated files"

# Set up virtual environment and install dependencies
setup:
	@echo "Creating virtual environment..."
	python -m venv $(VENV)
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt
	$(PIP) install pyinstaller
	@echo "Setup complete. Activate with 'source $(VENV)/bin/activate'"

# Run the script (ensure venv exists and use its Python)
run: $(VENV)/bin/python
	@echo "Running script..."
	$(PYTHON) $(SRC)

# Build executable (ensure venv exists and use its PyInstaller)
build: $(VENV)/bin/python
	@echo "Building executable..."
	$(VENV)/bin/pyinstaller --onefile --name $(EXE_NAME) $(SRC)
	@echo "Executable created in dist/"

# Rule to ensure venv exists (shared dependency for run/build)
$(VENV)/bin/python:
	@echo "Error: Virtual environment not found. Run 'make setup' first."
	@exit 1

# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf __pycache__ src/__pycache__
	rm -rf build dist *.spec
	@echo "Clean complete"