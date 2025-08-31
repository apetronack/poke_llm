from utils.type_effectiveness import get_multiplier
from pokemon import Pokemon, Move

def recommend_move(state):
    """
    Recommend the best move based on type effectiveness and power.
    Works with both Pokemon objects and dictionary format for backward compatibility.
    """
    best_score = -1
    best_move = None
    
    # Get moves based on whether we're using Pokemon objects or dictionaries
    moves_to_evaluate = []
    if hasattr(state, 'my_moves') and state.my_moves:
        if isinstance(state.my_moves[0], Move):
            # Working with Pokemon Move objects
            moves_to_evaluate = [
                {
                    'name': move.name,
                    'type': move.type,
                    'power': move.power or 0,
                    'accuracy': move.accuracy or 100
                }
                for move in state.my_moves
            ]
        else:
            # Working with dictionary format
            moves_to_evaluate = state.my_moves
    
    # Get Pokemon types
    my_types = state.get_my_pokemon_types()
    opponent_types = state.get_opponent_pokemon_types()
    
    for move in moves_to_evaluate:
        atk_type = move['type']
        power = move.get('power', 0)
        accuracy = move.get('accuracy', 100) / 100
        
        score = 0
        for def_type in opponent_types:
            multiplier = get_multiplier(atk_type, def_type)
            score += power * multiplier * accuracy
            # STAB (Same Type Attack Bonus)
            if atk_type in my_types:
                score *= 1.5

        if score > best_score:
            best_score = score
            best_move = move['name']

    return best_move