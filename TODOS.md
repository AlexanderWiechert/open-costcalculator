# costcalculator

### For local testing and development

```bash
python3 -m venv venv
source venv/bin/activate
pip install boto3 pyyaml tabulate pytest
```

## Open Points

### AWS Resources

- aws_acm_certificate
- aws_acm_certificate_validation
- aws_cloudwatch_log_group
- aws_cognito_identity_provider
- aws_cognito_user_pool
- aws_cognito_user_pool_client
- aws_cognito_user_pool_domain
- aws_db_instance
- aws_db_parameter_group
- aws_db_subnet_group
- aws_ecr_repository
- aws_ecs_cluster
- aws_ecs_cluster_capacity_providers
- aws_ecs_service
- aws_ecs_task_definition
- aws_iam_access_key
- aws_iam_policy
- aws_iam_policy_attachment
- aws_iam_policy_document
- aws_iam_role
- aws_iam_role_policy_attachment
- aws_iam_user
- aws_lb
- aws_lb_listener
- aws_lb_listener_rule
- aws_lb_target_group
- aws_route53_record
- aws_route53_zone
- aws_secretsmanager_secret
- aws_secretsmanager_secret_version
- aws_security_group
- aws_security_group_rule
- aws_ses_domain_dkim
- aws_ses_domain_identity
- aws_ses_domain_mail_from
- aws_ses_email_identity

### Optimization Suggestions for main.py

1. Extract recurring code blocks into separate functions

Example: Price calculation and output for EC2, EBS, ALB, NAT Gateway, RDS, Fargate, Control Plane, etc. follow a clear schema:

```python
def add_component(table, label, quantity, type_desc, cost):
    table.append([label, quantity, type_desc, f"${cost:.5f}"])
    return cost
```

2. Configure region centrally

Currently, "EU (Frankfurt)" is hardcoded in several places. Recommended:

```python
REGION = "EU (Frankfurt)"
```

3. Encapsulate service-specific pricing logic

Example:

```python
def calculate_eks_control_plane_cost(plan, hours):
    version = cluster_meta.extract_version(plan)
    if not version:
        return None, 0.0
    release = eks_pricing_meta.get_release_date(version)
    cost = round(calculate_control_plane_cost(release, hours), 5)
    return f"v{version}", cost
```

4. Modularize by components (optional)

The `main()` function is getting long. You could split it into structured subsections:

```python
def process_eks(plan, ...)
def process_node_group(plan, ...)
def process_rds(plan, ...)
def process_nat_gateway(plan, ...)
```

Each return value delivers `List[TableRow]`, `Cost`.

5. Optional: Use logging instead of print() for errors

Instead of:

```python
print("️  Keine capacity_type gefunden – fallback zu 'OnDemand'")
```

→

```python
import logging
logging.warning("No capacity_type found – falling back to 'OnDemand'")
```