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
pip install boto3 pyyaml