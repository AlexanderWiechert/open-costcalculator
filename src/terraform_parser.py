import json

def load_tf_plan(filename):
    with open(filename, "r") as f:
        return json.load(f)

def extract_variables(plan):
    return {name: content.get("value") for name, content in plan.get("variables", {}).items()}

def extract_cost_info(plan):
    cost_info = []
    for resource in plan.get("resource_changes", []):
        if resource.get("type") == "aws_eks_node_group":
            change = resource.get("change", {})
            after = change.get("after", {})
            instance_types = after.get("instance_types", [])
            capacity_type = after.get("capacity_type")
            cluster_name = after.get("cluster_name")
            scaling_config = after.get("scaling_config", [])
            desired_size = None
            if scaling_config and isinstance(scaling_config, list) and scaling_config[0]:
                desired_size = scaling_config[0].get("desired_size")
            cost_info.append({
                "resource": resource.get("address"),
                "instance_types": instance_types,
                "capacity_type": capacity_type,
                "cluster_name": cluster_name,
                "desired_size": desired_size
            })
    return cost_info

def extract_lambda_info(plan):
    lambda_info = []
    resources = plan.get("planned_values", {}).get("root_module", {}).get("resources", [])
    for res in resources:
        if res.get("type") == "aws_lambda_function":
            values = res.get("values", {})
            lambda_info.append({
                "resource": res.get("address"),
                "function_name": values.get("function_name"),
                "runtime": values.get("runtime"),
                "memory_size": values.get("memory_size")
            })
    return lambda_info

def extract_apigw_info(plan):
    apigw_info = []
    resources = plan.get("planned_values", {}).get("root_module", {}).get("resources", [])
    for res in resources:
        if res.get("type") == "aws_api_gateway_rest_api":
            values = res.get("values", {})
            apigw_info.append({
                "resource": res.get("address"),
                "name": values.get("name"),
                "description": values.get("description")
            })
    return apigw_info
