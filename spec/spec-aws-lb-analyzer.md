# 📦 Analyzer: AWS Load Balancer (LB + Listener + Target Group)

## Ziel
Analysiert `aws_lb`, `aws_lb_listener`, `aws_lb_target_group` Ressourcen im Terraform-Plan zur Ermittlung monatlicher Kosten.

## Unterstützte Typen
- `application`
- `network`
- `gateway`
- regional/zonal LBs

## Kostenarten
- Pro-Stunde-Kosten je LB (abhängig vom Typ)
- Listener-Kosten (je nach Protokoll)
- Request-basierte Kosten (optionaler Zusatz, basiert auf Annotation wie `estimated_requests_per_month`)

## Datenquelle
- **AWS Pricing API**
- Region wird aus dem Plan extrahiert

## Terraform-Felder (Beispiele)
- `load_balancer_type`, `internal`, `idle_timeout`
- `protocol` bei Listenern
- `port`, `target_type` in Target Groups

## Ausgabe
- Einheitlich: Tabelle, JSON (via CLI `--output-format`)
- Enthält Details + monatliche Gesamtkosten

## Testszenarien
- ALB + Listener + TargetGroup vollständig
- Gateway LB mit minimaler Konfiguration
- Fehlende Felder → Default-Verhalten