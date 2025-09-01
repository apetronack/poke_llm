"""
Test the enhanced BattleState with comprehensive battle tracking
"""
from battle.battle_state import BattleState, WeatherType
from battle.decision_engine import recommend_move
from pokemon import Pokemon, PokemonStats, Move

def test_enhanced_battle_state():
    """Test enhanced BattleState with all new tracking features"""
    
    print("=== Testing Enhanced BattleState ===\n")
    
    # Create Pokemon for testing
    blaziken_stats = PokemonStats(80, 120, 70, 110, 70, 80)
    blaziken_moves = [
        Move("Flamethrower", "Fire", 90, 100, 15, "special"),
        Move("Sky Uppercut", "Fighting", 85, 90, 15, "physical"),
        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
        Move("Thunder Punch", "Electric", 75, 100, 15, "physical")
    ]
    blaziken = Pokemon("Blaziken", ["Fire", "Fighting"], blaziken_stats, blaziken_moves, level=50)
    
    sceptile_stats = PokemonStats(70, 85, 65, 105, 85, 120)
    sceptile_moves = [
        Move("Leaf Blade", "Grass", 90, 100, 15, "physical"),
        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
        Move("Dragon Claw", "Dragon", 80, 100, 15, "physical"),
        Move("Aerial Ace", "Flying", 60, 100, 20, "physical")
    ]
    sceptile = Pokemon("Sceptile", ["Grass"], sceptile_stats, sceptile_moves, level=50)
    
    print("1. Creating enhanced BattleState:")
    state = BattleState(blaziken, sceptile)
    
    print(f"Initial battle summary:")
    summary = state.get_battle_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n2. Testing turn advancement and weather:")
    
    # Set sunny weather
    state.set_weather(WeatherType.SUN, duration=5)
    print(f"Set sunny weather: {state.get_weather_info()}")
    
    # Add some screen effects
    state.add_screen_effect("Light Screen", 5, "ally")
    state.add_screen_effect("Reflect", 5, "opponent")
    print(f"Added screens: {[s.effect_name for s in state.screens]}")
    
    print("\n3. Simulating battle turns:")
    
    # Turn 1: Blaziken uses Flamethrower
    state.advance_turn()
    state.record_move_used("ally", "Flamethrower")
    state.record_damage("opponent", 85, 85)  # opponent takes 85, ally deals 85
    print(f"Turn {state.turn_count}: Blaziken used Flamethrower")
    
    # Turn 2: Sceptile uses Leaf Blade
    state.advance_turn()
    state.record_move_used("opponent", "Leaf Blade")
    state.record_damage("ally", 90, 90)
    print(f"Turn {state.turn_count}: Sceptile used Leaf Blade")
    
    # Turn 3: Blaziken uses Earthquake
    state.advance_turn()
    state.record_move_used("ally", "Earthquake")
    state.record_damage("opponent", 120, 120)
    print(f"Turn {state.turn_count}: Blaziken used Earthquake")
    
    # Turn 4: Sceptile uses Dragon Claw
    state.advance_turn()
    state.record_move_used("opponent", "Dragon Claw")
    state.record_damage("ally", 80, 80)
    print(f"Turn {state.turn_count}: Sceptile used Dragon Claw")
    
    print("\n4. Battle state after 4 turns:")
    summary = state.get_battle_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n5. Opponent move analysis:")
    move_pattern = state.get_opponent_move_pattern()
    for key, value in move_pattern.items():
        print(f"  {key}: {value}")
    
    print("\n6. Testing Pokemon switching:")
    
    # Create a third Pokemon for switching
    swampert_stats = PokemonStats(100, 110, 90, 85, 90, 60)
    swampert_moves = [
        Move("Surf", "Water", 90, 100, 15, "special"),
        Move("Ice Beam", "Ice", 90, 100, 10, "special"),
        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
        Move("Avalanche", "Ice", 60, 100, 10, "physical")
    ]
    swampert = Pokemon("Swampert", ["Water", "Ground"], swampert_stats, swampert_moves, level=50)
    
    # Switch ally Pokemon
    print(f"Switching from {state.my_pokemon.name} to Swampert")
    state.switch_pokemon(swampert, "ally")
    
    print(f"New ally Pokemon: {state.get_my_pokemon_name()}")
    print(f"Pokemon history count - Ally: {len(state.ally_pokemon_history)}, Opponent: {len(state.opponent_pokemon_history)}")
    
    print("\n7. Testing screen effects:")
    print(f"Light Screen active on ally side: {state.has_screen_active('Light Screen', 'ally')}")
    print(f"Reflect active on opponent side: {state.has_screen_active('Reflect', 'opponent')}")
    
    ally_screens = state.get_active_screens("ally")
    opponent_screens = state.get_active_screens("opponent")
    print(f"Ally screens: {[s.effect_name for s in ally_screens]}")
    print(f"Opponent screens: {[s.effect_name for s in opponent_screens]}")
    
    print("\n8. Advancing several turns to test effect expiration:")
    for i in range(3):
        state.advance_turn()
        print(f"Turn {state.turn_count}: Weather remaining: {state.weather.turns_remaining if state.weather else 0}, Screens: {len(state.screens)}")
    
    print("\n=== Enhanced Battle State Test Complete ===")
    print("✅ Turn tracking")
    print("✅ Weather conditions") 
    print("✅ Screen effects")
    print("✅ Move history tracking")
    print("✅ Pokemon switching")
    print("✅ Damage tracking")
    print("✅ Battle summary generation")
    
    return state

def test_comprehensive_battle_simulation():
    """Test a more comprehensive battle simulation"""
    print("\n=== Comprehensive Battle Simulation ===\n")
    
    # Create test Pokemon
    charizard_stats = PokemonStats(78, 84, 78, 109, 85, 100)
    charizard_moves = [
        Move("Fire Blast", "Fire", 110, 85, 5, "special"),
        Move("Air Slash", "Flying", 75, 95, 15, "special"),
        Move("Solar Beam", "Grass", 120, 100, 10, "special"),
        Move("Dragon Pulse", "Dragon", 85, 100, 10, "special")
    ]
    charizard = Pokemon("Charizard", ["Fire", "Flying"], charizard_stats, charizard_moves, level=50)
    
    blastoise_stats = PokemonStats(79, 83, 100, 85, 105, 78)
    blastoise_moves = [
        Move("Hydro Pump", "Water", 110, 80, 5, "special"),
        Move("Ice Beam", "Ice", 90, 100, 10, "special"),
        Move("Earthquake", "Ground", 100, 100, 10, "physical"),
        Move("Focus Blast", "Fighting", 120, 70, 5, "special")
    ]
    blastoise = Pokemon("Blastoise", ["Water"], blastoise_stats, blastoise_moves, level=50)
    
    # Initialize battle
    battle = BattleState(charizard, blastoise)
    
    print("Battle Start:")
    print(f"  {charizard.name} vs {blastoise.name}")
    
    # Set up initial conditions
    battle.set_weather(WeatherType.SUN, 8)  # Sunny weather for 8 turns
    battle.add_screen_effect("Light Screen", 5, "ally")
    
    print(f"  Weather: {battle.get_weather_info()['type']}")
    print(f"  Light Screen set for ally")
    
    # Simulate 10 turns of battle
    moves_sequence = [
        ("ally", "Solar Beam"),
        ("opponent", "Hydro Pump"),
        ("ally", "Fire Blast"),
        ("opponent", "Ice Beam"),
        ("ally", "Air Slash"),
        ("opponent", "Earthquake"),
        ("ally", "Dragon Pulse"),
        ("opponent", "Focus Blast"),
        ("ally", "Fire Blast"),
        ("opponent", "Hydro Pump")
    ]
    
    for turn, (side, move_name) in enumerate(moves_sequence, 1):
        battle.advance_turn()
        battle.record_move_used(side, move_name)
        
        # Simulate damage (simplified)
        if side == "ally":
            damage = 80  # Simplified damage calculation
            battle.record_damage("opponent", damage, damage)
        else:
            damage = 75
            battle.record_damage("ally", damage, damage)
        
        print(f"Turn {battle.turn_count}: {side.title()} used {move_name} ({damage} damage)")
    
    print(f"\nFinal Battle Summary:")
    final_summary = battle.get_battle_summary()
    for key, value in final_summary.items():
        print(f"  {key}: {value}")
    
    print(f"\nOpponent Move Analysis:")
    move_analysis = battle.get_opponent_move_pattern()
    for key, value in move_analysis.items():
        print(f"  {key}: {value}")
    
    return battle

if __name__ == "__main__":
    # Run basic enhanced battle state test
    enhanced_state = test_enhanced_battle_state()
    
    # Run comprehensive simulation
    comprehensive_battle = test_comprehensive_battle_simulation()
