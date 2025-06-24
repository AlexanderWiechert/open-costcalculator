# 🛠 Centralize region configuration

The region is currently hardcoded in several places as "EU (Frankfurt)". We want to support centralized region configuration.

---

### 📦 Implementation Plan

- Create `core/config.py` with `DEFAULT_REGION = "eu-central-1"`
- Add CLI flag `--region` to override it
- Refactor pricing and filter logic to use this setting

---

### 🧪 Tests

- Validate region override via CLI
- Ensure fallbacks work with no region specified

---

### 🧱 Notes

Supports multi-region analysis and prepares the project for broader coverage.
