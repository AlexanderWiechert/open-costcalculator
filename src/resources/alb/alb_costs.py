from resources.alb import alb_meta
from core import pricing_defaults

def calculate_alb_cost(plan, hours):
    alb_count = alb_meta.count_albs(plan)
    if alb_meta.detect_alb_from_controller(plan) or alb_count > 0:
        alb_cost = round((pricing_defaults.ALB_HOURLY_RATE +
                          pricing_defaults.ALB_LCU_RATE * pricing_defaults.ALB_ASSUMED_LCU) * hours, 5) * max(alb_count, 1)
        return [["ALB (geschätzt)", alb_count or 1, f"{pricing_defaults.ALB_ASSUMED_LCU} LCU", f"${alb_cost:.5f}"]], alb_cost
    return [], 0.0
