# 🔄 Compare Terraform plans (delta cost analysis)

We want to introduce a new CLI feature that compares two Terraform plan JSON files and calculates the cost delta per resource and service.

---

### 📌 Goal

Enable developers and reviewers to assess the cost impact of infrastructure changes in PRs or deployments.

---

### 📦 Implementation Plan

- Add CLI command: `compare-plan`
  ```bash
  open-costcalculator compare-plan --old plan/old.plan.json --new plan/new.plan.json
  ```
- Parse both plans using existing plan reader and resource filters
- Match resources by type and name
- Compute:
  - cost difference per resource
  - net delta per service type
  - total delta

- Extend report module with delta-aware rendering
- Optional: emit Markdown summary for CI

---

### 🧪 Test Scenarios

- Resource added: new db instance appears only in new plan
- Resource removed: RDS present in old, not in new
- Resource changed: instance type modified
- No change

---

### 🧱 Notes

Supports CI workflows by showing cost changes before merge. Also enables FinOps feedback during review.
