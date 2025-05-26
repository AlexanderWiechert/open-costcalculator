def extract(plan_json):
    for res in plan_json.get("resource_changes", []):
        if res.get("type") == "aws_eks_node_group":
            after = res.get("change", {}).get("after", {})
            instance_type = after.get("instance_types", [None])[0]
            capacity_type = after.get("capacity_type", "ON_DEMAND")
            scaling = after.get("scaling_config", [{}])
            desired_size = scaling.get("desired_size", 1)
            return instance_type, capacity_type, desired_size
    return None, None, 0
