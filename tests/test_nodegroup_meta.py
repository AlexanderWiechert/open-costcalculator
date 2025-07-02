from resources.eks import nodegroup_meta


def test_extract_nodegroup_data():
    sample_plan = {
        "resource_changes": [
            {
                "type": "aws_eks_node_group",
                "change": {
                    "after": {
                        "instance_types": ["t3.medium"],
                        "scaling_config": {"desired_size": 2},
                        "capacity_type": "ON_DEMAND",
                    }
                },
            }
        ]
    }
    instance_type, capacity_type, desired_size = nodegroup_meta.extract(sample_plan)
    assert instance_type == "t3.medium"
    assert capacity_type == "ON_DEMAND"
    assert desired_size == 2
