def extract_version(plan):
    for res in plan.get("resource_changes", []):
        if res.get("type") == "aws_eks_cluster":
            return res.get("change", {}).get("after", {}).get("version")
    return None
