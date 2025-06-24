# Contributing to OpenCostCalculator

Thank you for your interest in contributing to **OpenCostCalculator**! This guide outlines the process for reporting issues, suggesting features, and contributing code.

---

## 🧭able of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Standards](#development-standards)
- [Testing](#testing)
- [Commit and GitHub Flow](#commit-and-github-flow)

---

## Code of Conduct

Please be respectful and inclusive in your interactions. See the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) as the basis for behavior.

---

## Getting Started

1. **Fork** this repository and clone your fork:
   ```bash
   git clone https://github.com/<your-username>/open-costcalculator.git
   cd open-costcalculator
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

---

## How to Contribute

### Bug Reports

Please include:
- A short description of the bug
- Reproduction steps (if possible, include Terraform plan snippet or command)
- Environment information (Python version, OS)

### Feature Requests

Describe the problem your feature solves and suggest a clear implementation direction if possible.

### Code Contributions

We welcome improvements to:
- New AWS resource analyzers
- CLI enhancements
- Output formatting
- Logging or configuration improvements

---

## Development Standards

- Follow [PEP8](https://pep8.org/) and use `black` and `isort` for formatting:
  ```bash
  black --line-length 120 src/ tests/
  isort src/ tests/
  ```

- Keep functions small and modular.

- Use logging over `print()` for all runtime messages:
  ```python
  import logging
  logging.warning("Example warning message")
  ```

- Prefer clear naming over comments.

---

## Testing

We use `pytest`. Run tests with:
```bash
pytest
```

Add tests in the `tests/` directory. Cover new modules and logic with unit tests.

To check test coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

---

## Commit and GitHub Flow

- Use feature branches (`feature/xyz`, `bugfix/abc`)
- Follow [Conventional Commits](https://www.conventionalcommits.org/):
    - `feat:` for new features
    - `fix:` for bug fixes
    - `docs:` for documentation only
    - `refactor:` for internal changes
- Example:
  ```
  feat(rds): add support for gp3 volumes
  ```

After opening a PR, please describe what your changes do and link any related issues.

---

Thanks for making OpenCostCalculator better! 