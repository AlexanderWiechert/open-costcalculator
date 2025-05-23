## What works
- Cost analysis for EKS, RDS, ALB, EBS, NAT Gateway
- Pricing query from AWS APIs
- Human-readable CLI output

## What’s left
### AWS resource implementation strategy:

#### ✅ Implemented (cost-relevant)
- eks
- rds
- alb
- ebs
- nat_gateway
- secretsmanager

#### 🟡 Recommended for implementation (cost-relevant)
- aws_db_instance
- aws_lb
- aws_secretsmanager_secret
- aws_route53_zone
- aws_cognito_user_pool
- aws_cloudwatch_log_group
- aws_ses_domain_identity

#### 🟠 Optional for context (indirect cost, dependencies)
- aws_ecs_service
- aws_ecs_cluster
- aws_ecr_repository
- aws_acm_certificate (Private CA only)
- aws_acm_certificate_validation
- aws_ecs_task_definition

#### 🔴 Not cost-relevant (configuration only)
- aws_db_parameter_group
- aws_db_subnet_group
- aws_iam_access_key
- aws_iam_policy
- aws_iam_policy_attachment
- aws_iam_policy_document
- aws_iam_role
- aws_iam_role_policy_attachment
- aws_iam_user
- aws_route53_record
- aws_security_group
- aws_security_group_rule
- aws_ses_email_identity
- aws_ses_domain_mail_from
- aws_ses_domain_dkim
- aws_cognito_user_pool_client
- aws_cognito_identity_provider
- aws_cognito_user_pool_domain

### Codebase improvements planned:
1. Extract repeated logic (e.g. pricing + output) into reusable functions
2. Centralize region configuration instead of hardcoding "EU (Frankfurt)"
3. Encapsulate service-specific pricing logic in dedicated functions
4. Modularize `main()` into component-specific processors (e.g. `process_rds`, `process_eks`, ...)
5. Use logging instead of `print()` for error/warning output

## Known issues and limitations
- No currency conversion
- Limited support for non-standard pricing models (e.g., Reserved Instances)
- AWS API rate limiting not handled gracefully