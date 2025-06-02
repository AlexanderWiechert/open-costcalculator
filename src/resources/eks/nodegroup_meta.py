def extract(plan_json):
    for res in plan_json.get("resource_changes", []):
        if res.get("type") == "aws_eks_node_group":
            after = res.get("change", {}).get("after", {})
            instance_type = after.get("instance_types", [None])[0]
            capacity_type = after.get("capacity_type", "ON_DEMAND")

            scaling_raw = after.get("scaling_config", {})
            if isinstance(scaling_raw, list) and scaling_raw:
                scaling = scaling_raw[0]
            elif isinstance(scaling_raw, dict):
                scaling = scaling_raw
            else:
                scaling = {}

            desired_size = scaling.get("desired_size", 1)
            return instance_type, capacity_type, desired_size

    return None, None, 0
