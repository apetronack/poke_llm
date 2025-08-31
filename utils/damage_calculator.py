from utils.type_effectiveness import get_multiplier

# Damage calculator for physical moves
def calculate_physical_damage(attacker, defender, move, random_multiplier = 1.0, battle_conditions=None):
    """
    Calculate damage for physical moves.
    """
    if move.power is None or move.power == 0:
        return 0
    MAX_RANDOM_MULTIPLIER = 1
    MIN_RANDOM_MULTIPLIER = 0.85

    # Check that random multiplier within valid range
    if random_multiplier < MIN_RANDOM_MULTIPLIER or random_multiplier > MAX_RANDOM_MULTIPLIER:
        raise ValueError(f"Random multiplier must be between {MIN_RANDOM_MULTIPLIER} and {MAX_RANDOM_MULTIPLIER}")

    # Default Values
    level = 1
    power = 1
    attacker_stat = 1
    defender_stat = 1
    burn_multiplier = 1
    screen_multiplier = 1
    num_targets = 1
    weather_multiplier = 1
    stockpile_multiplier = 1
    flash_fire_multiplier = 1
    crit_multiplier = 1
    double_damage_multiplier = 1
    charge_multiplier = 1
    helping_hand_multiplier = 1
    STAB_multiplier = 1
    type_effectiveness_multiplier = 1

    # Determine value of all multipliers
    if hasattr(attacker, 'level'):
        level = attacker.level
    if hasattr(move, 'power'):
        power = move.power # 0 power moves already considered above
    if hasattr(attacker, 'attack'):
        attacker_stat = attacker.attack
    if hasattr(defender, 'defense'):
        defender_stat = defender.defense
    if hasattr(attacker, 'burn'):
        # Check for guts ability - if user has guts, burn multiplier not applied
        if hasattr(attacker, 'ability_names') and "guts" not in attacker.ability_names:
            burn_multiplier = 0.5
        elif hasattr(attacker, 'abilities') and "guts" not in attacker.abilities:
            burn_multiplier = 0.5
    
    # TODO: Add battle conditions as input, adjust modifiers accordingly
    # if hasattr(defender, 'screens'):
    #     screen_multiplier = 0.5 if "reflect" in defender.screens else 1
    # if hasattr(move, 'num_targets'):
    #     num_targets = move.num_targets
    # if hasattr(defender, 'weather'):
    #     weather_multiplier = 1.3 if defender.weather == "sunny" else 1
    # if hasattr(attacker, 'stockpile'):
    #     stockpile_multiplier = 1 + (0.5 * attacker.stockpile)
    # if hasattr(attacker, 'flash_fire'):
    #     flash_fire_multiplier = 1.5 if attacker.flash_fire else 1
    # if hasattr(attacker, 'critical_hit'):
    #     crit_multiplier = 1.5 if attacker.critical_hit else 1
    # if hasattr(attacker, 'double_damage'):
    #     double_damage_multiplier = 2 if attacker.double_damage else 1
    # if hasattr(attacker, 'charge'):
    #     charge_multiplier = 1.5 if attacker.charge else 1
    # if hasattr(attacker, 'helping_hand'):
    #     helping_hand_multiplier = 1.5 if attacker.helping_hand else 1
    if hasattr(move, 'type'):
        STAB_multiplier = 1.5 if move.type in attacker.types else 1
    if hasattr(move, 'type'):
        type_effectiveness_multiplier = get_multiplier(move.type, defender.types)
    max_random_multiplier = 1
    min_random_multiplier = 0.85

    # Calculate base damage
    base_damage = ((((2*level / 5 + 2) * power * attacker_stat / defender_stat) / 50) * burn_multiplier * screen_multiplier * num_targets * weather_multiplier * flash_fire_multiplier + 2) * stockpile_multiplier * crit_multiplier * double_damage_multiplier * charge_multiplier * helping_hand_multiplier * STAB_multiplier * type_effectiveness_multiplier * random_multiplier
    
    return max(0, int(base_damage))

# Damage calculator for special moves
def calculate_special_damage(attacker, defender, move, random_multiplier = 1.0, battle_conditions=None):
    """
    Calculate damage for special moves.
    """
    if move.power is None or move.power == 0:
        return 0
    MAX_RANDOM_MULTIPLIER = 1
    MIN_RANDOM_MULTIPLIER = 0.85

    # Check that random multiplier within valid range
    if random_multiplier < MIN_RANDOM_MULTIPLIER or random_multiplier > MAX_RANDOM_MULTIPLIER:
        raise ValueError(f"Random multiplier must be between {MIN_RANDOM_MULTIPLIER} and {MAX_RANDOM_MULTIPLIER}")

    # Default Values
    level = 1
    power = 1
    attacker_stat = 1
    defender_stat = 1
    burn_multiplier = 1
    screen_multiplier = 1
    num_targets = 1
    weather_multiplier = 1
    stockpile_multiplier = 1
    flash_fire_multiplier = 1
    crit_multiplier = 1
    double_damage_multiplier = 1
    charge_multiplier = 1
    helping_hand_multiplier = 1
    STAB_multiplier = 1
    type_effectiveness_multiplier = 1

    # Determine value of all multipliers
    if hasattr(attacker, 'level'):
        level = attacker.level
    if hasattr(move, 'power'):
        power = move.power # 0 power moves already considered above
    if hasattr(attacker, 'special_attack'):
        attacker_stat = attacker.special_attack
    if hasattr(defender, 'special_defense'):
        defender_stat = defender.special_defense

    # TODO: Add battle conditions as input, adjust modifiers accordingly
    # if hasattr(defender, 'screens'):
    #     screen_multiplier = 0.5 if "light_screen" in defender.screens else 1
    # if hasattr(move, 'num_targets'):
    #     num_targets = move.num_targets
    # if hasattr(defender, 'weather'):
    #     weather_multiplier = 1.3 if defender.weather == "sunny" else 1
    # if hasattr(attacker, 'stockpile'):
    #     stockpile_multiplier = 1 + (0.5 * attacker.stockpile)
    # if hasattr(attacker, 'flash_fire'):
    #     flash_fire_multiplier = 1.5 if attacker.flash_fire else 1
    # if hasattr(attacker, 'critical_hit'):
    #     crit_multiplier = 1.5 if attacker.critical_hit else 1
    # if hasattr(attacker, 'double_damage'):
    #     double_damage_multiplier = 2 if attacker.double_damage else 1
    # if hasattr(attacker, 'charge'):
    #     charge_multiplier = 1.5 if attacker.charge else 1
    # if hasattr(attacker, 'helping_hand'):
    #     helping_hand_multiplier = 1.5 if attacker.helping_hand else 1
    if hasattr(move, 'type'):
        STAB_multiplier = 1.5 if move.type in attacker.types else 1
    if hasattr(move, 'type'):
        type_effectiveness_multiplier = get_multiplier(move.type, defender.types)

    # Calculate base damage
    base_damage = ((((2*level / 5 + 2) * power * attacker_stat / defender_stat) / 50) * burn_multiplier * screen_multiplier * num_targets * weather_multiplier * flash_fire_multiplier + 2) * stockpile_multiplier * crit_multiplier * double_damage_multiplier * charge_multiplier * helping_hand_multiplier * STAB_multiplier * type_effectiveness_multiplier * random_multiplier

    return max(0, int(base_damage))