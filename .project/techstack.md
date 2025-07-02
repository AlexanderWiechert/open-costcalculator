## Technologies used
- Python 3.9+
- Terraform (input format)
- AWS Pricing API
- boto3
- tabulate
- pyyaml

## Development setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Tooling
- pytest for testing
- Makefile for development tasks
- Git for version control

## Known constraints
- Only supports JSON plans (Terraform >= 0.12)
- Requires internet access to query AWS APIs
- Only supports selected AWS services