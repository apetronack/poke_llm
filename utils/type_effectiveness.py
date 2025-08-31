import json

with open('data/type_chart.json') as f:
    TYPE_CHART = json.load(f)

def get_multiplier(attacking_type, defending_types):
    product = 1.0
    for def_type in defending_types:
        product *= TYPE_CHART.get(attacking_type, {}).get(def_type, 1.0)
    return product
