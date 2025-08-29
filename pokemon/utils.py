"""
Utility functions for working with Pokemon objects and battle systems
"""
from typing import Dict, List
from pokemon import Pokemon, Move


def pokemon_to_battle_format(pokemon: Pokemon) -> Dict:
    """
    Convert a Pokemon object to the format expected by the battle system
    """
    return {
        "name": pokemon.name,
        "types": pokemon.types
    }


def moves_to_battle_format(pokemon: Pokemon) -> List[Dict]:
    """
    Convert Pokemon moves to the format expected by the battle system
    """
    return [
        {
            "name": move.name,
            "type": move.type,
            "power": move.power or 0,  # Handle None values for status moves
            "accuracy": move.accuracy or 100  # Default accuracy if None
        }
        for move in pokemon.moves
    ]


def create_battle_ready_pokemon(pokemon_name: str, level: int = 50, 
                               move_names: List[str] = None) -> tuple:
    """
    Create a Pokemon and return it in battle-ready format
    
    Returns:
        tuple: (pokemon_dict, moves_list) ready for BattleState
    """
    pokemon = Pokemon.from_api(pokemon_name, level, move_names)
    pokemon_dict = pokemon_to_battle_format(pokemon)
    moves_list = moves_to_battle_format(pokemon)
    
    return pokemon_dict, moves_list


def display_pokemon_summary(pokemon: Pokemon) -> None:
    """
    Display a comprehensive summary of a Pokemon
    """
    print(f"=== {pokemon.name} (Level {pokemon.level}) ===")
    print(f"Type(s): {'/'.join(pokemon.types)}")
    print(f"HP: {pokemon.current_hp}/{pokemon.calculate_hp()}")
    
    if pokemon.abilities:
        abilities_str = ", ".join([
            f"{ability.name}{'*' if ability.is_hidden else ''}" 
            for ability in pokemon.abilities
        ])
        print(f"Abilities: {abilities_str}")
    
    print(f"Height: {pokemon.height}m, Weight: {pokemon.weight}kg")
    
    print("\nBase Stats:")
    stats = pokemon.stats
    print(f"  HP: {stats.hp}")
    print(f"  Attack: {stats.attack}")
    print(f"  Defense: {stats.defense}")
    print(f"  Sp. Attack: {stats.special_attack}")
    print(f"  Sp. Defense: {stats.special_defense}")
    print(f"  Speed: {stats.speed}")
    print(f"  Total: {stats.total}")
    
    if pokemon.moves:
        print("\nMoves:")
        for i, move in enumerate(pokemon.moves, 1):
            power_str = f" (Power: {move.power})" if move.power else " (Status)"
            accuracy_str = f" (Accuracy: {move.accuracy}%)" if move.accuracy else ""
            print(f"  {i}. {move.name} [{move.type}]{power_str}{accuracy_str}")
    
    print()


def compare_pokemon_stats(pokemon1: Pokemon, pokemon2: Pokemon) -> None:
    """
    Compare the base stats of two Pokemon
    """
    print(f"=== {pokemon1.name} vs {pokemon2.name} ===")
    stats1, stats2 = pokemon1.stats, pokemon2.stats
    
    comparisons = [
        ("HP", stats1.hp, stats2.hp),
        ("Attack", stats1.attack, stats2.attack),
        ("Defense", stats1.defense, stats2.defense),
        ("Sp. Attack", stats1.special_attack, stats2.special_attack),
        ("Sp. Defense", stats1.special_defense, stats2.special_defense),
        ("Speed", stats1.speed, stats2.speed),
        ("Total", stats1.total, stats2.total)
    ]
    
    for stat_name, val1, val2 in comparisons:
        if val1 > val2:
            winner = pokemon1.name
            diff = val1 - val2
        elif val2 > val1:
            winner = pokemon2.name
            diff = val2 - val1
        else:
            winner = "Tie"
            diff = 0
        
        if winner == "Tie":
            print(f"{stat_name}: {val1} (Tie)")
        else:
            print(f"{stat_name}: {winner} wins ({diff} point difference)")
    
    print()
