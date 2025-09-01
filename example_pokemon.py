"""
Example usage of the Pokemon class
"""
from pokemon import Pokemon, Move

def main():
    print("=== Pokemon Class Demo ===\n")
    
    # Method 1: Create Pokemon from API (automatically fetches all data)
    print("1. Creating Blaziken from API:")
    blaziken = Pokemon.from_api("blaziken", level=50)
    print(blaziken)
    print(f"Base stats total: {blaziken.stats.total}")
    print(f"Actual HP at level 50: {blaziken.calculate_hp()}")
    print(f"Abilities: {[ability.name for ability in blaziken.abilities]}")
    print(f"Default moves: {[move.name for move in blaziken.moves]}")
    print()
    
    # Method 2: Create Pokemon with specific moves
    print("2. Creating Sceptile with specific moves:")
    sceptile_moves = ["leaf-blade", "earthquake", "dragon-claw", "aerial-ace"]
    sceptile = Pokemon.from_api("sceptile", level=50, move_names=sceptile_moves)
    print(sceptile)
    print(f"Custom moves: {[move.name for move in sceptile.moves]}")
    print()
    
    # Method 3 removed: Dictionary compatibility is no longer supported
    
    # Demonstrate battle mechanics
    print("4. Battle mechanics demo:")
    print(f"Blaziken takes 50 damage:")
    damage_taken = blaziken.take_damage(50)
    print(f"Damage taken: {damage_taken}, Current HP: {blaziken.current_hp}")
    
    print(f"Blaziken heals for 30:")
    healing_done = blaziken.heal(30)
    print(f"Healing done: {healing_done}, Current HP: {blaziken.current_hp}")
    print()
    
    # Demonstrate move details
    print("5. Move details:")
    if blaziken.moves:
        move = blaziken.moves[0]
        print(f"Move: {move.name}")
        print(f"Type: {move.type}")
        print(f"Power: {move.power}")
        print(f"Accuracy: {move.accuracy}")
        print(f"PP: {move.pp}")
        print(f"Damage Class: {move.damage_class}")
    print()
    
    # No dictionary conversion needed anymore
    
    # Show actual stats at current level
    print("7. Actual stats at current level:")
    actual_stats = blaziken.actual_stats
    for stat_name, value in actual_stats.items():
        print(f"  {stat_name.title()}: {value}")


if __name__ == "__main__":
    main()
