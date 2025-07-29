import pokebase as pb
from functools import lru_cache

@lru_cache(maxsize=128)
def get_pokemon_data(name):
    return pb.pokemon(name.lower())

@lru_cache(maxsize=128)
def get_move_data(name):
    return pb.move(name.lower())