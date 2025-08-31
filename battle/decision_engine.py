from utils.type_effectiveness import get_multiplier
from utils.damage_calculator import calculate_physical_damage, calculate_special_damage
from pokemon import Pokemon, Move

def recommend_move(state):
    """
    Recommend the best move based on actual damage calculations.
    Works with both Pokemon objects and dictionary format for backward compatibility.
    """
    best_damage = -1
    best_move = None
    
    # Check if we're working with Pokemon objects (preferred) or dictionaries
    if isinstance(state.my_pokemon, Pokemon) and isinstance(state.opponent_pokemon, Pokemon):
        # Use advanced damage calculation with Pokemon objects
        return _recommend_move_with_damage_calc(state)
    else:
        # Fall back to simple scoring for dictionary format
        return _recommend_move_legacy(state)


def _recommend_move_with_damage_calc(state):
    """
    Advanced move recommendation using actual damage calculations.
    Requires Pokemon objects in the battle state.
    """
    best_damage = -1
    best_move = None
    
    my_pokemon = state.my_pokemon
    opponent_pokemon = state.opponent_pokemon
    
    for move in my_pokemon.moves:
        # Skip status moves (they don't deal damage)
        if move.power is None or move.power == 0:
            continue
            
        try:
            # Calculate damage based on move type
            if move.damage_class.lower() == 'physical':
                damage = calculate_physical_damage(my_pokemon, opponent_pokemon, move)
            elif move.damage_class.lower() == 'special':
                damage = calculate_special_damage(my_pokemon, opponent_pokemon, move)
            else:
                # Status moves - assign low score but don't ignore completely
                damage = 0
            
            # Apply accuracy modifier
            accuracy_factor = (move.accuracy or 100) / 100
            expected_damage = damage * accuracy_factor
            
            # Debugging
            print(f"Expected damage for {move.name}: {expected_damage}")
            if expected_damage > best_damage:
                best_damage = expected_damage
                best_move = move.name
                
        except Exception as e:
            print(f"Error calculating damage for {move.name}: {e}")
            # Fall back to simple calculation for this move
            continue
    
    return best_move


def _recommend_move_legacy(state):
    """
    Legacy move recommendation for backward compatibility with dictionary format.
    Uses simple scoring based on type effectiveness and power.
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


def calculate_move_damage(attacker, defender, move):
    """
    Calculate the damage a specific move would deal.
    Returns 0 for status moves or if calculation fails.
    """
    if not isinstance(attacker, Pokemon) or not isinstance(defender, Pokemon):
        raise ValueError("Both attacker and defender must be Pokemon objects")
    
    if move.power is None or move.power == 0:
        return 0
    
    try:
        if move.damage_class.lower() == 'physical':
            return calculate_physical_damage(attacker, defender, move)
        elif move.damage_class.lower() == 'special':
            return calculate_special_damage(attacker, defender, move)
        else:
            return 0
    except Exception as e:
        print(f"Error calculating damage for {move.name}: {e}")
        return 0


def get_move_damage_range(attacker, defender, move):
    """
    Calculate the minimum and maximum damage a move can deal.
    Returns (min_damage, max_damage) tuple.
    """
    if not isinstance(attacker, Pokemon) or not isinstance(defender, Pokemon):
        raise ValueError("Both attacker and defender must be Pokemon objects")
    
    if move.power is None or move.power == 0:
        return (0, 0)
    
    try:
        if move.damage_class.lower() == 'physical':
            min_damage = calculate_physical_damage(attacker, defender, move, random_multiplier=0.85)
            max_damage = calculate_physical_damage(attacker, defender, move, random_multiplier=1.0)
        elif move.damage_class.lower() == 'special':
            min_damage = calculate_special_damage(attacker, defender, move, random_multiplier=0.85)
            max_damage = calculate_special_damage(attacker, defender, move, random_multiplier=1.0)
        else:
            return (0, 0)
        
        return (min_damage, max_damage)
    except Exception as e:
        print(f"Error calculating damage range for {move.name}: {e}")
        return (0, 0)


def get_all_move_analysis(state):
    """
    Get detailed analysis of all available moves including damage calculations.
    Returns a list of dictionaries with move analysis.
    """
    if not isinstance(state.my_pokemon, Pokemon) or not isinstance(state.opponent_pokemon, Pokemon):
        raise ValueError("Both Pokemon must be Pokemon objects for detailed analysis")
    
    analysis = []
    my_pokemon = state.my_pokemon
    opponent_pokemon = state.opponent_pokemon
    
    for move in my_pokemon.moves:
        move_info = {
            'name': move.name,
            'type': move.type,
            'power': move.power,
            'accuracy': move.accuracy,
            'damage_class': move.damage_class,
            'pp': move.pp
        }
        
        if move.power and move.power > 0:
            # Calculate damage
            avg_damage = calculate_move_damage(my_pokemon, opponent_pokemon, move)
            min_damage, max_damage = get_move_damage_range(my_pokemon, opponent_pokemon, move)
            
            # Apply accuracy
            accuracy_factor = (move.accuracy or 100) / 100
            expected_damage = avg_damage * accuracy_factor
            
            move_info.update({
                'min_damage': min_damage,
                'max_damage': max_damage,
                'average_damage': avg_damage,
                'expected_damage': expected_damage,
                'can_ko': max_damage >= opponent_pokemon.current_hp,
                'guaranteed_ko': min_damage >= opponent_pokemon.current_hp,
                'damage_percent': (avg_damage / opponent_pokemon.current_hp) * 100 if opponent_pokemon.current_hp > 0 else 0
            })
        else:
            # Status move
            move_info.update({
                'min_damage': 0,
                'max_damage': 0,
                'average_damage': 0,
                'expected_damage': 0,
                'can_ko': False,
                'guaranteed_ko': False,
                'damage_percent': 0,
                'is_status_move': True
            })
        
        analysis.append(move_info)
    
    # Sort by expected damage (highest first)
    analysis.sort(key=lambda x: x['expected_damage'], reverse=True)
    return analysis


def recommend_move_with_analysis(state):
    """
    Recommend the best move and return detailed analysis.
    Returns tuple of (best_move_name, full_analysis_list)
    """
    try:
        analysis = get_all_move_analysis(state)
        best_move = analysis[0]['name'] if analysis else None
        return best_move, analysis
    except Exception as e:
        print(f"Error in detailed analysis: {e}")
        # Fall back to simple recommendation
        best_move = recommend_move(state)
        return best_move, []