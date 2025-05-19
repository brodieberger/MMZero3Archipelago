from typing import List, Dict, Any

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from .Items import MMZero3Item, item_data_table, item_table
from .Locations import MMZero3Location, location_data_table, location_table, locked_locations
from .Options import MMZero3Options
from .Regions import region_data_table

class MMZero3WebWorld(WebWorld):
    theme = "ice"
    bug_report_page = "https://github.com/brodieberger/ZeroArchipelago/"


class MMZero3World(World):
    """
    Play as Zero, kill the robots and save the day
    """

    game = "Mega Man Zero 3"

    item_name_to_id = item_table
    location_name_to_id = location_table

    web = MMZero3WebWorld()
    options_dataclass = MMZero3Options
    options: MMZero3Options

    def create_item(self, name: str) -> MMZero3Item:
        return MMZero3Item(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[MMZero3Item] = []
        # Exclude locked items from the item pool
        locked_item_names = {data.locked_item for data in locked_locations.values() if data.locked_item}
        for name, item in item_data_table.items():
            if item.code and item.can_create(self) and name not in locked_item_names:
                item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

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
        return "100 Energy Crystals"
    
    def set_rules(self) -> None:
        set_rule(self.multiworld.get_entrance("To Boss Stage", self.player),
                    lambda state: state.has("Boss Key", self.player))
        
        set_rule(self.multiworld.get_location("Kill Omega", self.player),
                    lambda state: state.can_reach_region("Boss Stage", self.player))
        
        # Completion condition
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)
        
        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")