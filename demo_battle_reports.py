"""
Demo of the battle report and analysis utilities
"""
from battle.battle_state import BattleState, WeatherType
from battle.battle_utils import create_battle_report, get_battle_recommendations, BattleStateAnalyzer
from battle.decision_engine import recommend_move
from pokemon import Pokemon, PokemonStats, Move

def demo_battle_reports():
    """Demo the battle report and analysis system"""
    
    print("=== Battle Report System Demo ===\n")
    
    # Create Pokemon for a realistic battle scenario
    
    # Blaziken (Fire/Fighting) - Our Pokemon
    blaziken_stats = PokemonStats(80, 120, 70, 110, 70, 80)
    blaziken_moves = [
        Move("Flamethrower", "Fire", 90, 100, 15, "special"),
        Move("Close Combat", "Fighting", 120, 100, 5, "physical"),
        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
        Move("Protect", "Normal", 0, 100, 10, "status")
    ]
    blaziken = Pokemon("Blaziken", ["Fire", "Fighting"], blaziken_stats, blaziken_moves, level=50)
    blaziken.current_hp = 130  # Slightly damaged
    
    # Swampert (Water/Ground) - Opponent
    swampert_stats = PokemonStats(100, 110, 90, 85, 90, 60)
    swampert_moves = [
        Move("Surf", "Water", 90, 100, 15, "special"),
        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
        Move("Ice Beam", "Ice", 90, 100, 10, "special"),
        Move("Stealth Rock", "Rock", 0, 100, 20, "status")
    ]
    swampert = Pokemon("Swampert", ["Water", "Ground"], swampert_stats, swampert_moves, level=50)
    swampert.current_hp = 180  # Nearly full health
    
    # Initialize battle
    battle = BattleState(blaziken, swampert)
    
    print("1. Initial Battle Report:")
    print(create_battle_report(battle))
    
    print("\n2. Initial Recommendations:")
    recommendations = get_battle_recommendations(battle)
    for rec in recommendations['recommendations']:
        print(f"  • {rec}")
    print(f"  Priority: {recommendations['priority']}")
    
    # Simulate some battle progression
    print("\n" + "="*60)
    print("SIMULATING BATTLE PROGRESSION")
    print("="*60)
    
    # Turn 1: Set up sunny weather and use moves
    battle.set_weather(WeatherType.SUN, 5)
    battle.advance_turn()
    battle.record_move_used("ally", "Flamethrower")
    battle.record_move_used("opponent", "Surf")
    battle.record_damage("ally", 95)  # Blaziken takes water damage
    battle.record_damage("opponent", 85)  # Swampert takes fire damage (boosted by sun)
    
    # Turn 2: More moves
    battle.advance_turn()
    battle.record_move_used("ally", "Close Combat")
    battle.record_move_used("opponent", "Earthquake")
    battle.record_damage("ally", 110)  # Blaziken weak to ground
    battle.record_damage("opponent", 90)
    
    # Turn 3: Opponent sets up
    battle.advance_turn()
    battle.record_move_used("ally", "Earthquake")
    battle.record_move_used("opponent", "Stealth Rock")
    battle.record_damage("opponent", 100)
    
    # Turn 4: Both Pokemon getting low
    battle.advance_turn()
    battle.record_move_used("ally", "Flamethrower")
    battle.record_move_used("opponent", "Ice Beam")
    battle.record_damage("ally", 85)
    battle.record_damage("opponent", 80)
    
    # Update HP to reflect damage
    blaziken.current_hp = 25  # Very low
    swampert.current_hp = 60   # Also getting low
    
    print("\n3. Mid-Battle Report:")
    print(create_battle_report(battle))
    
    print("\n4. Updated Recommendations:")
    recommendations = get_battle_recommendations(battle)
    for rec in recommendations['recommendations']:
        print(f"  • {rec}")
    print(f"  Priority: {recommendations['priority']}")
    
    # Detailed analysis
    print("\n5. Detailed Analysis:")
    analyzer = BattleStateAnalyzer(battle)
    
    momentum = analyzer.get_momentum_analysis()
    print(f"  Recent momentum:")
    print(f"    Your recent moves: {momentum['recent_ally_moves']}")
    print(f"    Opponent recent moves: {momentum['recent_opponent_moves']}")
    
    prediction = analyzer.predict_opponent_next_move()
    print(f"  Opponent prediction:")
    print(f"    Predicted move: {prediction['prediction']}")
    print(f"    Confidence: {prediction['confidence']:.1f}%")
    print(f"    Reasoning: {prediction['reasoning']}")
    
    phase = analyzer.get_battle_phase_analysis()
    print(f"  Battle phase analysis:")
    print(f"    Phase: {phase['phase']}")
    print(f"    Strategy: {phase['recommended_strategy']}")
    print(f"    Your HP: {phase['ally_hp_percent']:.1f}%")
    print(f"    Opponent HP: {phase['opponent_hp_percent']:.1f}%")
    
    # Get move recommendation with context
    print("\n6. Move Recommendation with Context:")
    best_move = recommend_move(battle)
    print(f"  Recommended move: {best_move}")
    print(f"  Reasoning: Based on current HP, weather, and opponent patterns")
    
    print("\n=== Battle Report Demo Complete ===")

def demo_team_battle_reports():
    """Demo battle reports with team switching"""
    
    print("\n=== Team Battle Report Demo ===\n")
    
    # Create a team scenario
    print("Setting up a 3v3 team battle scenario...")
    
    # Team Pokemon
    charizard = Pokemon("Charizard", ["Fire", "Flying"], 
                       PokemonStats(78, 84, 78, 109, 85, 100),
                       [Move("Fire Blast", "Fire", 110, 85, 5, "special"),
                        Move("Air Slash", "Flying", 75, 95, 15, "special")], level=50)
    
    venusaur = Pokemon("Venusaur", ["Grass", "Poison"],
                      PokemonStats(80, 82, 83, 100, 100, 80),
                      [Move("Petal Blizzard", "Grass", 90, 100, 15, "physical"),
                       Move("Sludge Bomb", "Poison", 90, 100, 10, "special")], level=50)
    
    blastoise = Pokemon("Blastoise", ["Water"],
                       PokemonStats(79, 83, 100, 85, 105, 78),
                       [Move("Hydro Pump", "Water", 110, 80, 5, "special"),
                        Move("Ice Beam", "Ice", 90, 100, 10, "special")], level=50)
    
    # Opponent
    tyranitar = Pokemon("Tyranitar", ["Rock", "Dark"],
                       PokemonStats(100, 134, 110, 95, 100, 61),
                       [Move("Stone Edge", "Rock", 100, 80, 5, "physical"),
                        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
                        Move("Crunch", "Dark", 80, 100, 15, "physical"),
                        Move("Ice Punch", "Ice", 75, 100, 15, "physical")], level=50)
    
    # Start with Charizard
    battle = BattleState(charizard, tyranitar)
    
    print("Initial team composition:")
    print(f"  Lead: {charizard.name}")
    print(f"  Team: {venusaur.name}, {blastoise.name}")
    print(f"  vs {tyranitar.name}")
    
    # Simulate team battle
    battle.set_weather(WeatherType.SANDSTORM, 8)
    
    # Charizard takes some damage
    for turn in range(3):
        battle.advance_turn()
        battle.record_move_used("ally", "Fire Blast")
        battle.record_move_used("opponent", "Stone Edge")
        battle.record_damage("ally", 80)
        battle.record_damage("opponent", 65)
    
    charizard.current_hp = 50  # Low HP
    
    print(f"\n{charizard.name} Report after 3 turns:")
    print(create_battle_report(battle))
    
    # Switch to Venusaur
    print(f"\nSwitching to {venusaur.name}...")
    battle.switch_pokemon(venusaur, "ally")
    
    # Continue battle
    for turn in range(2):
        battle.advance_turn()
        battle.record_move_used("ally", "Petal Blizzard")
        battle.record_move_used("opponent", "Ice Punch")
        battle.record_damage("ally", 90)
        battle.record_damage("opponent", 85)
    
    venusaur.current_hp = 70  # Also getting low
    
    print(f"\n{venusaur.name} Report:")
    print(create_battle_report(battle))
    
    # Final switch to Blastoise
    print(f"\nFinal switch to {blastoise.name}...")
    battle.switch_pokemon(blastoise, "ally")
    
    # Final turns
    for turn in range(2):
        battle.advance_turn()
        battle.record_move_used("ally", "Hydro Pump")
        battle.record_move_used("opponent", "Earthquake")
        battle.record_damage("ally", 85)
        battle.record_damage("opponent", 110)
    
    tyranitar.current_hp = 40  # Very low
    
    print(f"\nFinal Battle Report with {blastoise.name}:")
    print(create_battle_report(battle))
    
    print("\nTeam Battle Summary:")
    summary = battle.get_battle_summary()
    print(f"  Total turns: {summary['turn_count']}")
    print(f"  Pokemon used: {summary['ally_pokemon_used']}")
    print(f"  Opponent moves seen: {len(summary['seen_opponent_moves'])}")
    
    print("\nTeam Performance:")
    for i, pokemon_history in enumerate(battle.ally_pokemon_history):
        print(f"  {pokemon_history.pokemon.name}:")
        print(f"    Active turns: {pokemon_history.turn_switched_in} to {pokemon_history.turn_switched_out}")
        print(f"    Damage taken: {pokemon_history.damage_taken}")
        print(f"    Moves used: {len(pokemon_history.moves_used)}")
    
    current = battle.current_ally_history
    print(f"  {current.pokemon.name} (current):")
    print(f"    Active since turn: {current.turn_switched_in}")
    print(f"    Damage taken: {current.damage_taken}")
    print(f"    Moves used: {len(current.moves_used)}")
    
    print("\n=== Team Battle Report Demo Complete ===")

if __name__ == "__main__":
    # Run battle report demo
    demo_battle_reports()
    
    # Run team battle report demo
    demo_team_battle_reports()
