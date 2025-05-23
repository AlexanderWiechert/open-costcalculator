You are a contributor to an open-source CLI project that analyzes AWS resource costs from Terraform plans. The project supports modular analyzers, each located in its own subdirectory under `src/resources/`.

Each analyzer needs to be tested with a realistic Terraform plan JSON to ensure it works as expected.

The project expects Terraform plans to be stored in the `/plan/` directory for development and testing purposes.

Steps:
1. For each implemented analyzer (e.g., `alb`, `rds`, `nat_gateway`), create a minimal but valid Terraform configuration in HCL that includes one or more resources of that type.
2. Generate the corresponding Terraform plan using:
   ```bash
   terraform init
   terraform plan -out=tfplan.binary
   terraform show -json tfplan.binary > /plan/terraform-<resource>.plan.json
   ```
3. Save the resulting file as `/plan/terraform-<resource>.plan.json`, using the lowercase name of the resource module (e.g. `terraform-alb.plan.json`, `terraform-rds.plan.json`)
4. Ensure the resource configuration is representative of a real-world scenario, including any attributes used in pricing (e.g. instance size, region, tier)
5. Document any assumptions or special conditions in a comment block at the top of the `.tf` file (e.g. "uses free tier eligible resources")

Expected output:
Each analyzer module has an associated JSON Terraform plan example stored in `/plan/`, which can be used for local testing, CI validation, and automated regression checks.
