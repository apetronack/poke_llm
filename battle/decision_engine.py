from utils.type_effectiveness import get_multiplier
from utils.damage_calculator import calculate_physical_damage, calculate_special_damage
from pokemon import Pokemon, Move
from battle.battle_state import WeatherType

def recommend_move(state):
    """
    Recommend the best move based on actual damage calculations and battle state.
    Enhanced to consider weather, screens, and opponent move history.
    """
    return _recommend_move_with_enhanced_analysis(state)


def _recommend_move_with_enhanced_analysis(state):
    """
    Enhanced move recommendation using battle state information.
    Considers weather effects, screens, and opponent patterns.
    """
    best_score = -1
    best_move = None
    
    my_pokemon = state.my_pokemon
    opponent_pokemon = state.opponent_pokemon
    
    # Get opponent move patterns for strategic considerations
    opponent_patterns = state.get_opponent_move_pattern()
    
    for move in my_pokemon.moves:
        score = _calculate_move_score(state, move, opponent_patterns)
        
        print(f"Move score for {move.name}: {score}")
        if score > best_score:
            best_score = score
            best_move = move.name
    
    return best_move


def _calculate_move_score(state, move, opponent_patterns):
    """Calculate a comprehensive score for a move considering all battle factors"""
    base_score = 0
    
    my_pokemon = state.my_pokemon
    opponent_pokemon = state.opponent_pokemon
    
    # Base damage calculation
    if move.power and move.power > 0:
        try:
            if move.damage_class.lower() == 'physical':
                damage = calculate_physical_damage(my_pokemon, opponent_pokemon, move)
            elif move.damage_class.lower() == 'special':
                damage = calculate_special_damage(my_pokemon, opponent_pokemon, move)
            else:
                damage = 0
            
            # Apply accuracy
            accuracy_factor = (move.accuracy or 100) / 100
            base_score = damage * accuracy_factor
            
        except Exception as e:
            print(f"Error calculating damage for {move.name}: {e}")
            base_score = 0
    
    # Weather bonuses/penalties
    weather_modifier = _get_weather_modifier(state, move)
    base_score *= weather_modifier
    
    # Screen effects
    screen_modifier = _get_screen_modifier(state, move)
    base_score *= screen_modifier
    
    # Strategic considerations based on opponent patterns
    strategic_bonus = _get_strategic_bonus(state, move, opponent_patterns)
    base_score += strategic_bonus
    
    # Priority considerations
    if hasattr(move, 'priority') and move.priority > 0:
        base_score += 10  # Small bonus for priority moves
    
    return base_score


def _get_weather_modifier(state, move):
    """Get weather-based damage modifier"""
    if not state.weather:
        return 1.0
    
    weather = state.weather.weather_type
    move_type = move.type.lower()
    
    # Weather boosts
    if weather == WeatherType.SUN:
        if move_type == 'fire':
            return 1.5
        elif move_type == 'water':
            return 0.5
    elif weather == WeatherType.RAIN:
        if move_type == 'water':
            return 1.5
        elif move_type == 'fire':
            return 0.5
    elif weather == WeatherType.SANDSTORM:
        if move_type in ['rock', 'ground', 'steel']:
            return 1.2
    
    return 1.0


def _get_screen_modifier(state, move):
    """Get screen effect modifier for damage"""
    if not move.power or move.power == 0:
        return 1.0
    
    # Check if opponent has screens that would reduce our damage
    opponent_screens = state.get_active_screens("opponent")
    
    for screen in opponent_screens:
        if screen.effect_name == "Light Screen" and move.damage_class.lower() == 'special':
            return 0.5
        elif screen.effect_name == "Reflect" and move.damage_class.lower() == 'physical':
            return 0.5
    
    return 1.0


def _get_strategic_bonus(state, move, opponent_patterns):
    """Get strategic bonus based on battle history and patterns"""
    bonus = 0
    
    # If opponent frequently uses a specific move type, prioritize counters
    if opponent_patterns['recent_moves']:
        recent_move_types = _get_move_types_from_names(opponent_patterns['recent_moves'])
        if _move_is_effective_against_types(move, recent_move_types):
            bonus += 20
    
    # Bonus for moves that can KO
    if hasattr(state.opponent_pokemon, 'current_hp'):
        try:
            if move.damage_class.lower() == 'physical':
                potential_damage = calculate_physical_damage(state.my_pokemon, state.opponent_pokemon, move)
            elif move.damage_class.lower() == 'special':
                potential_damage = calculate_special_damage(state.my_pokemon, state.opponent_pokemon, move)
            else:
                potential_damage = 0
            
            if potential_damage >= state.opponent_pokemon.current_hp:
                bonus += 50  # Big bonus for potential KO
            elif potential_damage >= state.opponent_pokemon.current_hp * 0.8:
                bonus += 25  # Bonus for bringing close to KO
        except:
            pass
    
    # Penalty for moves the opponent might expect (overused moves)
    if hasattr(state, 'current_ally_history'):
        ally_moves = [move_name for move_name, _ in state.current_ally_history.moves_used]
        move_usage_count = ally_moves.count(move.name)
        if move_usage_count > 2:
            bonus -= 10  # Small penalty for predictability
    
    return bonus


def _get_move_types_from_names(move_names):
    """Helper to get move types from move names (simplified)"""
    # This would typically require a move database lookup
    # For now, return common types based on move names
    type_mapping = {
        'flamethrower': 'fire',
        'hydro pump': 'water',
        'thunderbolt': 'electric',
        'earthquake': 'ground',
        'ice beam': 'ice',
        'leaf blade': 'grass',
        'dragon claw': 'dragon'
    }
    
    return [type_mapping.get(move.lower(), 'normal') for move in move_names]


def _move_is_effective_against_types(move, target_types):
    """Check if move is super effective against target types"""
    # Simplified effectiveness check
    effective_matchups = {
        'water': ['fire', 'ground', 'rock'],
        'fire': ['grass', 'ice', 'bug', 'steel'],
        'grass': ['water', 'ground', 'rock'],
        'electric': ['water', 'flying'],
        'ice': ['grass', 'ground', 'flying', 'dragon'],
        'fighting': ['normal', 'rock', 'steel', 'ice', 'dark'],
        'ground': ['fire', 'electric', 'poison', 'rock', 'steel']
    }
    
    move_type = move.type.lower()
    if move_type in effective_matchups:
        return any(target_type in effective_matchups[move_type] for target_type in target_types)
    
    return False




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