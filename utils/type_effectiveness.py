import json

with open('data/type_chart.json') as f:
    TYPE_CHART = json.load(f)

def get_multiplier(attacking_type, defending_type):
    # Returns the type effectiveness multiplier for an attacking type against a defending type.
    return TYPE_CHART.get(attacking_type, {}).get(defending_type, 1.0)