from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, StartInventoryPool

class Goal(Choice):
    """
    Vanilla: Beat the final boss to win.
    Disk Hunt: Collect all data disks to win.
    """
    display_name = "Goal"
    option_vanilla = 0
    option_disk_hunt = 1
    default = 0

@dataclass
class MMZero3Options(PerGameCommonOptions):
    goal: Goal