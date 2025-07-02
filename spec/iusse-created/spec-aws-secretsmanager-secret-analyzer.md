# 🔍 Add analyzer for aws_secretsmanager_secret resources

We want to support cost analysis for **aws_secretsmanager_secret** resources defined in Terraform plans.

This analyzer should:
- Identify all relevant Terraform resources of type `aws_secretsmanager_secret`
- Extract pricing-relevant attributes (e.g. size, region, retention, usage-based settings)
- Use the AWS Pricing API or fallback definitions in `services.json`
- Report monthly cost impact for each instance of the resource

---

### 📦 Implementation Plan

Create a new analyzer under:

```
resources/secretsmanager_secret/
├── costs.py
├── filters.py
└── meta.py
```

Extract the relevant attributes for `aws_secretsmanager_secret` from the Terraform JSON plan and calculate:
- Estimated monthly cost
- Usage-based components (if applicable)
- Tiered pricing (if applicable)

---

### 🧪 Test Scenarios

- Minimal example with 1 resource
- Complex example with custom configuration
- Edge cases: unknown attributes, missing data

> Test plans should be stored under `plan/terraform-secretsmanager_secret.plan.json`

---

### 🧱 Notes

- Integrate with CLI report output
- Add to `README.md` as a supported resource
- Update `progress.md` status after implementation