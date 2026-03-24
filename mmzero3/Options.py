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
    range_end = 180
    default = 80

class EasyExSkill(Toggle):
    """Rewards player with EX-Skill at the end of a level regardless of ranking. Currently recommended, as otherwise EXSkills are missable unless you load an earlier save or use savestates. This will be fixed later."""
    display_name = "Always reward EX-Skill"

class RewardNotification(Toggle):
    """Will notify the player of earned Archipelago items. Currently the text is very slow and screen obscuring, so not recommended."""
    display_name = "In-game reward notification"

@dataclass
class MMZero3Options(PerGameCommonOptions):
    goal: Goal
    required_secret_disks: RequiredSecretDisks
    easy_ex_skill: EasyExSkill
    reward_notification: RewardNotification