def detect_alb_from_controller(plan):
    return any(
        res.get("type") == "helm_release"
        and "aws-load-balancer-controller" in res.get("change", {}).get("after", {}).get("chart", "")
        for res in plan.get("resource_changes", [])
    )


def count_albs(plan):
    return sum(
        1
        for res in plan.get("resource_changes", [])
        if res.get("type") == "aws_lb"
        and res.get("change", {}).get("after", {}).get("load_balancer_type") == "application"
    )
