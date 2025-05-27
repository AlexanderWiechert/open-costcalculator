# 🏷️ Group costs by Terraform tags (e.g. project/team)

Introduce a grouping feature that enables summarizing cloud cost data by tag, such as `tag.Project`, `tag.Environment`, etc.

---

### 📌 Goal

Allow FinOps and engineering teams to attribute cost by project or team using existing tagging conventions.

---

### 📦 Implementation Plan

- Add CLI flag: `--group-by tag.<key>`
- During resource filtering:
  - extract `tags` map
  - lookup the specified key
- Aggregate cost per unique tag value
- Extend report output for:
  - table
  - JSON
  - YAML

---

### 🧪 Test Scenarios

- Two RDS resources with `tag.Project=foo`
- One EC2 with no tag → grouped as "unlabeled"
- Mixed resource types

---

### 🧱 Notes

Supports cost attribution, reporting, and integration with governance tooling.
