# pricing_defaults.py
# Enthält Standardkostenwerte für AWS-Komponenten

# EKS Control Plane Pricing (https://aws.amazon.com/eks/pricing/)
CONTROL_PLANE_STANDARD_RATE = 0.10  # USD/h bei < 15 Monate alt
CONTROL_PLANE_EXTENDED_RATE = 0.60  # USD/h bei > 14 Monate alt

# Fargate (https://aws.amazon.com/fargate/pricing/)
FARGATE_VCPU_RATE = 0.04048  # USD pro vCPU/h
FARGATE_RAM_RATE = 0.004445  # USD pro GB/h
FARGATE_DEFAULT_VCPU = 0.25  # Standardwert
FARGATE_DEFAULT_RAM_GB = 0.5  # Standardwert
FARGATE_DEFAULT_PODS = 2  # Annahme: 2 Pods

# EBS
AMAZON_EBS = 0.08  # USD/GB Monatlich (gp3)

# RDS-Storagepreise nach Typ
EBS_STORAGE_PRICING = {"gp2": 0.115, "gp3": 0.08, "io1": 0.125}

# ALB (https://aws.amazon.com/elasticloadbalancing/pricing/)
ALB_HOURLY_RATE = 0.0225  # USD/h für Betrieb
ALB_LCU_RATE = 0.008  # USD/LCU/h
ALB_ASSUMED_LCU = 1.0  # Annahme für typische Last

# Hinweis: Man kann theoretisch in einem fortgeschrittenen Szenario
# Metriken wie ActiveConnectionCount etc. über boto3 und CloudWatch
# abfragen und daraus LCU bestimmen. Aber das ist nicht mehr rein
# terraform-basiert, sondern eine Live-Auswertung.
