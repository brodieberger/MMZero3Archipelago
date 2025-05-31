from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions

class Goal(Choice):
    """
    Default: Beat the final boss with enough data disks collected to win.
    Vanilla: Beat the final boss to win.
    Disk Hunt: Collect all data disks to win.
    """
    display_name = "Goal"
    option_default = 0
    option_vanilla = 1
    option_disk_hunt = 2
    default = 0

@dataclass
class MMZero3Options(PerGameCommonOptions):
    goal: Goal