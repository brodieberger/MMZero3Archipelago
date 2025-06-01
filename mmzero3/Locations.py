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


# Define disk IDs per level
derelict_ship       = [7, 24, 37, 50, 101, 111, 133, 140, 156, 158]
aegis_volcano       = [8, 26, 47, 72, 73, 102, 114, 141, 146, 152]
oceanic_highway     = [5, 9, 49, 59, 75, 79, 113, 159, 160, 161]
old_residential     = [1, 13, 28, 39, 48, 67, 74, 112, 135, 145]
weapons_factory     = [12, 52, 53, 84, 93, 100, 104, 115, 131, 147]
missile_factory     = [21, 30, 55, 57, 90, 98, 117, 127, 138, 139]
forest_of_anatre    = [2, 14, 40, 63, 71, 76, 108, 119, 134, 157]
ice_base            = [15, 32, 35, 66, 68, 109, 120, 128, 132, 136]
twilight_desert     = [22, 31, 65, 85, 89, 91, 105, 118, 153, 154]
area_x2             = [34, 42, 61, 62, 69, 70, 77, 110, 121, 137]
energy_facility     = [4, 56, 64, 78, 82, 95, 124, 149, 150, 155]
giant_elevator      = [27, 41, 45, 54, 80, 88, 122, 129, 144, 148]
snowy_plains        = [3, 25, 29, 46, 60, 86, 103, 123, 130, 162]
sunken_library      = [10, 16, 17, 18, 33, 43, 51, 94, 96, 125]
sub_arcadia         = [6, 36, 38, 81, 83, 87, 142, 143, 163, 180]
abandoned_lab       = [11, 19, 20, 97, 126, 151, 164, 177, 178, 179]
filler_stage        = []

# Map regions to their disk ID lists
region_to_disks = {
    "Derelict Spacecraft": derelict_ship,
    "Aegis Volcano Base": aegis_volcano,
    "Old Residential": old_residential,
    "Oceanic Highway Ruins": oceanic_highway,
    "Weapons Repair Factory": weapons_factory,

    "Missile Factory": missile_factory,
    
    "Forest of Anatre": forest_of_anatre,
    "Frontline Ice Base": ice_base,
    "Twilight Desert": twilight_desert,
    
    "Area X-2": area_x2,

    "Energy Facility": energy_facility,
    "Snowy Plains": snowy_plains,
    "Sunken Library": sunken_library,
    "Giant Elevator": giant_elevator,

    "Sub Arcadia": sub_arcadia,
    "Abandoned Research Laboratory": abandoned_lab,

    "Filler Stage": filler_stage,
}

# Stage names as they appear in game order
stage_names = [
    "Derelict Spacecraft", "Aegis Volcano Base", "Oceanic Highway Ruins",
    "Weapons Repair Factory", "Old Residential", "Missile Factory",
    "Twilight Desert", "Frontline Ice Base", "Forest of Anatre",
    "Area X-2", "Energy Facility", "Snowy Plains",
    "Sunken Library", "Giant Elevator"
]


location_data_table: Dict[str, MMZero3LocationData] = {
    
    "Get Z Saber (Start Game)": MMZero3LocationData(
        region="Derelict Spacecraft",
        locked_item="Z Saber",
        address=999,
    ),

    **{
        f"Complete {stage}": MMZero3LocationData(
            region=f"{stage}",
            address=180 + idx + 1,
        )
        for idx, stage in enumerate(stage_names)
    },

    "Complete Sub Arcadia": MMZero3LocationData(
        region="Sub Arcadia",
        locked_item="Boss Key",
        address=195,
    ),

    "Complete Abandoned Research Laboratory": MMZero3LocationData(
        region="Abandoned Research Laboratory",
        locked_item="Victory",
        address=196,
    ),
}

for region, disk_ids in region_to_disks.items():
    for disk_id in disk_ids:
        name = f"Get Secret Disk {disk_id}"
        location_data_table[name] = MMZero3LocationData(region=region, address=disk_id)

'''
Exclude these items. They are all of the files that can be found in the Hub area
These are excluded to due issues with the memory manipulation I am using.
exclude = [23, 44, 58, 92, 99, 106, 107, 116, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176]
'''

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
