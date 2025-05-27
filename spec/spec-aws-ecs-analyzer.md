# 📦 Analyzer: AWS ECS (Service + Task Definition)

## Ziel
Analysiert ECS-Dienste und Task-Definitionen aus Terraform-Plänen zur Berechnung monatlicher Compute-Kosten – unterstützt `FARGATE` und `EC2`.

## Ressourcen
- `aws_ecs_task_definition`
- `aws_ecs_service`

## Fokus: FARGATE (v1)
Die erste Version konzentriert sich auf FARGATE-basierte Services.

## Berechnung
- CPU + RAM aus `task_definition`
- `desired_count` aus `ecs_service`
- Monatlicher Preis = Stundenpreis * 730 * Anzahl

## Felder
- `cpu`, `memory` aus `task_definition`
- `launch_type`, `desired_count`, `task_definition` aus `ecs_service`

## API
Die Preise werden **nicht** aus statischen Defaults gezogen, sondern sollen über die AWS Pricing API geladen werden (siehe `pricing_utils.py`).

## Ausgabe
- Einheitlich strukturiert (wie bei EKS, RDS)
- Ausgabe als Tabelle oder JSON

## Testfälle
- `FARGATE` mit gültigen Werten
- `FARGATE` ohne `desired_count` (Fallback = 1)
- `EC2` als Launchtyp (derzeit ignorieren)