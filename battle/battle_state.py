from typing import Union, Dict, List, Optional, Set
from dataclasses import dataclass, field
from pokemon import Pokemon, Move
from enum import Enum

class WeatherType(Enum):
    """Weather conditions that can be active in battle"""
    NONE = "none"
    SUN = "sun"
    RAIN = "rain"
    SANDSTORM = "sandstorm"
    HAIL = "hail"
    SNOW = "snow"  # For newer generations
    FOG = "fog"
    HARSH_SUNLIGHT = "harsh_sunlight"
    HEAVY_RAIN = "heavy_rain"
    STRONG_WINDS = "strong_winds"

@dataclass
class WeatherCondition:
    """Represents active weather in battle"""
    weather_type: WeatherType
    turns_remaining: int
    is_permanent: bool = False  # For abilities like Drought

@dataclass
class ScreenEffect:
    """Represents screen effects like Light Screen, Reflect, etc."""
    effect_name: str
    turns_remaining: int
    affects_side: str  # "ally" or "opponent"

@dataclass
class PokemonBattleHistory:
    """Tracks a Pokemon's battle history"""
    pokemon: Pokemon
    turn_switched_in: int
    turn_switched_out: Optional[int] = None
    moves_used: List[tuple] = field(default_factory=list)  # (move_name, turn)
    damage_taken: int = 0
    damage_dealt: int = 0
    was_ko: bool = False

class BattleState:
    def __init__(self, my_pokemon: Pokemon, opponent_pokemon: Pokemon):
        """
        Initialize BattleState with comprehensive battle tracking.
        Args:
            my_pokemon: Pokemon object
            opponent_pokemon: Pokemon object
        """
        self.my_pokemon = my_pokemon
        self.my_moves = my_pokemon.moves
        self.opponent_pokemon = opponent_pokemon
        self.opponent_moves = opponent_pokemon.moves
        
        # Battle tracking
        self.turn_count = 0
        self.weather: Optional[WeatherCondition] = None
        self.screens: List[ScreenEffect] = []
        
        # Pokemon history tracking
        self.ally_pokemon_history: List[PokemonBattleHistory] = []
        self.opponent_pokemon_history: List[PokemonBattleHistory] = []
        
        # Currently active Pokemon history entries
        self.current_ally_history = PokemonBattleHistory(my_pokemon, 0)
        self.current_opponent_history = PokemonBattleHistory(opponent_pokemon, 0)
        
        # Seen moves tracking
        self.seen_opponent_moves: Set[str] = set()
        self.opponent_move_history: List[tuple] = []  # (move_name, turn, target)
        
        # Battle state flags
        self.is_my_turn = True
        self.battle_ended = False
        self.winner: Optional[str] = None

    # Original methods for backward compatibility
    def get_my_pokemon_types(self) -> List[str]:
        """Get my Pokemon's types"""
        return self.my_pokemon.types

    def get_opponent_pokemon_types(self) -> List[str]:
        """Get opponent Pokemon's types"""
        return self.opponent_pokemon.types

    def get_my_pokemon_name(self) -> str:
        """Get my Pokemon's name"""
        return self.my_pokemon.name

    def get_opponent_pokemon_name(self) -> str:
        """Get opponent Pokemon's name"""
        return self.opponent_pokemon.name

    # New battle state tracking methods
    def advance_turn(self):
        """Advance to the next turn and update effects"""
        self.turn_count += 1
        self.is_my_turn = not self.is_my_turn
        
        # Update weather
        if self.weather and not self.weather.is_permanent:
            self.weather.turns_remaining -= 1
            if self.weather.turns_remaining <= 0:
                self.weather = None
        
        # Update screens
        self.screens = [screen for screen in self.screens 
                       if self._update_screen_effect(screen)]
    
    def _update_screen_effect(self, screen: ScreenEffect) -> bool:
        """Update screen effect and return True if it should continue"""
        screen.turns_remaining -= 1
        return screen.turns_remaining > 0

    def set_weather(self, weather_type: WeatherType, duration: int = 5, permanent: bool = False):
        """Set the current weather condition"""
        self.weather = WeatherCondition(weather_type, duration, permanent)

    def clear_weather(self):
        """Clear the current weather"""
        self.weather = None

    def add_screen_effect(self, effect_name: str, duration: int, side: str):
        """Add a screen effect (Light Screen, Reflect, etc.)"""
        # Remove existing effect of the same type on the same side
        self.screens = [s for s in self.screens 
                       if not (s.effect_name == effect_name and s.affects_side == side)]
        
        screen = ScreenEffect(effect_name, duration, side)
        self.screens.append(screen)

    def get_active_screens(self, side: str) -> List[ScreenEffect]:
        """Get all active screen effects for a side"""
        return [screen for screen in self.screens if screen.affects_side == side]

    def record_move_used(self, pokemon_side: str, move_name: str, target: str = "opponent"):
        """Record that a move was used"""
        if pokemon_side == "ally":
            self.current_ally_history.moves_used.append((move_name, self.turn_count))
        elif pokemon_side == "opponent":
            self.current_opponent_history.moves_used.append((move_name, self.turn_count))
            self.seen_opponent_moves.add(move_name)
            self.opponent_move_history.append((move_name, self.turn_count, target))

    def record_damage(self, pokemon_side: str, damage_taken: int, damage_dealt: int = 0):
        """Record damage taken and dealt"""
        if pokemon_side == "ally":
            self.current_ally_history.damage_taken += damage_taken
            self.current_ally_history.damage_dealt += damage_dealt
        elif pokemon_side == "opponent":
            self.current_opponent_history.damage_taken += damage_taken
            self.current_opponent_history.damage_dealt += damage_dealt

    def switch_pokemon(self, new_pokemon: Pokemon, side: str):
        """Handle Pokemon switching"""
        if side == "ally":
            # Archive current Pokemon history
            self.current_ally_history.turn_switched_out = self.turn_count
            self.ally_pokemon_history.append(self.current_ally_history)
            
            # Update current Pokemon
            self.my_pokemon = new_pokemon
            self.my_moves = new_pokemon.moves
            self.current_ally_history = PokemonBattleHistory(new_pokemon, self.turn_count)
            
        elif side == "opponent":
            # Archive current Pokemon history
            self.current_opponent_history.turn_switched_out = self.turn_count
            self.opponent_pokemon_history.append(self.current_opponent_history)
            
            # Update current Pokemon
            self.opponent_pokemon = new_pokemon
            self.opponent_moves = new_pokemon.moves
            self.current_opponent_history = PokemonBattleHistory(new_pokemon, self.turn_count)

    def record_ko(self, pokemon_side: str):
        """Record that a Pokemon was knocked out"""
        if pokemon_side == "ally":
            self.current_ally_history.was_ko = True
        elif pokemon_side == "opponent":
            self.current_opponent_history.was_ko = True

    def get_battle_summary(self) -> Dict:
        """Get a comprehensive summary of the battle state"""
        return {
            "turn_count": self.turn_count,
            "current_pokemon": {
                "ally": {
                    "name": self.my_pokemon.name,
                    "hp": f"{self.my_pokemon.current_hp}/{self.my_pokemon.calculate_hp()}",
                    "types": self.my_pokemon.types
                },
                "opponent": {
                    "name": self.opponent_pokemon.name,
                    "hp": f"{self.opponent_pokemon.current_hp}/{self.opponent_pokemon.calculate_hp()}",
                    "types": self.opponent_pokemon.types
                }
            },
            "weather": {
                "type": self.weather.weather_type.value if self.weather else "none",
                "turns_remaining": self.weather.turns_remaining if self.weather else 0
            },
            "screens": [
                {
                    "effect": screen.effect_name,
                    "side": screen.affects_side,
                    "turns_remaining": screen.turns_remaining
                } for screen in self.screens
            ],
            "seen_opponent_moves": list(self.seen_opponent_moves),
            "ally_pokemon_used": len(self.ally_pokemon_history) + 1,
            "opponent_pokemon_used": len(self.opponent_pokemon_history) + 1,
            "is_my_turn": self.is_my_turn
        }

    def get_opponent_move_pattern(self) -> Dict:
        """Analyze opponent's move usage patterns"""
        if not self.opponent_move_history:
            return {"most_used": None, "recent_moves": [], "move_frequency": {}}
        
        # Count move frequency
        move_counts = {}
        for move_name, _, _ in self.opponent_move_history:
            move_counts[move_name] = move_counts.get(move_name, 0) + 1
        
        # Get most used move
        most_used = max(move_counts.items(), key=lambda x: x[1]) if move_counts else None
        
        # Get recent moves (last 5)
        recent_moves = [move[0] for move in self.opponent_move_history[-5:]]
        
        return {
            "most_used": most_used[0] if most_used else None,
            "recent_moves": recent_moves,
            "move_frequency": move_counts,
            "total_moves_seen": len(self.seen_opponent_moves),
            "total_moves_used": len(self.opponent_move_history)
        }

    def has_screen_active(self, effect_name: str, side: str) -> bool:
        """Check if a specific screen effect is active"""
        return any(screen.effect_name == effect_name and screen.affects_side == side 
                  for screen in self.screens)

    def get_weather_info(self) -> Dict:
        """Get current weather information"""
        if not self.weather:
            return {"type": "none", "turns_remaining": 0, "is_permanent": False}
        
        return {
            "type": self.weather.weather_type.value,
            "turns_remaining": self.weather.turns_remaining,
            "is_permanent": self.weather.is_permanent
        }