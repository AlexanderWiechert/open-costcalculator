**Role:**
You are a DevOps-focused developer working in IntelliJ on an open-source Python CLI project.

---

**Input:**

- Source code in `src/`
- Tests in `tests/`
- Python 3.9.22
- Linting: `black`, `flake8`
- Testing: `pytest`
- GitHub is used for version control and CI/CD
- Project is intended to be published to PyPI later

---

**Steps:**

1. Create `.github/workflows/ci.yml`
2. Trigger on `push` and `pull_request`
3. Use Python 3.9.22
4. Install dependencies from `requirements.txt` and `requirements-dev.txt`
5. Run `black`, `flake8`
6. Run `pytest`
7. Prepare for optional publishing step

---

**Expected Result:**
A functional GitHub Actions workflow that validates code style and test coverage on every push and pull request – and lays the foundation for packaging automation.
