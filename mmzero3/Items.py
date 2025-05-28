from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import MMZero3World

class MMZero3Item(Item):
    game: str = "Mega Man Zero 3"

class MMZero3ItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[["MMZero3World"], bool] = lambda world: True


# Exclude these items. They are all of the files that can be found in the Hub area
# These are excluded to due issues with the memory manipulation I am using, hopefully only a temp fix.
exclude = [23, 44, 58, 92, 99, 106, 107, 116, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176]
item_data_table: Dict[str, MMZero3ItemData] = {
    "Z Saber": MMZero3ItemData(
        code=999,
        type=ItemClassification.progression,
    ),
    **{
        f"Secret Disk {i}": MMZero3ItemData(
            code=i,
            type=ItemClassification.useful,
        )
        for i in range(1, 181) if i not in exclude
    },
    "Boss Key": MMZero3ItemData(
        code=181,
        type=ItemClassification.progression,
    ),
    "Victory": MMZero3ItemData(
        code=182,
        type=ItemClassification.progression,
    ),
    "100 Energy Crystals": MMZero3ItemData(
        code=183,
        can_create=lambda world: False  # Only created from `get_filler_item_name`.
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
