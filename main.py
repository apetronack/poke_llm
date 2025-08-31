from battle.battle_state import BattleState
from battle.decision_engine import recommend_move
from pokemon import Pokemon

if __name__ == "__main__":
    print("=== Updated BattleState with Pokemon Objects ===")
    
    # Create Pokemon objects with specific moves
    blaziken_moves = ["flamethrower", "sky-uppercut", "earthquake", "slash"]
    sceptile_moves = ["leaf-blade", "earthquake", "dragon-claw", "aerial-ace"]
    
    # Using Pokemon objects directly
    print("Using Pokemon objects directly:")
    try:
        blaziken = Pokemon.from_api("blaziken", level=50, move_names=blaziken_moves)
        sceptile = Pokemon.from_api("sceptile", level=50, move_names=sceptile_moves)
        
        print(f"My Pokemon: {blaziken.name} ({'/'.join(blaziken.types)})")
        print(f"My moves: {[move.name for move in blaziken.moves]}")
        print(f"Opponent: {sceptile.name} ({'/'.join(sceptile.types)})")
        
        # Create BattleState with Pokemon objects directly
        state = BattleState(blaziken, sceptile)
        best = recommend_move(state)
        print(f"Recommended move: {best}")
        
    except Exception as e:
        print(f"API creation failed (possibly no internet): {e}")
        print("Falling back to manual creation...")
        
        # Fallback to manual creation if API fails
        from pokemon import PokemonStats, Move, Ability
        
        # Create Blaziken manually
        blaziken_stats = PokemonStats(80, 120, 70, 110, 70, 80)
        blaziken_moves_obj = [
            Move("Flamethrower", "Fire", 90, 100, 15, "special"),
            Move("Sky Uppercut", "Fighting", 85, 90, 15, "physical"),
            Move("Earthquake", "Ground", 100, 100, 10, "physical"),
            Move("Slash", "Normal", 70, 100, 20, "physical")
        ]
        blaziken = Pokemon("Blaziken", ["Fire", "Fighting"], blaziken_stats, blaziken_moves_obj, level=50)
        
        # Create Sceptile manually  
        sceptile_stats = PokemonStats(70, 85, 65, 105, 85, 120)
        sceptile_moves_obj = [
            Move("Leaf Blade", "Grass", 90, 100, 15, "physical"),
            Move("Earthquake", "Ground", 100, 100, 10, "physical")
        ]
        sceptile = Pokemon("Sceptile", ["Grass"], sceptile_stats, sceptile_moves_obj, level=50)
        
        print(f"My Pokemon: {blaziken.name} ({'/'.join(blaziken.types)})")
        print(f"Opponent: {sceptile.name} ({'/'.join(sceptile.types)})")
        
        state = BattleState(blaziken, sceptile)
        best = recommend_move(state)
        print(f"Recommended move: {best}")