# OpenCostCalculator

OpenCostCalculator ist ein modulares Python-Tool zur stunden- und monatsgenauen Kostenanalyse von Terraform-basierten AWS-Infrastrukturen. Es liest Terraform-Pläne (im JSON-Format), extrahiert relevante Ressourceninformationen und ermittelt auf Basis der AWS Pricing API dynamisch die geschätzten Kosten pro Ressource.

## Merkmale

- Analyse von AWS-Ressourcen direkt aus Terraform-Plänen (`terraform plan -out=... | show -json`)
- Dynamische Preisermittlung via AWS Pricing API und EC2 Spot API
- Unterstützung für:
  - EKS Cluster & Node Groups (On-Demand & Spot)
  - Fargate-Profile
  - EBS Volumes
  - NAT Gateways
  - RDS Instanzen & Storage
  - ALBs (geschätzte LCU-Nutzung)
- Klar formatierte Kostenübersicht als Tabelle
- Modular aufgebaut: jede AWS-Ressource ist über eigene Module erweiterbar
- Debug-Logging und erweiterbare Filter-Logik

## Projektstruktur

```
src/
│
├── main.py                         # Einstiegspunkt des Tools
│
├── core/                           # Gemeinsame Logik (Argumente, Logging, Preise)
│   ├── arg_utils.py
│   ├── duration_meta.py
│   ├── logger.py
│   ├── pricing_utils.py
│
├── resources/
│   ├── eks/                        # EKS-spezifische Logik
│   │   ├── cluster_meta.py
│   │   ├── control_plane_costs.py
│   │   ├── ec2_filters.py
│   │   ├── eks_pricing_meta.py
│   │   ├── fargate_costs.py
│   │   ├── nodegroup_costs.py
│   │   ├── nodegroup_meta.py
│   │
│   ├── alb/
│   │   ├── alb_costs.py
│   │
│   ├── nat_gateway/
│   │   ├── nat_gateway_costs.py
│   │   ├── nat_gateway_meta.py
│
│   ├── rds/
│   │   ├── rds_costs.py
│   │   ├── rds_filters.py
│   │   ├── rds_meta.py
│   │   ├── rds_utils.py
│
├── tests/                          # Unit-Tests
│   ├── test_logger.py
│   ├── test_ec2_filters.py
│   ├── test_pricing_utils.py
│   ├── ...
```

## Voraussetzungen

- Python 3.10 oder höher
- AWS-Zugangsdaten via `~/.aws/credentials` oder Umgebungsvariablen
- Terraform Plan im JSON-Format (`terraform show -json terraform.plan > terraform.plan.json`)
- Installierte Dependencies:

```bash
# 1. Virtuelle Umgebung erstellen
python3 -m venv .venv

# 2. Aktivieren
source .venv/bin/activate

# 3. Pakete installieren
pip3 install -r requirements.txt
```

## Nutzung

```bash
cd src
python main.py --plan ../test/terraform-eks.plan.json
```

Optional mit Debug-Ausgabe:

```bash
python main.py --plan ../test/terraform-eks.plan.json --debug
```

## Beispielausgabe

```
📊 Cloud Ressourcen Kostenübersicht (pro Monat)
| Komponente      |   Anzahl | Typ         | Kosten    |
|-----------------|----------|-------------|-----------|
| Control Plane    |        1 | v1.31       | $73.00000 |
| Node Group (EC2) |        2 | t3.medium   | $29.49200 |
| RDS Instance     |        1 | db.t3.micro | $14.60000 |
| RDS Storage      |       10 | gp2         | $1.15000  |
| NAT Gateway      |        1 | Standard    | $32.85000 |
| ALB (geschätzt)  |        2 | 1.0 LCU     | $44.53000 |
💰 Gesamtkosten/Monat: $195.622
```

## Tests

Das Projekt enthält Unit-Tests für zentrale Module:

### Ausführen aller Tests

```bash
pytest
```

### Einzelnen Test ausführen

```bash
pytest tests/test_logger.py
```

### Coverage Report

```bash
pytest --cov=src --cov-report=term-missing
```

Für SonarQube kannst du zusätzlich folgenden Report erzeugen:

```bash
pytest --cov=src --cov-report=xml
```

## Lizenz

**Proprietäre Lizenz – Alle Rechte vorbehalten**

Dieses Projekt ist urheberrechtlich geschützt und darf ohne ausdrückliche Genehmigung des Autors nicht kopiert, verbreitet, verändert oder kommerziell genutzt werden. Forks, Klone oder die Nutzung in anderen Projekten sind nicht erlaubt.

Für Kooperationen oder kommerzielle Nutzung bitte Kontakt aufnehmen.

---

**Autor:** Alexander Wiechert  
**E-Mail:** info@elastic2ls.com