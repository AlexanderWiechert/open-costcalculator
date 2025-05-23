## Why this project exists
Cloud infrastructure costs are often intransparent and hard to attribute to specific services or architectural decisions. The OpenCostCalculator project exists to close this gap by providing a modular CLI tool that analyzes Terraform plans and estimates AWS costs per resource using real-time data from the AWS Pricing APIs.

## Problem being solved
- Incomplete visibility into AWS resource costs during the planning phase
- Manual or inaccurate estimations of costs
- Lack of detailed cost breakdown per service or resource

## How the project should work
- Accepts a Terraform plan in JSON format
- Parses the resource definitions
- Queries AWS Pricing APIs to retrieve up-to-date pricing data
- Maps prices to individual resources and usage patterns (e.g., EC2 Spot, EBS IOPS)
- Outputs a human-readable cost report as a table, grouped by service

## High-level overview of development
- Modular Python architecture with resource-specific analyzers (e.g., EKS, RDS, ALB)
- Central CLI interface in `main.py`
- Uses `boto3`, `tabulate`, and optional filters for extensibility

## Core requirements and goals
- Provide cost transparency before deployment
- Support major AWS services used in typical production infrastructures
- Be extensible to new resources and pricing models
- Easy integration in CI/CD pipelines and developer workflows