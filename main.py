from battle.battle_state import BattleState
from battle.decision_engine import recommend_move
from pokemon import Pokemon

if __name__ == "__main__":
    # Option 1: Use the new Pokemon class with API data
    print("=== Using new Pokemon class ===")
    blaziken = Pokemon.from_api("blaziken", level=50, move_names=["flamethrower", "sky-uppercut", "earthquake", "slash"])
    sceptile = Pokemon.from_api("sceptile", level=50)
    
    print(f"My Pokemon: {blaziken}")
    print(f"Opponent: {sceptile}")
    print()
    
    # Convert to dictionary format for compatibility with existing battle system
    my_pokemon = blaziken.to_dict()
    opponent_pokemon = sceptile.to_dict()
    
    # Extract moves in the format expected by battle system
    my_moves = [
        {
            "name": move["name"],
            "type": move["type"],
            "power": move["power"] or 0,  # Handle None values
            "accuracy": move["accuracy"] or 100
        }
        for move in my_pokemon["moves"]
    ]
    
    # I do not yet know my opponent's moves and their power
    opponent_moves = []

    state = BattleState(my_pokemon, opponent_pokemon, my_moves, opponent_moves)
    best = recommend_move(state)
    print(f"Recommended move: {best}")
    
    print("\n=== Alternative: Using original format ===")
    # Option 2: Keep using your original format (still works)
    my_pokemon_simple = {"name": "Blaziken", "types": ["Fire", "Fighting"]}
    opponent_pokemon_simple = {"name": "Sceptile", "types": ["Grass"]}
    # I know my own moves and their power
    my_moves_simple = [
        {"name": "Flamethrower", "type": "Fire", "power": 90, "accuracy": 100},
        {"name": "Sky Uppercut", "type": "Fighting", "power": 85, "accuracy": 90},
        {"name": "Earthquake", "type": "Ground", "power": 100, "accuracy": 100},
        {"name": "Slash", "type": "Normal", "power": 70, "accuracy": 100}
    ]
    
    state_simple = BattleState(my_pokemon_simple, opponent_pokemon_simple, my_moves_simple, [])
    best_simple = recommend_move(state_simple)
    print(f"Recommended move (simple): {best_simple}")