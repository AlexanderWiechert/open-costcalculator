# 🛠 Refactor report formatting into central module

We want to unify output formatting (table, json, yaml) under a single formatting interface for easier maintenance and expansion.

---

### 📦 Implementation Plan

- Define a common output model, e.g. `ReportEntry`
- Move format-specific code to:
  - `report/format_table.py`
  - `report/format_json.py`
  - `report/format_yaml.py`
- `main.py` and all analyzers output data using this structure

---

### 🧪 Tests

- Snapshot test output in all formats
- Validate all analyzers emit correct output

---

### 🧱 Notes

This will make CLI output consistent and help support future formats (CSV, HTML, etc.)
