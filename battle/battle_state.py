from typing import Union, Dict, List
from pokemon import Pokemon

class BattleState:
    def __init__(self, my_pokemon: Union[Pokemon, Dict], opponent_pokemon: Union[Pokemon, Dict], 
                 my_moves=None, opponent_moves=None):
        """
        Initialize BattleState with Pokemon objects or dictionaries (for backward compatibility).
        
        Args:
            my_pokemon: Pokemon object or dictionary
            opponent_pokemon: Pokemon object or dictionary  
            my_moves: Optional list of moves (ignored if Pokemon objects are used)
            opponent_moves: Optional list of moves (ignored if Pokemon objects are used)
        """
        # Handle Pokemon objects vs dictionaries
        if isinstance(my_pokemon, Pokemon):
            self.my_pokemon = my_pokemon
            self.my_moves = my_pokemon.moves
        else:
            # Backward compatibility with dictionary format
            self.my_pokemon = my_pokemon
            self.my_moves = my_moves or []
            
        if isinstance(opponent_pokemon, Pokemon):
            self.opponent_pokemon = opponent_pokemon
            self.opponent_moves = opponent_pokemon.moves
        else:
            # Backward compatibility with dictionary format
            self.opponent_pokemon = opponent_pokemon
            self.opponent_moves = opponent_moves or []
    
    def get_my_pokemon_types(self) -> List[str]:
        """Get my Pokemon's types"""
        if isinstance(self.my_pokemon, Pokemon):
            return self.my_pokemon.types
        else:
            return self.my_pokemon.get('types', [])
    
    def get_opponent_pokemon_types(self) -> List[str]:
        """Get opponent Pokemon's types"""
        if isinstance(self.opponent_pokemon, Pokemon):
            return self.opponent_pokemon.types
        else:
            return self.opponent_pokemon.get('types', [])
    
    def get_my_pokemon_name(self) -> str:
        """Get my Pokemon's name"""
        if isinstance(self.my_pokemon, Pokemon):
            return self.my_pokemon.name
        else:
            return self.my_pokemon.get('name', 'Unknown')
    
    def get_opponent_pokemon_name(self) -> str:
        """Get opponent Pokemon's name"""
        if isinstance(self.opponent_pokemon, Pokemon):
            return self.opponent_pokemon.name
        else:
            return self.opponent_pokemon.get('name', 'Unknown')