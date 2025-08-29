"""
Test the Pokemon class with manual data (without API)
"""
from pokemon import Pokemon, Move, Ability, PokemonStats

def test_manual_pokemon():
    """Test creating a Pokemon manually without API calls"""
    
    # Create stats
    stats = PokemonStats(
        hp=78,
        attack=84,
        defense=78,
        special_attack=109,
        special_defense=85,
        speed=100
    )
    
    # Create moves
    moves = [
        Move(name="Flamethrower", type="Fire", power=90, accuracy=100, pp=15, damage_class="special"),
        Move(name="Sky Uppercut", type="Fighting", power=85, accuracy=90, pp=15, damage_class="physical"),
        Move(name="Earthquake", type="Ground", power=100, accuracy=100, pp=10, damage_class="physical"),
        Move(name="Slash", type="Normal", power=70, accuracy=100, pp=20, damage_class="physical")
    ]
    
    # Create abilities
    abilities = [
        Ability(name="Blaze", effect="Powers up Fire-type moves when HP is low"),
        Ability(name="Speed Boost", effect="Gradually boosts Speed", is_hidden=True)
    ]
    
    # Create Pokemon
    blaziken = Pokemon(
        name="Blaziken",
        types=["Fire", "Fighting"],
        stats=stats,
        moves=moves,
        abilities=abilities,
        level=50,
        height=1.9,
        weight=52.0
    )
    
    print("=== Manual Pokemon Creation Test ===")
    print(blaziken)
    print(f"\nBase Stats Total: {blaziken.stats.total}")
    print(f"Actual HP at level 50: {blaziken.calculate_hp()}")
    print(f"Current HP: {blaziken.current_hp}")
    
    print(f"\nAbilities:")
    for ability in blaziken.abilities:
        hidden_mark = " (Hidden)" if ability.is_hidden else ""
        print(f"  - {ability.name}{hidden_mark}: {ability.effect}")
    
    print(f"\nMoves:")
    for move in blaziken.moves:
        print(f"  - {move.name} ({move.type}) - Power: {move.power}, Accuracy: {move.accuracy}%")
    
    print(f"\nActual stats at level {blaziken.level}:")
    actual_stats = blaziken.actual_stats
    for stat_name, value in actual_stats.items():
        print(f"  {stat_name.title()}: {value}")
    
    # Test battle mechanics
    print(f"\n=== Battle Mechanics Test ===")
    print(f"Taking 30 damage...")
    damage_taken = blaziken.take_damage(30)
    print(f"Damage taken: {damage_taken}, Current HP: {blaziken.current_hp}")
    
    print(f"Healing for 20...")
    healing_done = blaziken.heal(20)
    print(f"Healing done: {healing_done}, Current HP: {blaziken.current_hp}")
    
    # Test conversion to dict
    print(f"\n=== Conversion to Dictionary ===")
    pokemon_dict = blaziken.to_dict()
    print(f"As dictionary: {pokemon_dict['name']} - {pokemon_dict['types']}")
    
    return blaziken

if __name__ == "__main__":
    blaziken = test_manual_pokemon()
