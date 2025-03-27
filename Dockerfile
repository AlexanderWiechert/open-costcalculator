# Stage 1: Basis-Image mit allen Abhängigkeiten (apt und pip)
FROM python:3.9-slim AS base

WORKDIR /app

# Installiere jq und andere System-Dependencies
RUN apt-get update && apt-get install -y jq && rm -rf /var/lib/apt/lists/*

# Installiere Python-Abhängigkeiten
RUN pip install boto3

# Stage 2: Finales Image – Kopiere nur den Anwendungscode
FROM base

WORKDIR /app

# Kopiere den Anwendungscode in den Container
COPY src/aws_pricing.py /app/aws_pricing.py
COPY entrypoint.sh /app/entrypoint.sh

# Mache das Entrypoint-Skript ausführbar
RUN chmod +x /app/entrypoint.sh

# Standardbefehl: Starte das Entrypoint-Skript
CMD ["./entrypoint.sh"]
