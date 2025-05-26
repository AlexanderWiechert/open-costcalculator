def build(volume_type="gp3", region="EU (Frankfurt)"):
    return [
        {"Type": "TERM_MATCH", "Field": "volumeType", "Value": volume_type},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region},
    ]
