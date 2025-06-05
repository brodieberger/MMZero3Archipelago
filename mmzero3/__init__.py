import math
from typing import List, Dict, Any, ClassVar

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from .Items import MMZero3Item, item_data_table, item_table
from .Locations import MMZero3Location, location_data_table, location_table, locked_locations
from .Options import MMZero3Options
from .Regions import region_data_table
from .Rom import MMZero3ProcedurePatch, MMZero3Settings
from .Client import MMZero3Client

import pkgutil
import hashlib
import os
from worlds.Files import APProcedurePatch

class MMZero3WebWorld(WebWorld):
    theme = "ice"
    bug_report_page = "https://github.com/brodieberger/ZeroArchipelago/"


class MMZero3World(World):
    """
    Play as Zero, kill the robots and save the day
    """

    game = "Mega Man Zero 3"
    web = MMZero3WebWorld()
    
    settings_key = "MMZero3_settings"
    settings: ClassVar[Rom.MMZero3Settings]

    options_dataclass = MMZero3Options
    options: MMZero3Options

    item_name_to_id = item_table
    location_name_to_id = location_table

    def create_item(self, name: str) -> MMZero3Item:
        return MMZero3Item(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[MMZero3Item] = []
        
        # Exclude locked items from the item pool
        locked_item_names = {data.locked_item for data in locked_locations.values() if data.locked_item}
        
        for name, item in item_data_table.items():
            if item.code and item.can_create(self) and name not in locked_item_names:
                item_pool.append(self.create_item(name))

        # Add the items to the pool
        self.multiworld.itempool += item_pool

        # Calculate how many filler items are needed
        total_locations = len([loc for loc in location_data_table.values() if loc.can_create(self)])
        total_items = len(item_pool) + len(locked_item_names)
        filler_count = total_locations - total_items

        # Fill extra locations with filler items if needed
        for _ in range(filler_count):
            self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self)
            }, MMZero3Location)
            region.add_exits({target: f"To {target}" for target in region_data_table[region_name].connecting_regions})

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.get_location(location_name).place_locked_item(locked_item)

    def get_filler_item_name(self) -> str:
        # TODO: implement energy crystal
        return "100 Energy Crystals (Unimplemented)"
    
    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "required_secret_disks": self.options.required_secret_disks.value,
            "goal": self.options.goal.value,
            "easy_ex_skill": self.options.easy_ex_skill.value
        }

    def set_rules(self) -> None:
        set_rule(self.multiworld.get_entrance("To Abandoned Research Laboratory", self.player),
                    lambda state: state.has("Sub Arcadia Cleared", self.player))
        
        set_rule(
            self.multiworld.get_entrance("To Missile Factory", self.player),
            lambda state: all(state.has(item, self.player) for item in [
                "Aegis Volcano Base Cleared",
                "Oceanic Highway Ruins Cleared",
                "Weapons Repair Factory Cleared",
                "Old Residential Cleared",
            ])
        )

        set_rule(
            self.multiworld.get_entrance("To Area X-2", self.player),
            lambda state: all(state.has(item, self.player) for item in [
                "Forest of Anatre Cleared",
                "Frontline Ice Base Cleared",
                "Twilight Desert Cleared",
            ])
        )

        set_rule(
            self.multiworld.get_entrance("To Sub Arcadia", self.player),
            lambda state: all(state.has(item, self.player) for item in [
                "Giant Elevator Cleared",
                "Sunken Library Cleared",
                "Snowy Plains Cleared",
                "Energy Facility Cleared"
            ])
        )
                        
        set_rule(self.multiworld.get_location("Complete Abandoned Research Laboratory", self.player),
                    lambda state: state.can_reach_region("Abandoned Research Laboratory", self.player))

        # Completion condition
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        
    def generate_output(self, output_directory: str) -> None:
        patch = Rom.MMZero3ProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("mmz3-ap.bsdiff4", pkgutil.get_data(__name__, "mmz3-ap.bsdiff4"))
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
