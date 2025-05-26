def extract(plan):
    # Extract relevant info from the plan about nodegroups
    # ...

    for change in plan.get("resource_changes", []):
        if change.get("type") == "aws_eks_node_group":
            after = change.get("change", {}).get("after", {})
            # Old code:
            # scaling = after.get("scaling_config", [{}])[0]
            # New code:
            scaling = after.get("scaling_config", {})

            instance_type = after.get("instance_types", [None])[0]
            capacity_type = after.get("capacity_type")
            desired_size = scaling.get("desired_size", 0)

            return instance_type, capacity_type, desired_size

    return None, None, 0
