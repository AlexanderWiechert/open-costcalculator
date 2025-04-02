# Zentrale Preisdefinitionen für AWS-Services (OnDemand)
CONTROL_PLANE_STANDARD_RATE = 0.10      # bis 14 Monate nach Release
CONTROL_PLANE_EXTENDED_RATE = 0.60      # 15–26 Monate nach Release

# EBS Preis pro GB/Monat
AMAZON_EBS = 0.08  # entspricht $0.08 pro GB/Monat (gp3)

FARGATE_VCPU_RATE = 0.04048             # pro vCPU-Stunde
FARGATE_RAM_RATE = 0.004445             # pro GB-RAM-Stunde
FARGATE_DEFAULT_VCPU = 0.25             # Default pro Pod
FARGATE_DEFAULT_RAM_GB = 0.5            # Default pro Pod
FARGATE_DEFAULT_PODS = 2                # geschätzte Anzahl pro Cluster
