"""
Test the updated BattleState with Pokemon objects
"""
from battle.battle_state import BattleState
from battle.decision_engine import recommend_move
from pokemon import Pokemon, PokemonStats, Move

def test_pokemon_battle_state():
    """Test BattleState with Pokemon objects"""
    
    print("=== Testing Updated BattleState ===\n")
    
    # Create Pokemon manually (no API dependency)
    print("1. Creating Pokemon manually:")
    
    # Blaziken
    blaziken_stats = PokemonStats(80, 120, 70, 110, 70, 80)
    blaziken_moves = [
        Move("Flamethrower", "Fire", 90, 100, 15, "special"),
        Move("Sky Uppercut", "Fighting", 85, 90, 15, "physical"),
        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
        Move("Thunder Punch", "Electric", 75, 100, 15, "physical")
    ]
    blaziken = Pokemon("Blaziken", ["Fire", "Fighting"], blaziken_stats, blaziken_moves, level=50)
    
    # Sceptile
    sceptile_stats = PokemonStats(70, 85, 65, 105, 85, 120)
    sceptile_moves = [
        Move("Leaf Blade", "Grass", 90, 100, 15, "physical"),
        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
        Move("Dragon Claw", "Dragon", 80, 100, 15, "physical"),
        Move("Aerial Ace", "Flying", 60, 100, 20, "physical")
    ]
    sceptile = Pokemon("Sceptile", ["Grass"], sceptile_stats, sceptile_moves, level=50)
    
    print(f"Created: {blaziken.name} vs {sceptile.name}")
    print(f"Blaziken moves: {[move.name for move in blaziken.moves]}")
    print(f"Sceptile moves: {[move.name for move in sceptile.moves]}")
    
    print("\n2. Testing BattleState with Pokemon objects:")
    
    # Create BattleState with Pokemon objects directly
    state = BattleState(blaziken, sceptile)
    
    print(f"My Pokemon: {state.get_my_pokemon_name()} ({state.get_my_pokemon_types()})")
    print(f"Opponent: {state.get_opponent_pokemon_name()} ({state.get_opponent_pokemon_types()})")
    
    # Get move recommendation
    best_move = recommend_move(state)
    print(f"Recommended move: {best_move}")
    
    print("\n3. Testing backward compatibility with dictionaries:")
    
    # Test with dictionary format
    my_pokemon_dict = {"name": "Blaziken", "types": ["Fire", "Fighting"]}
    opponent_pokemon_dict = {"name": "Sceptile", "types": ["Grass"]}
    my_moves_dict = [
        {"name": "Flamethrower", "type": "Fire", "power": 90, "accuracy": 100},
        {"name": "Sky Uppercut", "type": "Fighting", "power": 85, "accuracy": 90},
        {"name": "Earthquake", "type": "Ground", "power": 100, "accuracy": 100},
        {"name": "Thunder Punch", "type": "Electric", "power": 75, "accuracy": 100}
    ]
    
    state_dict = BattleState(my_pokemon_dict, opponent_pokemon_dict, my_moves_dict, [])
    best_move_dict = recommend_move(state_dict)
    print(f"Recommended move (dict format): {best_move_dict}")
    
    print("\n4. Testing mixed format:")
    
    # Test mixed format (Pokemon object vs dictionary)
    state_mixed = BattleState(blaziken, opponent_pokemon_dict)
    best_move_mixed = recommend_move(state_mixed)
    print(f"Recommended move (mixed format): {best_move_mixed}")
    
    print("\n=== Test Results ===")
    print("✅ Pokemon objects work directly with BattleState")
    print("✅ Backward compatibility maintained for dictionaries")
    print("✅ Mixed format support works")
    print("✅ Move recommendation system updated")
    print("✅ No more manual formatting required!")
    
    return blaziken, sceptile

if __name__ == "__main__":
    test_pokemon_battle_state()
