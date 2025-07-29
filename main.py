from battle.battle_state import BattleState
from battle.decision_engine import recommend_move

if __name__ == "__main__":
    my_pokemon = {"name": "Blaziken", "types": ["Fire", "Fighting"]}
    opponent_pokemon = {"name": "Sceptile", "types": ["Grass"]}
    my_moves = [
        {"name": "Flamethrower", "type": "Fire", "power": 90, "accuracy": 100},
        {"name": "Sky Uppercut", "type": "Fighting", "power": 85, "accuracy": 90},
        {"name": "Earthquake", "type": "Ground", "power": 100, "accuracy": 100},
        {"name": "Slash", "type": "Normal", "power": 70, "accuracy": 100}
    ]
    state = BattleState(my_pokemon, opponent_pokemon, my_moves)
    best = recommend_move(state)
    print(f"Recommended move: {best}")