# OpenCostCalculator

[![CI](https://github.com/AlexanderWiechert/open-costcalculator/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexanderWiechert/open-costcalculator/actions)
[![License](https://img.shields.io/github/license/AlexanderWiechert/open-costcalculator)](LICENSE)

OpenCostCalculator ist ein modulares Python-Tool zur stunden- und monatsgenauen Kostenanalyse von Terraform-basierten AWS-Infrastrukturen. Es liest Terraform-Pläne (im JSON-Format), extrahiert relevante Ressourceninformationen und ermittelt auf Basis der AWS Pricing API dynamisch die geschätzten Kosten pro Ressource.

## 💡 Merkmale

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
- Konfigurierbare Nutzungsannahmen über `config.yaml`
- Ausgabe als Tabelle, JSON oder YAML
- CI-Integration mit GitHub Actions

## 📂 Projektstruktur

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
│   ├── eks/
│   ├── alb/
│   ├── nat_gateway/
│   ├── rds/
│   └── ...
├── tests/                          # Unit-Tests
```

## 📌 Aktueller Milestone

**MVP: Analyzer & Config Support (Q3 2025)**  
🎯 Enthält:
- `config.yaml` Unterstützung
- Analyzer: S3, ECS, LB
- Refactoring: Logging, CLI-Struktur
- Standardisiertes Reporting

👉 Siehe [Projekt-Roadmap](docs/roadmap.md)

## 📦 Installation & Nutzung

```bash
# 1. Klonen
git clone https://github.com/AlexanderWiechert/open-costcalculator.git
cd open-costcalculator

# 2. (Optional) virtuelle Umgebung erstellen
python3 -m venv .venv
source .venv/bin/activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Plan auswerten
python src/main.py --plan plan/terraform-eks.plan.json --debug
```

## 🧪 Tests

```bash
pytest              # Alle Tests ausführen
pytest -v           # Verbosere Ausgabe
pytest tests/test_logger.py  # Einzelner Test
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-report=xml  # Für SonarQube
```

## 🖌️ Codequalität lokal prüfen

```bash
black --line-length 120 src/ tests/
isort src/ tests/
flake8 src/ tests/
```

### Pre-Commit Setup (optional)

```bash
pip install pre-commit
pre-commit install
```

`.pre-commit-config.yaml` Beispiel:
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

## 📊 Beispielausgabe

```text
📊 Cloud Ressourcen Kostenübersicht (pro Monat)
| Komponente       |   Anzahl | Typ         | Kosten    |
|------------------|----------|-------------|-----------|
| Control Plane    |        1 | v1.31       | $73.00000 |
| Node Group (EC2) |        2 | t3.medium   | $29.49200 |
| RDS Instance     |        1 | db.t3.micro | $14.60000 |
| RDS Storage      |       10 | gp2         | $1.15000  |
| NAT Gateway      |        1 | Standard    | $32.85000 |
| ALB (geschätzt)  |        2 | 1.0 LCU     | $44.53000 |
💰 Gesamtkosten/Monat: $195.622
```

## 🤝 Mitwirken

Beiträge willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Hinweise zu Style Guide, Tests und GitHub Flow.

## 📄 Lizenz

Dieses Projekt steht unter der [Apache License 2.0](LICENSE).

Du darfst den Code verwenden, verändern und weitergeben – unter Einhaltung der Bedingungen der Lizenz.

**Autor:** Alexander Wiechert  
**E-Mail:** info@elastic2ls.com