from openai import Assistant, Tool
from battle.battle_state import BattleState
from battle.decision_engine import recommend_move

def select_move_tool(state: dict) -> str:
    battle_state = BattleState(**state)
    return recommend_move(battle_state)

tool = Tool.from_function(select_move_tool)
assistant = Assistant(tools=[tool])