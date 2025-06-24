# 📦 Analyzer: AWS S3 Bucket

## Ziel
Analysiere `aws_s3_bucket` Ressourcen im Terraform-Plan zur Berechnung der monatlichen Speicherkosten – basierend auf Storage-Klasse, geschätztem Datenvolumen und API-Nutzung.

## Unterstützte Merkmale
- `storage_class`: STANDARD, STANDARD_IA, GLACIER
- `versioning`, `server_side_encryption`
- API-Zugriffe (GET, PUT, DELETE)
- Mindestgrößen, Mindestdauer (z. B. IA: 30 Tage, Glacier: 90 Tage)

## Kostenfaktoren
- GB pro Monat (Pflicht, über `config.yaml` oder Tags)
- API-Zugriffe pro Monat (`estimated_get_requests`, `estimated_put_requests`)
- Berücksichtige Mindestabrechnungszeit und Mindestgröße (z. B. 128 KB/30 Tage bei IA)

## Datenquelle
- AWS Pricing API
- Region wird aus Plan extrahiert

## Konfiguration (`config.yaml`)
Die Schätzwerte für Datenvolumen, Requests und Storage-Class werden in einer YAML-Konfigurationsdatei übergeben:

```yaml
defaults:
  s3:
    estimated_storage_gb: 100
    estimated_get_requests: 20000
    storage_class: STANDARD

overrides:
  aws_s3_bucket.data_bucket:
    estimated_storage_gb: 500
    storage_class: STANDARD_IA
```

## Fallback
- Wenn keine Werte in `config.yaml` vorhanden sind, wird im Plan nach Tags gesucht
- Wenn beides fehlt, erfolgt Warnung oder Default

## Ausgabe
- Strukturiert als Tabelle oder JSON
- Monatliche Gesamtkosten + Aufschlüsselung

## Testszenarien
- S3 Bucket mit `STANDARD_IA` und 500 GB
- S3 Bucket mit `GLACIER`, aber nur 1 Monat Nutzung
- Versioning aktiviert → doppelter Speicherverbrauch
- Kein config vorhanden → Warnung
- Nur Defaultwerte vorhanden