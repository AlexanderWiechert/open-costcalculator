# filter/fargate_costs.py

from . import pricing_defaults

def calculate_fargate_cost(hours):
    """
    Berechnet die geschätzten monatlichen Kosten für Fargate auf Basis
    eines Standard-Setups mit 2 Pods à 0.25 vCPU und 0.5 GB RAM.
    """
    cpu_cost = pricing_defaults.FARGATE_VCPU_RATE * pricing_defaults.FARGATE_DEFAULT_VCPU
    ram_cost = pricing_defaults.FARGATE_RAM_RATE * pricing_defaults.FARGATE_DEFAULT_RAM_GB
    total_per_pod = (cpu_cost + ram_cost) * hours
    return round(total_per_pod * pricing_defaults.FARGATE_DEFAULT_PODS, 5)
