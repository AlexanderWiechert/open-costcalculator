![OpenCostCalculator Logo](OpenCostCalculator_CloudGreen.svg)

---

# OpenCostCalculator

[![CI](https://github.com/AlexanderWiechert/open-costcalculator/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexanderWiechert/open-costcalculator/actions)
[![License](https://img.shields.io/github/license/AlexanderWiechert/open-costcalculator)](LICENSE)

**OpenCostCalculator** is a modular Python tool for hourly and monthly cost analysis of Terraform-based AWS infrastructures. It parses Terraform plans (in JSON format), extracts relevant resource data, and dynamically calculates estimated costs per resource using the AWS Pricing API.

## Project Status
> This project is under active development. Features are experimental and subject to change. Feedback and pull requests are very welcome!


## Vision
OpenCostCalculator aims to be a modular, transparent, and extensible CLI tool for cost analysis of Terraform-based cloud infrastructures — with a strong focus on **AWS, clarity, and automation**. It aspires to be an open alternative to proprietary tools like Infracost, designed to integrate seamlessly into existing DevOps workflows.

## Features

- Analyze AWS resources directly from Terraform plans (`terraform plan -out=... | show -json`)
- Dynamic pricing via AWS Pricing API and EC2 Spot API
- Support for:
    - EKS Clusters & Node Groups (On-Demand & Spot)
    - Fargate Profiles
    - EBS Volumes
    - NAT Gateways
    - RDS Instances & Storage
    - ALBs (estimated LCU usage)
- Clearly formatted cost overview as a table
- Modular design: each AWS resource can be extended via dedicated modules
- Debug logging and extendable filtering logic
- Configurable usage assumptions via `config.yaml`
- Output as table, JSON, or YAML
- CI integration using GitHub Actions

## Project Structure

```
src/
│
├── main.py                         # Entry point of the tool
│
├── core/                           # Shared logic (args, logging, pricing)
│   ├── arg_utils.py
│   ├── duration_meta.py
│   ├── logger.py
│   ├── pricing_utils.py
│
├── resources/
│   ├── eks/
│   ├── alb/
│   ├── nat_gateway/
│   ├── rds/
│   └── ...
├── tests/                          # Unit tests
```

## Current Milestone

**MVP: Analyzer & Config Support (Q3 2025)**  
🎯 Includes:
- `config.yaml` support
- Analyzer: S3, ECS, LB
- Refactoring: Logging, CLI structure
- Standardized reporting

See [Project Roadmap](docs/roadmap.md)

## 📦 Installation & Usage

```bash
# 1. Clone
git clone https://github.com/AlexanderWiechert/open-costcalculator.git
cd open-costcalculator

# 2. (Optional) create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Run cost analysis
python src/main.py --plan plan/terraform-eks.plan.json --debug
```

## Tests

```bash
pytest              # Run all tests
pytest -v           # Verbose output
pytest tests/test_logger.py  # Run specific test
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-report=xml  # For SonarQube
```

## Check code quality locally

```bash
black --line-length 120 src/ tests/
isort src/ tests/
flake8 src/ tests/
```

### Pre-commit setup (optional)

```bash
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml` example:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        args: ["--line-length", "120"]

  - repo: https://github.com/pre-commit/mirrors-isort
    rev: v5.12.0
    hooks:
      - id: isort
```

## Sample Output

```text
📊 Cloud Resource Cost Overview (per month)
| Component        |   Count | Type        | Cost      |
|------------------|---------|-------------|-----------|
| Control Plane    |       1 | v1.31       | $73.00000 |
| Node Group (EC2) |       2 | t3.medium   | $29.49200 |
| RDS Instance     |       1 | db.t3.micro | $14.60000 |
| RDS Storage      |      10 | gp2         | $1.15000  |
| NAT Gateway      |       1 | Standard    | $32.85000 |
| ALB (estimated)  |       2 | 1.0 LCU     | $44.53000 |
 Total Monthly Cost: $195.622
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for style guide, testing, and GitHub Flow information.

## License

This project is licensed under the [Apache License 2.0](LICENSE).

You are free to use, modify, and distribute the code – as long as you comply with the license terms.

**Author:** Alexander Wiechert  
**Email:** info@elastic2ls.com