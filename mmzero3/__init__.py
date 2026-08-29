import math
from typing import List, Dict, Any, ClassVar

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from .Items import (MMZero3Item, STORY_LATE, STORY_MID, item_data_table, item_name_groups,
                    item_table, stage_access_names, stage_names, weapon_ability_level,
                    weapon_names)
from .Locations import (MMZero3Location, location_data_table, location_name_groups, location_table,
                        locked_locations)
from .Options import MMZero3Options
from .Regions import region_data_table
from .Rom import MMZero3ProcedurePatch, MMZero3Settings, write_tokens
from .Client import MMZero3Client

import pkgutil
import hashlib
import os
from worlds.Files import APProcedurePatch

class MMZero3WebWorld(WebWorld):
    theme = "ice"
    bug_report_page = "https://github.com/brodieberger/ZeroArchipelago/"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Mega Man Zero 3 Randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Stingrays110"]
    )
    tutorials = [setup_en]

class MMZero3World(World):
    """
    Play as Zero, kill the robots and save the day
    """

    game = "Mega Man Zero 3"
    web = MMZero3WebWorld()
    options_dataclass = MMZero3Options
    options: MMZero3Options
    settings_key = "MMZero3_settings"
    settings: ClassVar[MMZero3Settings]

    item_name_to_id = item_table
    location_name_to_id = location_table

    item_name_groups = item_name_groups
    location_name_groups = location_name_groups


    starting_weapons: set

    def generate_early(self) -> None:
        # Inform the Universal Tracker what the starting items are
        passthrough = None
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Mega Man Zero 3" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["Mega Man Zero 3"]

        if passthrough:
            self.starting_weapons = set(passthrough["starting_weapons"])
        else:
            self.starting_weapons = set(self.options.starting_weapons.value)

            if not self.starting_weapons:
                self.starting_weapons = {self.random.choice(weapon_names)}

        # If it is your only weapon, add another Shield Boomerang so you can actually attack.
        if self.starting_weapons == {"Shield Boomerang"}:
            self.multiworld.push_precollected(self.create_item("Progressive Shield Boomerang"))

        # Force the first stage access item to be early local
        first_stage_access = self.random.choice(stage_access_names)
        self.multiworld.local_early_items[self.player][first_stage_access] = 1

    def starting_level(self, weapon: str) -> int:
        """How far up its chain a weapon starts. 0 means the player does not own it.

        This only really exists for the progressive item lambda fucntion.
        """
        if weapon not in self.starting_weapons:
            return 0
        if self.starting_weapons == {"Shield Boomerang"}:
            return 2
        return 1

    def create_item(self, name: str) -> MMZero3Item:
        return MMZero3Item(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[MMZero3Item] = []

        locked_item_names = {data.locked_item for data in locked_locations.values() if data.locked_item}

        for name, item in item_data_table.items():
            if item.code and item.can_create(self) and name not in locked_item_names:
                item_pool.extend(self.create_item(name) for _ in range(item.count(self)))

        self.multiworld.itempool += item_pool

        # Count only the free (non-locked) locations that are actually created
        free_location_count = len([
            loc for loc in location_data_table.values()
            if loc.can_create(self) and not loc.locked_item
        ])

        filler_count = free_location_count - len(item_pool)
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
        return "100 Energy Crystals"
    
    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "required_secret_disks": self.options.required_secret_disks.value,
            "easy_ex_skill": self.options.easy_ex_skill.value,
            "starting_weapons": sorted(self.starting_weapons),
            "death_link": self.options.death_link.value,
        }

    def set_rules(self) -> None:
        def has_weapon_at(state, weapon: str, ability: str) -> bool:
            copies_needed = weapon_ability_level(weapon, ability)
            if weapon in self.starting_weapons:
                copies_needed -= 1
            return state.has(f"Progressive {weapon}", self.player, copies_needed)

        # Breaking blocks, moving platforms, and the rod jump.
        def has_rod(state):
            return has_weapon_at(state, "Recoil Rod", "Charged Rod")

        def has_mobility(state):
            return state.has("Double Jump Foot Chip", self.player) or has_rod(state)

        def has_flame(state):
            if not state.has("Flame Body Chip", self.player):
                return False
            return (has_weapon_at(state, "Buster", "Full Charge")
                    or has_weapon_at(state, "Z-Saber", "Charged Slash")
                    or has_weapon_at(state, "Recoil Rod", "Charged Rod")
                    or has_weapon_at(state, "Shield Boomerang", "Charged Throw")
                    or (state.has("EX Skill: Split Heavens", self.player)
                        and has_weapon_at(state, "Z-Saber", "Owns")))

        # Access items.
        for stage_name in stage_names:
            set_rule(
                self.multiworld.get_entrance(f"To {stage_name}", self.player),
                lambda state, item=f"{stage_name} Access": state.has(item, self.player),
            )

        # The base's later mission sets.
        set_rule(self.multiworld.get_entrance("To Resistance Base 2", self.player),
                 lambda state: state.has("Story Progress", self.player, STORY_MID))

        set_rule(self.multiworld.get_entrance("To Resistance Base 3", self.player),
                 lambda state: state.has("Story Progress", self.player, STORY_LATE))

        # The final stage. Needs every access item
        set_rule(
            self.multiworld.get_entrance("To Abandoned Research Laboratory", self.player),
            lambda state: state.has_all(stage_access_names, self.player),
        )

        # Location rules: Recoil Rod required
        for loc_name in [
            "Aegis Volcano Base (4) 114: Push 1st Container",
            "Oceanic Highway Ruins (1) 005: 1st Pit Breakable",
            "Weapons Repair Factory (2) 115: Hit 3rd Hammer",
            "Old Residential (1) 039: 1st Door",
            "Old Residential (3) 112: Floor Breakables",
            "Forest of Anatre (8) 040: Breakables Below Boss Room",
            "Giant Elevator (2) 041: 1st Passage High Ledges",
            "Giant Elevator (6) 027: 1st Descent Bottom Left Breakable",
        ]:
            add_rule(self.multiworld.get_location(loc_name, self.player), has_rod)

        # Location rules: Mobility required (Double Jump or Recoil Rod)
        for loc_name in [
            "Aegis Volcano Base (3) 026: Platform Above First Room",
            "Aegis Volcano Base (5) 073: Push Container Before Miniboss, Platform After",
            "Old Residential Subtank: Top Left after Pantheon Bombers",
            "Forest of Anatre (7) 076: Above 9th Button",
            "Giant Elevator 1-UP: 1st Passage High Ledges"
        ]:
            add_rule(self.multiworld.get_location(loc_name, self.player), has_mobility)

        # Location rules: Flame Body Chip required
        for loc_name in [
            "Old Residential (4) 074: Left Fork Door",
            "Forest of Anatre (1) 063: Treetops Above Start",
            "Forest of Anatre (2) 002: Ledge Above 1st Door",
            "Old Residential 1-UP (1): Right of Fork",
            "Old Residential 1-UP (2): Left Fork Door",
            "Forest of Anatre 1-UP: In Tree Near Start"
        ]:
            add_rule(self.multiworld.get_location(loc_name, self.player), has_flame)

        # Flame Body Chip + Recoil Rod
        add_rule(self.multiworld.get_location("Old Residential (2) 001: Stump Door", self.player),
                 lambda state: has_flame(state) and has_rod(state))

        # Mobility OR Frog Foot Chip
        add_rule(self.multiworld.get_location("Frontline Ice Base (1) 066: Top Route Tower", self.player),
                    lambda state: state.has("Secret Disk 004: Frog Foot Chip", self.player) or has_mobility(state))

        # Double Mobility: Double Jump Foot Chip + Recoil Rod
        add_rule(self.multiworld.get_location("Giant Elevator (1) 045: 1st Passage High Ledges", self.player),
                 lambda state: state.has("Double Jump Foot Chip", self.player) and has_rod(state))

        # Collectable 1-UP spawns in the new room
        add_rule(self.multiworld.get_location("Resistance Base 1-UP: In Locked Room by Andrew", self.player),
                 lambda state: state.has("Secret Disk 120: New Room Near Andrew", self.player))

        # Completion condition
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        
    def generate_output(self, output_directory: str) -> None:
        patch = MMZero3ProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "basepatch.bsdiff4"))
        write_tokens(self, patch)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

        #from Utils import visualize_regions
        #visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data
