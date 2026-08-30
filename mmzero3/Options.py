from dataclasses import dataclass
from Options import Range, Toggle, OptionSet, DeathLink, PerGameCommonOptions


class RequiredSecretDisks(Range):
    """Number of Secret Disks required to unlock the final stage.

    The Abandoned Research Laboratory opens once every other stage has been cleared and
    you are holding this many disks. Clearing it completes the game.
    Setting it above 170 is not recommended, as it will place a lot of useful items in the final stage, which
    at that point, the game is basically completed.
    """
    display_name = "Required Secret Disks"
    range_start = 0
    range_end = 180
    default = 120

class EasyExSkill(Toggle):
    """Rewards player with EX-Skill at the end of a level regardless of ranking."""
    display_name = "Always reward EX-Skill"
    

class StartingWeapons(OptionSet):
    """Which weapons Zero starts with.
    The weapon will still start at its first tier, and progressive unlocks (charge attacks and saber combos) will need to be unlocked.
    If this is left empty, one random weapon is granted instead.
    
    Valid Keys: {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}"""
    display_name = "Starting Weapons"
    valid_keys = {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}
    default = frozenset({"Buster", "Z-Saber"})

@dataclass
class MMZero3Options(PerGameCommonOptions):
    required_secret_disks: RequiredSecretDisks
    easy_ex_skill: EasyExSkill
    starting_weapons: StartingWeapons
    death_link: DeathLink