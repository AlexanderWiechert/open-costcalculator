## System Architecture
```mermaid
flowchart TD
    CLI["CLI Interface (main.py)"] --> Core["Core Engine"]
    Core --> Parser["Terraform Plan Parser"]
    Core --> Analyzer["Resource Analyzers"]
    Analyzer -->|EKS| EKS[EKS Analyzer]
    Analyzer -->|RDS| RDS[RDS Analyzer]
    Analyzer -->|ALB| ALB[ALB Analyzer]
    Core --> Pricing["AWS Pricing API Module"]
    Core --> Output["Tabular Report Generator"]
```

## Key design principles
- Modularity: Each AWS service is handled in its own module
- Extensibility: Adding new resource support requires minimal integration
- Observability: Debug logs and verbose output options built in

## Patterns used
- Strategy Pattern: Each resource analyzer implements a common interface
- Adapter Pattern: For interaction with AWS Pricing API

## Component relationships
- `main.py` calls the Core Engine
- Core Engine delegates to parsers, analyzers, and output formatters
- Resource modules operate independently and register themselves dynamically