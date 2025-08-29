from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from pokedata.fetcher import get_pokemon_data, get_move_data
import pokebase as pb


@dataclass
class PokemonStats:
    """Represents the base stats of a Pokemon"""
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int
    
    @property
    def total(self) -> int:
        """Calculate total base stat"""
        return self.hp + self.attack + self.defense + self.special_attack + self.special_defense + self.speed


@dataclass
class Move:
    """Represents a Pokemon move"""
    name: str
    type: str
    power: Optional[int]
    accuracy: Optional[int]
    pp: int
    damage_class: str  # physical, special, or status
    effect: Optional[str] = None
    priority: int = 0
    
    @classmethod
    def from_api(cls, move_name: str) -> 'Move':
        """Create a Move object from PokeAPI data"""
        try:
            move_data = get_move_data(move_name)
            return cls(
                name=move_data.name.title(),
                type=move_data.type.name.title(),
                power=move_data.power,
                accuracy=move_data.accuracy,
                pp=move_data.pp,
                damage_class=move_data.damage_class.name,
                effect=move_data.effect_entries[0].effect if move_data.effect_entries else None,
                priority=move_data.priority
            )
        except Exception as e:
            print(f"Error fetching move data for {move_name}: {e}")
            # Return a basic move with unknown data
            return cls(
                name=move_name.title(),
                type="Normal",
                power=None,
                accuracy=None,
                pp=1,
                damage_class="status"
            )


@dataclass
class Ability:
    """Represents a Pokemon ability"""
    name: str
    effect: Optional[str] = None
    is_hidden: bool = False
    
    @classmethod
    def from_api(cls, ability_data: Any, is_hidden: bool = False) -> 'Ability':
        """Create an Ability object from PokeAPI data"""
        try:
            effect = None
            if hasattr(ability_data, 'effect_entries') and ability_data.effect_entries:
                effect = ability_data.effect_entries[0].effect
            
            return cls(
                name=ability_data.name.title(),
                effect=effect,
                is_hidden=is_hidden
            )
        except Exception:
            return cls(
                name=ability_data.name.title() if hasattr(ability_data, 'name') else "Unknown",
                is_hidden=is_hidden
            )


@dataclass
class Pokemon:
    """Comprehensive Pokemon class with all essential attributes"""
    name: str
    types: List[str]
    stats: PokemonStats
    moves: List[Move] = field(default_factory=list)
    abilities: List[Ability] = field(default_factory=list)
    level: int = 50
    nature: Optional[str] = None
    item: Optional[str] = None
    
    # Physical characteristics
    height: Optional[float] = None  # in meters
    weight: Optional[float] = None  # in kg
    
    # Battle-related attributes
    current_hp: Optional[int] = None
    status_condition: Optional[str] = None  # paralyzed, burned, frozen, etc.
    
    # Additional metadata
    species_id: Optional[int] = None
    base_experience: Optional[int] = None
    
    def __post_init__(self):
        """Initialize current HP if not set"""
        if self.current_hp is None:
            self.current_hp = self.calculate_hp()
    
    @classmethod
    def from_api(cls, pokemon_name: str, level: int = 50, move_names: Optional[List[str]] = None) -> 'Pokemon':
        """
        Create a Pokemon object by fetching data from PokeAPI
        
        Args:
            pokemon_name: Name of the Pokemon
            level: Level of the Pokemon (default 50)
            move_names: Optional list of specific moves to give the Pokemon
        """
        try:
            pokemon_data = get_pokemon_data(pokemon_name)
            
            # Extract types
            types = [ptype.type.name.title() for ptype in pokemon_data.types]
            
            # Extract base stats
            stat_dict = {}
            for stat in pokemon_data.stats:
                stat_name = stat.stat.name.replace('-', '_')
                stat_dict[stat_name] = stat.base_stat
            
            stats = PokemonStats(
                hp=stat_dict.get('hp', 0),
                attack=stat_dict.get('attack', 0),
                defense=stat_dict.get('defense', 0),
                special_attack=stat_dict.get('special_attack', 0),
                special_defense=stat_dict.get('special_defense', 0),
                speed=stat_dict.get('speed', 0)
            )
            
            # Extract abilities
            abilities = []
            for ability_slot in pokemon_data.abilities:
                try:
                    ability_data = pb.ability(ability_slot.ability.name)
                    ability = Ability.from_api(ability_data, ability_slot.is_hidden)
                    abilities.append(ability)
                except Exception:
                    # Fallback if we can't fetch ability details
                    ability = Ability(
                        name=ability_slot.ability.name.title(),
                        is_hidden=ability_slot.is_hidden
                    )
                    abilities.append(ability)
            
            # Handle moves
            moves = []
            if move_names:
                # Use provided move names
                for move_name in move_names:
                    move = Move.from_api(move_name)
                    moves.append(move)
            else:
                # Get some default moves the Pokemon can learn
                available_moves = [move.move.name for move in pokemon_data.moves[:4]]
                for move_name in available_moves:
                    move = Move.from_api(move_name)
                    moves.append(move)
            
            return cls(
                name=pokemon_data.name.title(),
                types=types,
                stats=stats,
                moves=moves,
                abilities=abilities,
                level=level,
                height=pokemon_data.height / 10.0,  # Convert from decimeters to meters
                weight=pokemon_data.weight / 10.0,  # Convert from hectograms to kg
                species_id=pokemon_data.id,
                base_experience=pokemon_data.base_experience
            )
            
        except Exception as e:
            print(f"Error creating Pokemon from API for {pokemon_name}: {e}")
            # Return a basic Pokemon with minimal data
            return cls(
                name=pokemon_name.title(),
                types=["Normal"],
                stats=PokemonStats(50, 50, 50, 50, 50, 50),
                level=level
            )
    
    @classmethod
    def from_dict(cls, pokemon_dict: Dict) -> 'Pokemon':
        """Create a Pokemon from a dictionary (for compatibility with existing code)"""
        name = pokemon_dict.get('name', 'Unknown')
        types = pokemon_dict.get('types', ['Normal'])
        
        # Try to fetch full data if we only have basic info
        if len(pokemon_dict) <= 3:  # Only basic info provided
            return cls.from_api(name)
        
        # Build from provided data
        stats_data = pokemon_dict.get('stats', {})
        stats = PokemonStats(
            hp=stats_data.get('hp', 50),
            attack=stats_data.get('attack', 50),
            defense=stats_data.get('defense', 50),
            special_attack=stats_data.get('special_attack', 50),
            special_defense=stats_data.get('special_defense', 50),
            speed=stats_data.get('speed', 50)
        )
        
        # Handle moves
        moves = []
        for move_data in pokemon_dict.get('moves', []):
            if isinstance(move_data, dict):
                move = Move(
                    name=move_data.get('name', 'Tackle'),
                    type=move_data.get('type', 'Normal'),
                    power=move_data.get('power'),
                    accuracy=move_data.get('accuracy'),
                    pp=move_data.get('pp', 1),
                    damage_class=move_data.get('damage_class', 'physical')
                )
                moves.append(move)
        
        return cls(
            name=name,
            types=types,
            stats=stats,
            moves=moves,
            level=pokemon_dict.get('level', 50)
        )
    
    def calculate_hp(self) -> int:
        """Calculate actual HP based on base stat and level"""
        # Simplified HP calculation (actual formula is more complex)
        return int(((2 * self.stats.hp + 31) * self.level) / 100) + self.level + 10
    
    def calculate_stat(self, base_stat: int) -> int:
        """Calculate actual stat based on base stat and level"""
        # Simplified stat calculation
        return int(((2 * base_stat + 31) * self.level) / 100) + 5
    
    @property
    def actual_stats(self) -> Dict[str, int]:
        """Get the actual stats at the current level"""
        return {
            'hp': self.calculate_hp(),
            'attack': self.calculate_stat(self.stats.attack),
            'defense': self.calculate_stat(self.stats.defense),
            'special_attack': self.calculate_stat(self.stats.special_attack),
            'special_defense': self.calculate_stat(self.stats.special_defense),
            'speed': self.calculate_stat(self.stats.speed)
        }
    
    def is_fainted(self) -> bool:
        """Check if the Pokemon has fainted"""
        return self.current_hp <= 0
    
    def take_damage(self, damage: int) -> int:
        """Apply damage to the Pokemon and return actual damage taken"""
        actual_damage = min(damage, self.current_hp)
        self.current_hp -= actual_damage
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Heal the Pokemon and return actual healing done"""
        max_hp = self.calculate_hp()
        actual_healing = min(amount, max_hp - self.current_hp)
        self.current_hp += actual_healing
        return actual_healing
    
    def add_move(self, move: Move) -> bool:
        """Add a move to the Pokemon (max 4 moves)"""
        if len(self.moves) < 4:
            self.moves.append(move)
            return True
        return False
    
    def get_move_by_name(self, move_name: str) -> Optional[Move]:
        """Get a move by name"""
        for move in self.moves:
            if move.name.lower() == move_name.lower():
                return move
        return None
    
    def to_dict(self) -> Dict:
        """Convert Pokemon to dictionary format (for compatibility)"""
        return {
            'name': self.name,
            'types': self.types,
            'level': self.level,
            'stats': {
                'hp': self.stats.hp,
                'attack': self.stats.attack,
                'defense': self.stats.defense,
                'special_attack': self.stats.special_attack,
                'special_defense': self.stats.special_defense,
                'speed': self.stats.speed
            },
            'moves': [
                {
                    'name': move.name,
                    'type': move.type,
                    'power': move.power,
                    'accuracy': move.accuracy,
                    'pp': move.pp,
                    'damage_class': move.damage_class
                }
                for move in self.moves
            ],
            'abilities': [ability.name for ability in self.abilities],
            'current_hp': self.current_hp,
            'height': self.height,
            'weight': self.weight
        }
    
    def __str__(self) -> str:
        """String representation of the Pokemon"""
        type_str = "/".join(self.types)
        ability_str = ", ".join([ability.name for ability in self.abilities])
        return f"{self.name} (Lv.{self.level}) - {type_str} - HP: {self.current_hp}/{self.calculate_hp()} - Abilities: {ability_str}"
    
    def __repr__(self) -> str:
        return f"Pokemon(name='{self.name}', types={self.types}, level={self.level})"
