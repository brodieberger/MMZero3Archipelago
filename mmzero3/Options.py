from dataclasses import dataclass
from Options import Choice, Range, Toggle, OptionSet, PerGameCommonOptions


class Goal(Choice):
    """
    Default: Beat the final boss with enough data disks collected to win.
    Vanilla: Beat the final boss to win.
    """
    display_name = "Goal"
    option_default = 0
    option_vanilla = 1
    default = 0

class RequiredSecretDisks(Range):
    """Number of Secret Disks required to complete the game"""
    display_name = "Required Secret Disks"
    range_start = 0
    range_end = 180
    default = 80

class EasyExSkill(Toggle):
    """Rewards player with EX-Skill at the end of a level regardless of ranking. Currently recommended, as otherwise EXSkills are missable unless you load an earlier save or use savestates. This will be fixed later."""
    display_name = "Always reward EX-Skill"
    

class RewardNotification(Toggle):
    """Will notify the player of earned Archipelago items. Currently the text is very slow and screen obscuring, so not recommended."""
    display_name = "In-game reward notification"

class RandomizeWeapons(Toggle):
    """When enabled, the four weapons (Buster, Z-Saber, Recoil Rod, Shield Boomerang) are added to the item pool and must be found before they can be used."""
    display_name = "Randomize Weapons"

class StartingWeapons(OptionSet):
    """Which weapons Zero starts with when Randomize Weapons is enabled. Selected weapons are given at the start and will not be placed in the item pool."""
    display_name = "Starting Weapons"
    valid_keys = {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}
    default = frozenset()

@dataclass
class MMZero3Options(PerGameCommonOptions):
    goal: Goal
    required_secret_disks: RequiredSecretDisks
    easy_ex_skill: EasyExSkill
    reward_notification: RewardNotification
    randomize_weapons: RandomizeWeapons
    starting_weapons: StartingWeapons