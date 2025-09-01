"""
Comprehensive demonstration of the Pokemon class
Shows both manual creation and API integration
"""

def manual_pokemon_demo():
    """Demonstrate Pokemon creation without API"""
    from pokemon import Pokemon, Move, Ability, PokemonStats
    
    print("=== POKEMON CLASS DEMONSTRATION ===\n")
    print("1. Creating Pokemon manually (no API required):")
    
    # Create stats for Blaziken
    blaziken_stats = PokemonStats(
        hp=80, attack=120, defense=70, 
        special_attack=110, special_defense=70, speed=80
    )
    
    # Create moves
    blaziken_moves = [
        Move(name="Flamethrower", type="Fire", power=90, accuracy=100, pp=15, damage_class="special"),
        Move(name="Sky Uppercut", type="Fighting", power=85, accuracy=90, pp=15, damage_class="physical"),
        Move(name="Earthquake", type="Ground", power=100, accuracy=100, pp=10, damage_class="physical"),
        Move(name="Thunder Punch", type="Electric", power=75, accuracy=100, pp=15, damage_class="physical")
    ]
    
    # Create abilities
    blaziken_abilities = [
        Ability(name="Blaze", effect="Powers up Fire-type moves when HP is low"),
        Ability(name="Speed Boost", effect="Speed stat is gradually boosted", is_hidden=True)
    ]
    
    # Create the Pokemon
    blaziken = Pokemon(
        name="Blaziken",
        types=["Fire", "Fighting"],
        stats=blaziken_stats,
        moves=blaziken_moves,
        abilities=blaziken_abilities,
        level=50,
        height=1.9,
        weight=52.0
    )
    
    print(f"Created: {blaziken}")
    print(f"Types: {'/'.join(blaziken.types)}")
    print(f"Base stat total: {blaziken.stats.total}")
    print(f"Actual HP at level 50: {blaziken.calculate_hp()}")
    print(f"Current HP: {blaziken.current_hp}")
    
    print("\nAbilities:")
    for ability in blaziken.abilities:
        hidden_str = " (Hidden Ability)" if ability.is_hidden else ""
        print(f"  • {ability.name}{hidden_str}")
        if ability.effect:
            print(f"    Effect: {ability.effect}")
    
    print("\nMoveset:")
    for i, move in enumerate(blaziken.moves, 1):
        power_str = f"Power: {move.power}" if move.power else "Status move"
        print(f"  {i}. {move.name} ({move.type}) - {power_str}, Accuracy: {move.accuracy}%")
    
    return blaziken


def api_pokemon_demo():
    """Demonstrate Pokemon creation with API (requires pokebase)"""
    try:
        from pokemon import Pokemon
        
        print("\n2. Creating Pokemon from PokeAPI:")
        
        # This will fetch real data from the Pokemon API
        charizard = Pokemon.from_api("charizard", level=50)
        print(f"Created from API: {charizard}")
        print(f"Real stats: HP={charizard.stats.hp}, Attack={charizard.stats.attack}")
        print(f"Height: {charizard.height}m, Weight: {charizard.weight}kg")
        
        if charizard.moves:
            print(f"Sample moves: {[move.name for move in charizard.moves[:3]]}")
        
        return charizard
    
    except ImportError as e:
        print(f"\nAPI demo skipped - pokebase not available: {e}")
        return None
    except Exception as e:
        print(f"\nAPI demo failed: {e}")
        return None


def battle_integration_demo(pokemon1, pokemon2=None):
    """Show how Pokemon integrates with the battle system"""
    print("\n3. Battle System Integration:")
    # Create a simple opponent if not provided
    if pokemon2 is None:
        from pokemon import Pokemon, PokemonStats
        opponent_stats = PokemonStats(75, 75, 75, 75, 75, 75)
        pokemon2 = Pokemon(
            name="Sceptile", 
            types=["Grass"], 
            stats=opponent_stats, 
            level=50
        )
    print(f"\nSimulating battle scenario:")
    print(f"  {pokemon1.name} vs {pokemon2.name}")
    print(f"  {pokemon1.name} types: {pokemon1.types}")
    print(f"  {pokemon2.name} types: {pokemon2.types}")


def pokemon_comparison_demo(pokemon1, pokemon2):
    """Compare two Pokemon"""
    from pokemon import compare_pokemon_stats
    
    print("\n4. Pokemon Comparison:")
    compare_pokemon_stats(pokemon1, pokemon2)


def battle_mechanics_demo(pokemon):
    """Demonstrate battle mechanics"""
    print("\n5. Battle Mechanics:")
    
    original_hp = pokemon.current_hp
    print(f"Starting HP: {pokemon.current_hp}")
    
    # Take damage
    damage = 45
    actual_damage = pokemon.take_damage(damage)
    print(f"Took {actual_damage} damage, HP now: {pokemon.current_hp}")
    
    # Heal
    heal_amount = 25
    actual_healing = pokemon.heal(heal_amount)
    print(f"Healed {actual_healing} HP, HP now: {pokemon.current_hp}")
    
    # Check status
    if pokemon.is_fainted():
        print("Pokemon has fainted!")
    else:
        print("Pokemon is still able to battle!")


def main():
    """Run all demonstrations"""
    
    # Manual creation (always works)
    blaziken = manual_pokemon_demo()
    
    # API creation (requires pokebase)
    charizard = api_pokemon_demo()
    
    # Use charizard if available, otherwise create a simple opponent
    opponent = charizard if charizard else None
    
    # Battle integration
    battle_integration_demo(blaziken, opponent)
    
    # Pokemon comparison
    if opponent:
        pokemon_comparison_demo(blaziken, opponent)
    
    # Battle mechanics
    battle_mechanics_demo(blaziken)
    
    print("\n=== SUMMARY ===")
    print("✅ Pokemon class with comprehensive attributes")
    print("✅ Manual creation with custom stats/moves/abilities")
    print("✅ API integration with PokeAPI (when available)")
    print("✅ Battle system compatibility")
    print("✅ Battle mechanics (damage, healing, status)")
    print("✅ Utility functions for comparison and conversion")
    print("\nYour Pokemon objects include:")
    print("• Name, types, level, stats (base and calculated)")
    print("• Moves with power, accuracy, type, and damage class")
    print("• Abilities (including hidden abilities)")
    print("• Physical characteristics (height, weight)")
    print("• Battle state (current HP, status conditions)")
    print("• Compatibility with your existing battle system")


if __name__ == "__main__":
    main()
