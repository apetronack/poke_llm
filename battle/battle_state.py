from typing import Union, Dict, List
from pokemon import Pokemon

class BattleState:
    def __init__(self, my_pokemon: Pokemon, opponent_pokemon: Pokemon):
        """
        Initialize BattleState with Pokemon objects only.
        Args:
            my_pokemon: Pokemon object
            opponent_pokemon: Pokemon object
        """
        self.my_pokemon = my_pokemon
        self.my_moves = my_pokemon.moves
        self.opponent_pokemon = opponent_pokemon
        self.opponent_moves = opponent_pokemon.moves

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