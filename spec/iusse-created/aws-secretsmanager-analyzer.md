# 🔍 Add analyzer for aws_secretsmanager_secret resources

We want to support cost analysis for **AWS Secrets Manager** secrets defined in Terraform plans.

This analyzer should handle:
- Fixed monthly costs per secret
- Optional cost impact of automatic rotation (if enabled)
- Pricing per region (if applicable)
- Optionally support `aws_secretsmanager_secret_version`

---

### 📦 Implementation Plan

Create a new analyzer under:

```
resources/secretsmanager/
├── secrets_costs.py
├── secrets_filters.py
└── secrets_meta.py
```

Extract the following attributes from each `aws_secretsmanager_secret` resource in the Terraform plan:
- `name`
- `rotation_enabled`
- `kms_key_id` (optional, may affect pricing in future)

Use the AWS Pricing API or `services.json` fallback for:
- Monthly cost per secret
- Additional costs for rotation (optional, if priced separately)

Output:
- Service: `Secrets Manager`
- Resource type: `Secret`
- Total monthly cost (per secret)
- Optional: rotation flag, kms usage

---

### 🧪 Test Scenarios

- One secret, no rotation
- One secret, with rotation enabled
- Multiple secrets
- Secrets with edge cases (e.g. missing `rotation_enabled`)

> Plan examples should be stored as `plan/terraform-secretsmanager.plan.json`

---

### 🧱 Notes

- Integrate with existing CLI output logic
- Document the new analyzer in `README.md`
- Mark the resource as implemented in `progress.md`
