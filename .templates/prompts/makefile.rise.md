You are setting up a Makefile for an open-source Python CLI project to simplify development tasks for yourself and future contributors.

Your project:

- Uses `src/` layout
- Has test code in `tests/`
- Uses `black` and `flake8` for linting
- Defines dev dependencies in `requirements-dev.txt`
- Uses `pytest` for running tests

Steps:

1. Create a `Makefile` in the project root
2. Add commands for:
   - `make install`: install runtime and dev dependencies
   - `make lint`: run `black` and `flake8` on `src/`
   - `make test`: run `pytest`
   - (optional) `make format`: auto-format using `black`
3. Use consistent variable naming (e.g. `PYTHON = python3.9`)
4. Add short comments to describe each target

Expected output:
A simple but powerful Makefile that standardizes development and quality checks, supports fast onboarding, and reduces command repetition.
