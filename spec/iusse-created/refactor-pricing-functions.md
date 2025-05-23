# 🛠 Refactor service-specific pricing logic into functions

We want to extract inline pricing logic from `main.py` into reusable, service-specific functions for consistency, reuse, and testability.

---

### 📦 Implementation Plan

- For each supported service (e.g. EKS, RDS), create a `calculate_<service>_cost(data, region)` function
- Move them into `core/pricing.py` or `resources/<service>/costs.py`
- Use the function centrally from `main.py`

---

### 🧪 Tests

- Unit test each pricing function with various cost-relevant inputs
- Ensure snapshot output remains consistent

---

### 🧱 Notes

This improves testability, modularity, and consistency of cost logic.
