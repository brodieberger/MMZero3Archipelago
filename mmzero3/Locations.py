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
        for i in range(1, 181)
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
