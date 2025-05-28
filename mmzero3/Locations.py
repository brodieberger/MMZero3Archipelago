from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import MMZero3World


class MMZero3Location(Location):
    game = "Mega Man Zero 3"


class MMZero3LocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["MMZero3World"], bool] = lambda world: True
    locked_item: Optional[str] = None


# Exclude these items. They are all of the files that can be found in the Hub area
# These are excluded to due issues with the memory manipulation I am using, hopefully only a temp fix.
exclude = [23, 44, 58, 92, 99, 106, 107, 116, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176]
location_data_table: Dict[str, MMZero3LocationData] = {
    "Z Saber": MMZero3LocationData(
        region="Opening Stage",
        locked_item="Z Saber",
        address=999,
    ),
    **{
        f"Get Secret Disk {i}": MMZero3LocationData(
            region="Level 1",
            address=i,
        )
        for i in range(1, 181) if i not in exclude
    },
    "Kill Boss 1": MMZero3LocationData(
        region="Level 1",
        address=181,
    ),
    "Kill Omega": MMZero3LocationData(
        region="Boss Stage",
        locked_item="Victory",
        address=182,
    ),
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
