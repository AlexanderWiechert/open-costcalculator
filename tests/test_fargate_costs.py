from core import duration_meta
from resources.eks import fargate_costs


def test_fargate_cost_computation():
    hours = duration_meta.HOURS_PER_MONTH
    cost = fargate_costs.calculate_fargate_cost(hours)
    assert cost > 0
