# ⚙️ Spezifikation: Zentrale Konfiguration via config.yaml

## Ziel

Einführung einer zentralen YAML-basierten Konfigurationsdatei (`config.yaml`) für dynamische Schätzwerte, die für ressourcenabhängige Kostenanalysen notwendig sind.

Diese Konfiguration wird in allen relevanten Analyzer-Komponenten genutzt, um zusätzliche Informationen bereitzustellen, die **nicht direkt im Terraform-Plan enthalten** sind.

---

## Motivation

Terraform-Pläne enthalten **keine echten Nutzungsdaten**, sondern nur Infrastrukturkonfiguration. Für Ressourcen wie S3, SQS, CloudFront, API Gateway etc. sind **Schätzungen notwendig**, z. B.:

- geschätztes Datenvolumen in GB
- Anzahl Requests pro Monat
- erwartete Speicherklasse oder Latenzprofil

Diese Schätzwerte sollen flexibel konfigurierbar sein, unabhängig vom Plan, z. B. über:

- Projektweite Defaults
- Ressourcenbezogene Overrides

---

## Anforderungen

### 🔖 1. Datei: `config.yaml`

**Pfad:** Projektroot (standardmäßig), optional via CLI

**Beispiel:**
```yaml
defaults:
  s3:
    estimated_storage_gb: 100
    estimated_get_requests: 20000
    storage_class: STANDARD

  sqs:
    estimated_requests: 100000

overrides:
  aws_s3_bucket.data_bucket:
    estimated_storage_gb: 500
    storage_class: STANDARD_IA

  aws_sqs_queue.critical:
    estimated_requests: 250000
```

---

### 📦 2. Implementierung: `core/config_loader.py`

```python
import yaml

def load_config(path="config.yaml"):
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}
```

---

### 🧠 3. Verwendung in Analyzer

Beispiel in `s3_analyzer.py`:

```python
from core.config_loader import load_config

config = load_config()
resource_id = "aws_s3_bucket.data_bucket"

values = config.get("overrides", {}).get(resource_id, {})
if not values:
    values = config.get("defaults", {}).get("s3", {})

estimated_gb = float(values.get("estimated_storage_gb", 0))
```

---

### 🧪 4. Testabdeckung

Tests für:
- Existierende Datei mit korrektem YAML
- Fallback auf Defaults
- Fehlen von Datei → kein Crash
- Ressourcenname wird korrekt aufgelöst (z. B. `aws_s3_bucket.bucket1`)
- Zahlentypen, Strings, YAML-Fehlerhandling

---

### 🧰 5. Erweiterung CLI

In `main.py` oder CLI-Wrapper:

```python
parser.add_argument("--config", help="Pfad zur Konfigurationsdatei", default="config.yaml")
```

Dieser Pfad wird dann in `load_config()` übergeben.

---

### 🚧 6. Weiteres

- Linting-Check: Warnung bei nicht aufgelösten Overrides
- Optional: `dry-run`-Modus mit Anzeige der angewandten Defaults

---

## Abhängigkeiten

Diese Spezifikation ist Voraussetzung für:

- ✅ `aws_s3_bucket` Analyzer
- ✅ `aws_sqs_queue` Analyzer
- ⏳ Zukünftig: `cloudfront`, `apigateway`, `lambda`, etc.

---

## Labels

```
labels: core, configuration, enhancement, dependency
```