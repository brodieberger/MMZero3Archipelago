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

item_data_table: Dict[str, MMZero3ItemData] = {
    "Z Saber": MMZero3ItemData(
        code=1,
        type=ItemClassification.progression,
    ),
    "Cyber Elf 1": MMZero3ItemData(
        code=2,
        type=ItemClassification.useful,
    ),
    "Cyber Elf 2": MMZero3ItemData(
        code=3,
        type=ItemClassification.useful,
    ),
    "Cyber Elf 3": MMZero3ItemData(
        code=4,
        type=ItemClassification.useful,
    ),
    "Cyber Elf 4": MMZero3ItemData(
        code=5,
        type=ItemClassification.useful,
    ),
    "Boss Key": MMZero3ItemData(
        code=6,
        type=ItemClassification.progression,
    ),
    "Victory": MMZero3ItemData(
        code=7,
        type=ItemClassification.progression,
    ),
    "100 Energy Crystals": MMZero3ItemData(
        code=8,
        can_create=lambda world: False  # Only created from `get_filler_item_name`.
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
