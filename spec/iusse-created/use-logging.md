# 🛠 Replace print() with structured logging

We want to replace all `print()` and direct `sys.stderr` calls with the standard Python `logging` module for consistency and CI integration.

---

### 📦 Implementation Plan

- Use `logging.getLogger(__name__)` in all files
- Replace print and stderr with appropriate log levels (info, warning, error)
- Add CLI flag `--log-level` to control verbosity

---

### 🧪 Tests

- Validate log messages appear in CLI
- Confirm `--log-level` works as expected

---

### 🧱 Notes

Improves CI/CD integration, structured debugging, and production readiness.
