# 🧱 Core refactoring: modularize main, add logging, central config

Restructure the CLI entry point for better modularity and maintainability.

---

### 📌 Goals

- Decouple `main.py` into process modules
- Replace `print()` with `logging`
- Centralize region config in `core/config.py`

---

### 📦 Implementation Plan

#### Modularization

- Move resource processing blocks into `resources/<service>/process.py`
- `main.py` dispatches per active resource

#### Logging

- Use Python `logging` with `getLogger(__name__)`
- Support `--log-level` CLI flag

#### Region config

- Add `DEFAULT_REGION` in `core/config.py`
- Respect `--region` CLI override

---

### 🧪 Test Scenarios

- Logging output shows correct level
- CLI output unchanged
- Resources processed modularly

---

### 🧱 Notes

Foundation for scaling contributors and functionality. Enables better CI integration.
