"""
Battle state utilities for convenient access to enhanced battle tracking features
"""
from typing import Dict, List, Optional, Tuple
from battle.battle_state import BattleState, WeatherType, ScreenEffect, PokemonBattleHistory
from pokemon import Pokemon

class BattleStateAnalyzer:
    """Utility class for analyzing battle state and providing insights"""
    
    def __init__(self, battle_state: BattleState):
        self.battle_state = battle_state
    
    def get_momentum_analysis(self) -> Dict:
        """Analyze battle momentum based on recent events"""
        recent_turns = 3
        
        # Get recent moves from both sides
        ally_recent = []
        opponent_recent = []
        
        if hasattr(self.battle_state, 'current_ally_history'):
            ally_moves = self.battle_state.current_ally_history.moves_used
            ally_recent = [move for move, turn in ally_moves if turn > self.battle_state.turn_count - recent_turns]
        
        if hasattr(self.battle_state, 'opponent_move_history'):
            opponent_moves = self.battle_state.opponent_move_history
            opponent_recent = [move for move, turn, _ in opponent_moves if turn > self.battle_state.turn_count - recent_turns]
        
        return {
            "recent_ally_moves": ally_recent,
            "recent_opponent_moves": opponent_recent,
            "turn_count": self.battle_state.turn_count,
            "weather_turns_left": self.battle_state.weather.turns_remaining if self.battle_state.weather else 0,
            "active_screens": len(self.battle_state.screens)
        }
    
    def predict_opponent_next_move(self) -> Dict:
        """Predict opponent's next move based on patterns"""
        patterns = self.battle_state.get_opponent_move_pattern()
        
        if not patterns['recent_moves']:
            return {"prediction": "Unknown", "confidence": 0}
        
        # Simple prediction based on frequency
        move_freq = patterns['move_frequency']
        most_frequent = max(move_freq.items(), key=lambda x: x[1]) if move_freq else None
        
        # Check for recent patterns
        recent = patterns['recent_moves'][-3:] if len(patterns['recent_moves']) >= 3 else patterns['recent_moves']
        
        prediction = most_frequent[0] if most_frequent else "Unknown"
        
        # Calculate confidence based on frequency
        total_moves = sum(move_freq.values()) if move_freq else 1
        confidence = (most_frequent[1] / total_moves * 100) if most_frequent else 0
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "reasoning": f"Most used move ({most_frequent[1]}/{total_moves} times)" if most_frequent else "No pattern detected",
            "recent_pattern": recent
        }
    
    def get_type_effectiveness_summary(self) -> Dict:
        """Get type effectiveness summary for current matchup"""
        ally_types = self.battle_state.my_pokemon.types
        opponent_types = self.battle_state.opponent_pokemon.types
        
        # Simplified type effectiveness (in a real implementation, use the type chart)
        effectiveness_chart = {
            "Fire": {"Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Steel": 2.0, "Water": 0.5, "Fire": 0.5, "Rock": 0.5, "Dragon": 0.5},
            "Water": {"Fire": 2.0, "Ground": 2.0, "Rock": 2.0, "Water": 0.5, "Grass": 0.5, "Dragon": 0.5},
            "Grass": {"Water": 2.0, "Ground": 2.0, "Rock": 2.0, "Fire": 0.5, "Grass": 0.5, "Poison": 0.5, "Flying": 0.5, "Bug": 0.5, "Dragon": 0.5, "Steel": 0.5},
            "Electric": {"Water": 2.0, "Flying": 2.0, "Electric": 0.5, "Grass": 0.5, "Dragon": 0.5, "Ground": 0.0},
            "Flying": {"Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Electric": 0.5, "Rock": 0.5, "Steel": 0.5},
            "Fighting": {"Normal": 2.0, "Ice": 2.0, "Rock": 2.0, "Dark": 2.0, "Steel": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Fairy": 0.5, "Ghost": 0.0}
        }
        
        ally_advantages = []
        ally_disadvantages = []
        
        for ally_type in ally_types:
            if ally_type in effectiveness_chart:
                for opp_type in opponent_types:
                    multiplier = effectiveness_chart[ally_type].get(opp_type, 1.0)
                    if multiplier > 1.0:
                        ally_advantages.append(f"{ally_type} vs {opp_type}")
                    elif multiplier < 1.0:
                        ally_disadvantages.append(f"{ally_type} vs {opp_type}")
        
        return {
            "ally_types": ally_types,
            "opponent_types": opponent_types,
            "advantages": ally_advantages,
            "disadvantages": ally_disadvantages,
            "recommendation": "Use type advantages" if ally_advantages else "Consider switching or status moves"
        }
    
    def get_battle_phase_analysis(self) -> Dict:
        """Analyze what phase of battle we're in"""
        turn_count = self.battle_state.turn_count
        ally_hp_percent = (self.battle_state.my_pokemon.current_hp / self.battle_state.my_pokemon.calculate_hp()) * 100
        opponent_hp_percent = (self.battle_state.opponent_pokemon.current_hp / self.battle_state.opponent_pokemon.calculate_hp()) * 100
        
        phase = "early"
        if turn_count > 10:
            phase = "late"
        elif turn_count > 5:
            phase = "mid"
        
        strategy = "aggressive"
        if ally_hp_percent < 30:
            strategy = "defensive"
        elif opponent_hp_percent < 30:
            strategy = "finishing"
        elif ally_hp_percent > 70 and opponent_hp_percent > 70:
            strategy = "setup"
        
        return {
            "phase": phase,
            "turn_count": turn_count,
            "ally_hp_percent": ally_hp_percent,
            "opponent_hp_percent": opponent_hp_percent,
            "recommended_strategy": strategy,
            "urgency": "high" if min(ally_hp_percent, opponent_hp_percent) < 25 else "normal"
        }

def create_battle_report(battle_state: BattleState) -> str:
    """Generate a comprehensive battle report"""
    analyzer = BattleStateAnalyzer(battle_state)
    
    # Get all analysis data
    summary = battle_state.get_battle_summary()
    momentum = analyzer.get_momentum_analysis()
    prediction = analyzer.predict_opponent_next_move()
    type_analysis = analyzer.get_type_effectiveness_summary()
    phase_analysis = analyzer.get_battle_phase_analysis()
    
    report = []
    report.append("=" * 50)
    report.append("BATTLE REPORT")
    report.append("=" * 50)
    
    # Current state
    report.append(f"\nCURRENT BATTLE STATE (Turn {summary['turn_count']}):")
    report.append(f"  Your Pokemon: {summary['current_pokemon']['ally']['name']} ({summary['current_pokemon']['ally']['hp']})")
    report.append(f"  Opponent: {summary['current_pokemon']['opponent']['name']} ({summary['current_pokemon']['opponent']['hp']})")
    
    # Weather and field conditions
    if summary['weather']['type'] != 'none':
        report.append(f"  Weather: {summary['weather']['type']} ({summary['weather']['turns_remaining']} turns left)")
    
    if summary['screens']:
        report.append("  Active screens:")
        for screen in summary['screens']:
            report.append(f"    {screen['effect']} ({screen['side']}, {screen['turns_remaining']} turns)")
    
    # Battle phase
    report.append(f"\nBATTLE PHASE: {phase_analysis['phase'].upper()}")
    report.append(f"  Strategy: {phase_analysis['recommended_strategy']}")
    report.append(f"  Urgency: {phase_analysis['urgency']}")
    
    # Type effectiveness
    report.append(f"\nTYPE MATCHUP:")
    report.append(f"  Your types: {', '.join(type_analysis['ally_types'])}")
    report.append(f"  Opponent types: {', '.join(type_analysis['opponent_types'])}")
    if type_analysis['advantages']:
        report.append(f"  Advantages: {', '.join(type_analysis['advantages'])}")
    if type_analysis['disadvantages']:
        report.append(f"  Disadvantages: {', '.join(type_analysis['disadvantages'])}")
    report.append(f"  Recommendation: {type_analysis['recommendation']}")
    
    # Opponent intelligence
    report.append(f"\nOPPONENT ANALYSIS:")
    report.append(f"  Moves seen: {', '.join(summary['seen_opponent_moves'])}")
    if prediction['prediction'] != "Unknown":
        report.append(f"  Predicted next move: {prediction['prediction']} ({prediction['confidence']:.1f}% confidence)")
        report.append(f"  Reasoning: {prediction['reasoning']}")
    
    # Team usage
    if summary['ally_pokemon_used'] > 1:
        report.append(f"\nTEAM STATUS:")
        report.append(f"  Pokemon used: {summary['ally_pokemon_used']}")
        report.append(f"  Opponent Pokemon seen: {summary['opponent_pokemon_used']}")
    
    report.append("\n" + "=" * 50)
    
    return "\n".join(report)

def get_battle_recommendations(battle_state: BattleState) -> Dict:
    """Get strategic recommendations based on current battle state"""
    analyzer = BattleStateAnalyzer(battle_state)
    phase_analysis = analyzer.get_battle_phase_analysis()
    type_analysis = analyzer.get_type_effectiveness_summary()
    
    recommendations = []
    
    # Phase-based recommendations
    if phase_analysis['recommended_strategy'] == 'finishing':
        recommendations.append("Focus on high-damage moves to finish the opponent")
    elif phase_analysis['recommended_strategy'] == 'defensive':
        recommendations.append("Consider healing or switching to a healthier Pokemon")
    elif phase_analysis['recommended_strategy'] == 'setup':
        recommendations.append("Good time for stat boosts or field setup moves")
    
    # Type-based recommendations
    if type_analysis['advantages']:
        recommendations.append("Use moves matching your type advantages")
    elif type_analysis['disadvantages']:
        recommendations.append("Consider switching Pokemon or using neutral moves")
    
    # Weather recommendations
    weather_info = battle_state.get_weather_info()
    if weather_info['type'] == 'sun':
        recommendations.append("Fire moves boosted, Water moves weakened")
    elif weather_info['type'] == 'rain':
        recommendations.append("Water moves boosted, Fire moves weakened")
    
    # Screen recommendations
    ally_screens = battle_state.get_active_screens("ally")
    opponent_screens = battle_state.get_active_screens("opponent")
    
    if any(s.effect_name == "Light Screen" for s in opponent_screens):
        recommendations.append("Opponent has Light Screen - use physical moves")
    if any(s.effect_name == "Reflect" for s in opponent_screens):
        recommendations.append("Opponent has Reflect - use special moves")
    
    return {
        "recommendations": recommendations,
        "priority": phase_analysis['urgency'],
        "phase": phase_analysis['phase']
    }
