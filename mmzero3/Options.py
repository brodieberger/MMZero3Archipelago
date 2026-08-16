from dataclasses import dataclass
from Options import Range, Toggle, OptionSet, DeathLink, PerGameCommonOptions


class RequiredSecretDisks(Range):
    """Number of Secret Disks required to unlock the final stage.

    The Abandoned Research Laboratory opens once every other stage has been cleared and
    you are holding this many disks. Clearing it completes the game."""
    display_name = "Required Secret Disks"
    range_start = 0
    range_end = 180
    default = 120

class EasyExSkill(Toggle):
    """Rewards player with EX-Skill at the end of a level regardless of ranking."""
    display_name = "Always reward EX-Skill"
    

class RandomizeWeapons(Toggle):
    """When enabled, the four weapons (Buster, Z-Saber, Recoil Rod, Shield Boomerang) are added to the item pool and must be found before they can be used.

    When disabled, all four weapons are available from the start and Starting Weapons is ignored."""
    display_name = "Randomize Weapons"

class StartingWeapons(OptionSet):
    """Which weapons Zero starts with when Randomize Weapons is enabled. Selected weapons are given at the start and will not be placed in the item pool.

    Zero cannot damage anything without a weapon, so if this is left empty a single weapon is granted automatically.
    Ignored when Randomize Weapons is disabled, since every weapon is granted in that case."""
    display_name = "Starting Weapons"
    valid_keys = {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}
    default = frozenset({"Buster", "Z-Saber"})

@dataclass
class MMZero3Options(PerGameCommonOptions):
    required_secret_disks: RequiredSecretDisks
    easy_ex_skill: EasyExSkill
    randomize_weapons: RandomizeWeapons
    starting_weapons: StartingWeapons
    death_link: DeathLink