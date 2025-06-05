from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions

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
    range_end = 160
    default = 80

class EasyExSkill(Toggle):
    """Give the player an S-Rank at the end of the level. Always gives EX-Skill. Note this can also make certain bosses harder, so don't consider this an easy mode!"""
    display_name = "Always have S-Rank"

@dataclass
class MMZero3Options(PerGameCommonOptions):
    goal: Goal
    required_secret_disks: RequiredSecretDisks
    easy_ex_skill: EasyExSkill