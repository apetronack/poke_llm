from utils.type_effectiveness import get_multiplier

def recommend_move(state):
    best_score = -1
    best_move = None
    
    for move in state.my_moves:
        atk_type = move['type']
        power = move.get('power', 0)
        accuracy = move.get('accuracy', 100) / 100
        
        score = 0
        for def_type in state.opponent_pokemon['types']:
            multiplier = get_multiplier(atk_type, def_type)
            score += power * multiplier * accuracy
            if atk_type in state.my_pokemon['types']:
                score *= 1.5  # STAB

        if score > best_score:
            best_score = score
            best_move = move['name']

    return best_move