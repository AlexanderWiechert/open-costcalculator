# costcalculator




### zum lokalen teste und entwickeln
python3 -m venv venv
source venv/bin/activate
pip install boto3 pyyaml tabulate pytest

## Offene Punkte
### AWS-Ressourcen

    aws_acm_certificate

    aws_acm_certificate_validation

    aws_cloudwatch_log_group

    aws_cognito_identity_provider

    aws_cognito_user_pool

    aws_cognito_user_pool_client

    aws_cognito_user_pool_domain

    aws_db_instance

    aws_db_parameter_group

    aws_db_subnet_group

    aws_ecr_repository

    aws_ecs_cluster

    aws_ecs_cluster_capacity_providers

    aws_ecs_service

    aws_ecs_task_definition

    aws_iam_access_key

    aws_iam_policy

    aws_iam_policy_attachment

    aws_iam_policy_document

    aws_iam_role

    aws_iam_role_policy_attachment

    aws_iam_user

    aws_lb

    aws_lb_listener

    aws_lb_listener_rule

    aws_lb_target_group

    aws_route53_record

    aws_route53_zone

    aws_secretsmanager_secret

    aws_secretsmanager_secret_version

    aws_security_group

    aws_security_group_rule

    aws_ses_domain_dkim

    aws_ses_domain_identity

    aws_ses_domain_mail_from

    aws_ses_email_identity


### Optimierungsvorschläge für main.py
1. Wiederkehrende Codeblöcke in eigene Funktionen auslagern

Beispiel: Die Preisberechnung + Ausgabe für EC2, EBS, ALB, NAT Gateway, RDS, Fargate, Control Plane etc. – diese folgen einem klaren Schema:

def add_component(table, label, quantity, type_desc, cost):
table.append([label, quantity, type_desc, f"${cost:.5f}"])
return cost

2. Region zentral konfigurieren

Aktuell ist "EU (Frankfurt)" mehrfach hartcodiert. Empfehlung:

REGION = "EU (Frankfurt)"

3. Service-spezifische Preislogik kapseln

Beispiel:

def calculate_eks_control_plane_cost(plan, hours):
version = cluster_meta.extract_version(plan)
if not version:
return None, 0.0
release = eks_pricing_meta.get_release_date(version)
cost = round(calculate_control_plane_cost(release, hours), 5)
return f"v{version}", cost

4. Modularisieren nach Komponenten (optional)

Die Hauptfunktion main() wird bald zu lang. Du könntest sie in strukturierte Unterabschnitte aufteilen wie z. B.:

def process_eks(plan, ...)
def process_node_group(plan, ...)
def process_rds(plan, ...)
def process_nat_gateway(plan, ...)

Jeder Rückgabewert liefert List[TableRow], Cost.
5. Optional: Logging statt print() für Fehler

Statt:

print("⚠️  Keine capacity_type gefunden – fallback zu 'OnDemand'")

→

import logging
logging.warning("Keine capacity_type gefunden – fallback zu 'OnDemand'")
