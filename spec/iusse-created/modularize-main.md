# 🛠 Modularize main.py by resource type

We want to break up the logic in `main.py` and route processing for each resource to a modular `process_<service>()` function.

---

### 📦 Implementation Plan

- Create `handlers/` or `resources/<service>/process.py`
- Move service-specific loops from `main.py` to these files
- `main.py` dispatches processing based on active analyzers

---

### 🧪 Tests

- Ensure all analyzers are called correctly
- Validate CLI results remain the same

---

### 🧱 Notes

This makes the codebase more maintainable and readable.
