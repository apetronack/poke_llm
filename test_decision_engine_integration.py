#!/usr/bin/env python3
"""
Test script to demonstrate the integration of damage calculator with decision engine.
"""

from pokemon import Pokemon, Move
from battle.battle_state import BattleState
from battle.decision_engine import (
    recommend_move, 
    recommend_move_with_analysis, 
    get_all_move_analysis,
    calculate_move_damage
)

def test_damage_calculator_integration():
    """Test the integration between damage calculator and decision engine"""
    
    print("=== Testing Damage Calculator Integration ===\n")
    
    # Create test Pokemon with known moves
    # Charizard (Fire/Flying)
    charizard = Pokemon.from_api("charizard", level=50, move_names=["flamethrower", "air-slash", "dragon-pulse", "solar-beam"])
    
    # Venusaur (Grass/Poison) - weak to Fire and Flying moves
    venusaur = Pokemon.from_api("venusaur", level=50, move_names=["vine-whip", "sludge-bomb", "earthquake", "sleep-powder"])
    
    print(f"Attacker: {charizard}")
    print(f"Defender: {venusaur}")
    print()
    
    # Create battle state
    state = BattleState(charizard, venusaur)
    
    # Test basic move recommendation
    print("=== Basic Move Recommendation ===")
    best_move = recommend_move(state)
    print(f"Recommended move: {best_move}")
    print()
    
    # Test detailed analysis
    print("=== Detailed Move Analysis ===")
    best_move_detailed, analysis = recommend_move_with_analysis(state)
    print(f"Best move (with analysis): {best_move_detailed}")
    print()
    
    print("All moves analysis:")
    for i, move_data in enumerate(analysis, 1):
        print(f"{i}. {move_data['name']} ({move_data['type']}):")
        print(f"   Power: {move_data['power']}, Accuracy: {move_data['accuracy']}%")
        print(f"   Damage Class: {move_data['damage_class']}")
        
        if move_data.get('is_status_move'):
            print(f"   Status move (no damage)")
        else:
            print(f"   Damage Range: {move_data['min_damage']}-{move_data['max_damage']}")
            print(f"   Expected Damage: {move_data['expected_damage']:.1f}")
            print(f"   Damage %: {move_data['damage_percent']:.1f}%")
            print(f"   Can KO: {move_data['can_ko']}, Guaranteed KO: {move_data['guaranteed_ko']}")
        print()
    
    # Test individual move damage calculation
    print("=== Individual Move Damage Tests ===")
    for move in charizard.moves:
        damage = calculate_move_damage(charizard, venusaur, move)
        print(f"{move.name} ({move.type}, {move.damage_class}): {damage} damage")
    print()
    
    print("=== Type Effectiveness Demonstration ===")
    # Test against different type combinations
    # Blastoise (Water) - resists Fire, weak to Grass
    blastoise = Pokemon.from_api("blastoise", level=50)
    
    state_vs_blastoise = BattleState(charizard, blastoise)
    
    print(f"Charizard vs Blastoise:")
    _, analysis_vs_blastoise = recommend_move_with_analysis(state_vs_blastoise)
    for move_data in analysis_vs_blastoise[:2]:  # Show top 2 moves
        print(f"  {move_data['name']}: {move_data['expected_damage']:.1f} expected damage")
    
    print(f"\nCharizard vs Venusaur:")
    for move_data in analysis[:2]:  # Show top 2 moves
        print(f"  {move_data['name']}: {move_data['expected_damage']:.1f} expected damage")

def test_legacy_compatibility():
    """Test that the system still works with dictionary format"""
    print("\n=== Testing Legacy Dictionary Compatibility ===")
    
    # Create Pokemon using dictionary format (legacy)
    my_pokemon_dict = {
        'name': 'Pikachu',
        'types': ['Electric'],
        'level': 50
    }
    
    opponent_pokemon_dict = {
        'name': 'Gyarados', 
        'types': ['Water', 'Flying'],
        'level': 50
    }
    
    moves_dict = [
        {'name': 'Thunderbolt', 'type': 'Electric', 'power': 90, 'accuracy': 100},
        {'name': 'Quick Attack', 'type': 'Normal', 'power': 40, 'accuracy': 100},
        {'name': 'Iron Tail', 'type': 'Steel', 'power': 100, 'accuracy': 75},
        {'name': 'Thunder Wave', 'type': 'Electric', 'power': 0, 'accuracy': 90}
    ]
    
    state_legacy = BattleState(my_pokemon_dict, opponent_pokemon_dict, moves_dict)
    
    best_move_legacy = recommend_move(state_legacy)
    print(f"Legacy format - Best move: {best_move_legacy}")

if __name__ == "__main__":
    try:
        test_damage_calculator_integration()
        test_legacy_compatibility()
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
