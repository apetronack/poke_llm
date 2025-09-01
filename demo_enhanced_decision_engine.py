"""
Demo script showing the enhanced decision engine with comprehensive battle state tracking
"""
from battle.battle_state import BattleState, WeatherType
from battle.decision_engine import recommend_move, get_all_move_analysis, recommend_move_with_analysis
from pokemon import Pokemon, PokemonStats, Move

def demo_enhanced_decision_making():
    """Demo the enhanced decision engine with battle state considerations"""
    
    print("=== Enhanced Pokemon Battle Decision Engine Demo ===\n")
    
    # Create Pokemon for the demo
    print("1. Setting up Pokemon:")
    
    # Charizard with fire/flying moves
    charizard_stats = PokemonStats(78, 84, 78, 109, 85, 100)
    charizard_moves = [
        Move("Fire Blast", "Fire", 110, 85, 5, "special"),
        Move("Air Slash", "Flying", 75, 95, 15, "special"),
        Move("Solar Beam", "Grass", 120, 100, 10, "special"),  # Benefits from sun
        Move("Thunder Punch", "Electric", 75, 100, 15, "physical")
    ]
    charizard = Pokemon("Charizard", ["Fire", "Flying"], charizard_stats, charizard_moves, level=50)
    charizard.current_hp = 120  # Partially damaged
    
    # Venusaur as opponent
    venusaur_stats = PokemonStats(80, 82, 83, 100, 100, 80)
    venusaur_moves = [
        Move("Petal Blizzard", "Grass", 90, 100, 15, "physical"),
        Move("Sludge Bomb", "Poison", 90, 100, 10, "special"),
        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
        Move("Weather Ball", "Normal", 50, 100, 10, "special")  # Changes with weather
    ]
    venusaur = Pokemon("Venusaur", ["Grass", "Poison"], venusaur_stats, venusaur_moves, level=50)
    venusaur.current_hp = 80  # Low HP
    
    print(f"  Charizard (HP: {charizard.current_hp}/{charizard.calculate_hp()})")
    print(f"  vs Venusaur (HP: {venusaur.current_hp}/{venusaur.calculate_hp()})")
    
    # Initialize battle state
    battle = BattleState(charizard, venusaur)
    
    print("\n2. Testing move recommendations under different conditions:")
    
    # Scenario 1: Normal conditions
    print("\nScenario 1: Normal battle conditions")
    best_move = recommend_move(battle)
    print(f"  Recommended move: {best_move}")
    
    # Get detailed analysis
    move_analysis = get_all_move_analysis(battle)
    print("  Move analysis:")
    for move_data in move_analysis[:2]:  # Show top 2 moves
        print(f"    {move_data['name']}: {move_data['expected_damage']:.1f} expected damage")
    
    # Scenario 2: Sunny weather (boosts Fire moves)
    print("\nScenario 2: Sunny weather active")
    battle.set_weather(WeatherType.SUN, 5)
    print(f"  Weather: {battle.get_weather_info()['type']}")
    
    best_move_sun = recommend_move(battle)
    print(f"  Recommended move: {best_move_sun}")
    
    # Scenario 3: Opponent has Light Screen (reduces special damage)
    print("\nScenario 3: Opponent has Light Screen active")
    battle.add_screen_effect("Light Screen", 3, "opponent")
    
    opponent_screens = battle.get_active_screens("opponent")
    print(f"  Opponent screens: {[s.effect_name for s in opponent_screens]}")
    
    best_move_screen = recommend_move(battle)
    print(f"  Recommended move: {best_move_screen}")
    
    # Scenario 4: Simulate opponent move history for pattern recognition
    print("\nScenario 4: After observing opponent move patterns")
    
    # Simulate some turns with opponent using grass moves frequently
    for i in range(3):
        battle.advance_turn()
        battle.record_move_used("opponent", "Petal Blizzard")
        battle.advance_turn()
    
    # Also record that opponent used Earthquake once
    battle.record_move_used("opponent", "Earthquake")
    
    patterns = battle.get_opponent_move_pattern()
    print(f"  Opponent patterns: {patterns['move_frequency']}")
    print(f"  Most used move: {patterns['most_used']}")
    
    best_move_pattern = recommend_move(battle)
    print(f"  Recommended move: {best_move_pattern}")
    
    # Scenario 5: Low HP situation (potential KO)
    print("\nScenario 5: Opponent at very low HP")
    venusaur.current_hp = 25  # Very low HP
    
    best_move_ko, analysis = recommend_move_with_analysis(battle)
    print(f"  Recommended move: {best_move_ko}")
    
    # Show which moves can KO
    print("  KO potential analysis:")
    for move_data in analysis:
        if move_data['can_ko']:
            print(f"    {move_data['name']}: Can KO! ({move_data['max_damage']} max damage)")
        elif move_data['damage_percent'] > 50:
            print(f"    {move_data['name']}: {move_data['damage_percent']:.1f}% damage")
    
    print("\n3. Complete battle state summary:")
    final_summary = battle.get_battle_summary()
    for key, value in final_summary.items():
        print(f"  {key}: {value}")
    
    print("\n=== Demo Complete ===")
    print("✅ Weather-based move selection")
    print("✅ Screen effect considerations")
    print("✅ Opponent pattern recognition")
    print("✅ KO opportunity detection")
    print("✅ Comprehensive battle analysis")

def demo_team_battle_tracking():
    """Demo team battle with multiple Pokemon switches"""
    
    print("\n=== Team Battle Tracking Demo ===\n")
    
    # Create a team of 3 Pokemon
    team_pokemon = []
    
    # Pokemon 1: Charizard
    charizard_stats = PokemonStats(78, 84, 78, 109, 85, 100)
    charizard_moves = [Move("Fire Blast", "Fire", 110, 85, 5, "special"),
                       Move("Air Slash", "Flying", 75, 95, 15, "special")]
    charizard = Pokemon("Charizard", ["Fire", "Flying"], charizard_stats, charizard_moves, level=50)
    team_pokemon.append(charizard)
    
    # Pokemon 2: Blastoise
    blastoise_stats = PokemonStats(79, 83, 100, 85, 105, 78)
    blastoise_moves = [Move("Hydro Pump", "Water", 110, 80, 5, "special"),
                       Move("Ice Beam", "Ice", 90, 100, 10, "special")]
    blastoise = Pokemon("Blastoise", ["Water"], blastoise_stats, blastoise_moves, level=50)
    team_pokemon.append(blastoise)
    
    # Pokemon 3: Venusaur
    venusaur_stats = PokemonStats(80, 82, 83, 100, 100, 80)
    venusaur_moves = [Move("Petal Blizzard", "Grass", 90, 100, 15, "physical"),
                      Move("Sludge Bomb", "Poison", 90, 100, 10, "special")]
    venusaur = Pokemon("Venusaur", ["Grass", "Poison"], venusaur_stats, venusaur_moves, level=50)
    team_pokemon.append(venusaur)
    
    # Opponent Pokemon
    opponent_stats = PokemonStats(85, 90, 85, 90, 85, 85)
    opponent_moves = [Move("Earthquake", "Ground", 100, 100, 10, "physical"),
                      Move("Stone Edge", "Rock", 100, 80, 5, "physical")]
    opponent = Pokemon("Tyranitar", ["Rock", "Dark"], opponent_stats, opponent_moves, level=50)
    
    # Start battle with Charizard
    battle = BattleState(charizard, opponent)
    
    print("1. Battle starts with Charizard")
    print(f"   Active: {battle.get_my_pokemon_name()} vs {battle.get_opponent_pokemon_name()}")
    
    # Simulate some turns
    for turn in range(1, 4):
        battle.advance_turn()
        battle.record_move_used("ally", charizard.moves[0].name)
        battle.record_move_used("opponent", opponent.moves[0].name)
        battle.record_damage("ally", 50)
        battle.record_damage("opponent", 80)
        print(f"   Turn {battle.turn_count}: {charizard.moves[0].name} vs {opponent.moves[0].name}")
    
    # Charizard gets low, switch to Blastoise
    print(f"\n2. Charizard HP low, switching to Blastoise")
    battle.switch_pokemon(blastoise, "ally")
    print(f"   New active: {battle.get_my_pokemon_name()}")
    print(f"   Team history: {len(battle.ally_pokemon_history)} Pokemon used previously")
    
    # More turns with Blastoise
    for turn in range(2):
        battle.advance_turn()
        battle.record_move_used("ally", blastoise.moves[0].name)
        battle.record_move_used("opponent", opponent.moves[1].name)
        battle.record_damage("ally", 40)
        battle.record_damage("opponent", 90)
        print(f"   Turn {battle.turn_count}: {blastoise.moves[0].name} vs {opponent.moves[1].name}")
    
    # Switch to Venusaur
    print(f"\n3. Switching to Venusaur for type advantage")
    battle.switch_pokemon(venusaur, "ally")
    print(f"   New active: {battle.get_my_pokemon_name()}")
    
    # Final turns
    for turn in range(2):
        battle.advance_turn()
        battle.record_move_used("ally", venusaur.moves[0].name)
        battle.record_move_used("opponent", opponent.moves[0].name)
        print(f"   Turn {battle.turn_count}: {venusaur.moves[0].name} vs {opponent.moves[0].name}")
    
    print("\n4. Final team battle summary:")
    summary = battle.get_battle_summary()
    print(f"   Total turns: {summary['turn_count']}")
    print(f"   Pokemon used: {summary['ally_pokemon_used']}")
    print(f"   Moves seen from opponent: {len(summary['seen_opponent_moves'])}")
    
    print("\n5. Team Pokemon history:")
    for i, pokemon_history in enumerate(battle.ally_pokemon_history):
        print(f"   Pokemon {i+1}: {pokemon_history.pokemon.name}")
        print(f"     Turns active: {pokemon_history.turn_switched_in} to {pokemon_history.turn_switched_out}")
        print(f"     Moves used: {[move for move, turn in pokemon_history.moves_used]}")
        print(f"     Damage taken/dealt: {pokemon_history.damage_taken}/{pokemon_history.damage_dealt}")
    
    # Current Pokemon
    current = battle.current_ally_history
    print(f"   Current Pokemon: {current.pokemon.name}")
    print(f"     Since turn: {current.turn_switched_in}")
    print(f"     Moves used: {[move for move, turn in current.moves_used]}")
    
    print("\n=== Team Battle Demo Complete ===")

if __name__ == "__main__":
    # Run the decision engine demo
    demo_enhanced_decision_making()
    
    # Run the team battle demo
    demo_team_battle_tracking()
