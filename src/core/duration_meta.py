# filter/duration_meta.py

# Standarddauer für Kostenberechnung (Monatsbasis, AWS verwendet oft 730 Std.)
HOURS_PER_MONTH = 730

# Optional für spätere Erweiterung:
HOURS_PER_DAY = 24
DAYS_PER_MONTH = 30.42  # AWS-relevant
DAYS_PER_YEAR = 365

# Jahresstunden – nützlich für Hochrechnungen
HOURS_PER_YEAR = int(DAYS_PER_YEAR * HOURS_PER_DAY)
