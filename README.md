# costcalculator

Dieses Repository enthält ein einfaches Beispiel, um AWS-Preisinformationen über die AWS Pricing API mit Python und boto3 abzurufen. Zudem wird gezeigt, wie du das Python-Skript in einem Docker-Container betreibst und dein lokales AWS-Credentials-Verzeichnis mountest.

## Inhalt

- **aws_pricing.py**: Python-Skript zur Abfrage von Preisinformationen für eine EC2 t2.micro-Instanz in US East (N. Virginia) unter Linux.
- **Dockerfile**: Docker-Konfiguration, um das Skript in einem Container auszuführen.
- **README.md**: Diese Anleitung.

## Voraussetzungen

- Ein aktives AWS-Konto mit gültigen Zugangsdaten.
- Lokales AWS-Credentials-Verzeichnis (üblicherweise `~/.aws`), das deine AWS-Zugangsdaten enthält.
- Docker (zum Erstellen und Ausführen des Containers).
- Python (wenn du das Skript lokal testen möchtest).

## Nutzung

### 1. AWS-Zugangsdaten konfigurieren

Stelle sicher, dass dein lokales `~/.aws`-Verzeichnis deine AWS-Zugangsdaten enthält. Beispiel für `~/.aws/credentials`:

```bash
[default]
aws_access_key_id = DEINE_ACCESS_KEY_ID
aws_secret_access_key = DEIN_SECRET_ACCESS_KEY
```

### 2. Docker-Image bauen

Wechsle in den Ordner, in dem sich die Dateien befinden, und führe folgenden Befehl aus:

```bash
docker build -t aws-pricing .
```

### 3. Container starten

Starte den Container und mounte dein lokales ~/.aws-Verzeichnis in den Container:

```bash
docker run -v ~/.aws:/root/.aws aws-pricing
```

Der Container führt nun das Skript aus und gibt die AWS-Preisinformationen aus.

#ohne container 

python3 -m venv venv
source venv/bin/activate
pip install boto3 pyyaml tabulate


#☁️ AWS-Ressourcen

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


# ✅ Optimierungsvorschläge für main.py
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
