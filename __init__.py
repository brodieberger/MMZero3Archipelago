import logging
import math
from typing import List, Dict, Any, ClassVar, Optional

from BaseClasses import Region, Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule
from .Items import (MMZero3Item, disk_cut_tier, item_data_table, item_name_groups, item_table, legacy_stage_names,
                    stage_names, weapon_names)
from .Locations import MMZero3Location, location_data_table, location_name_groups, location_table, locked_locations
from .Options import LegacyStages, MMZero3Options, mmzero3_option_groups
from .Presets import mmzero3_options_presets
from .Regions import region_data_table
from .Rules import set_rules
from .Rom import MMZero3ProcedurePatch, MMZero3Settings, write_tokens
from .data import Data
from .randomizers import EnemyRando, Palettes
from .Client import MMZero3Client

import pkgutil
import hashlib
import os
from worlds.Files import APProcedurePatch

class MMZero3WebWorld(WebWorld):
    theme = "ice"
    bug_report_page = "https://github.com/brodieberger/MMZero3Archipelago/issues"
    option_groups = mmzero3_option_groups
    options_presets = mmzero3_options_presets
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
    Play as Zero and fight through Neo Arcadia's Mutos Reploids to defeat Omega and stop Dr. Weil.
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
    slot_stages: List[str]
    required_disk_count: int
    required_stage_count: int

    def generate_early(self) -> None:
        self.roll_shop_prices()
        self.roll_palettes()
        difficulty = (1.0, 1.5, 2.0)[self.options.enemy_difficulty.value]
        self.enemies = EnemyRando.randomize(self.random, difficulty) \
            if self.options.randomize_enemies else {}

        # Inform the Universal Tracker what the starting items are
        passthrough = None
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Mega Man Zero 3" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["Mega Man Zero 3"]

        if passthrough:
            self.starting_weapons = set(passthrough["starting_weapons"])
            self.options.randomize_enemies.value = passthrough.get("randomize_enemies", 0)
            self.slot_stages = passthrough["slot_stages"]
            self.required_disk_count = passthrough["required_disk_count"]
            self.required_stage_count = passthrough["required_stage_count"]
        else:
            self.starting_weapons = set(self.options.starting_weapons.value)

            if not self.starting_weapons:
                self.starting_weapons = {self.random.choice(weapon_names)}
            self.slot_stages = self.roll_slot_stages()
            self.required_disk_count = self.disks_in_seed() * self.options.required_secret_disks.value // 100
            self.required_stage_count = len(self.stages()) * self.options.required_stage_clears.value // 100

        # If it is your only weapon, add another Shield Boomerang so you can actually attack.
        if self.starting_weapons == {"Shield Boomerang"}:
            self.multiworld.push_precollected(self.create_item("Progressive Shield Boomerang"))

        # Force the first stage access item to be early local
        first_stage_access = self.random.choice([f"{stage} Access" for stage in self.slot_stages])
        self.multiworld.local_early_items[self.player][first_stage_access] = 1

    def roll_slot_stages(self) -> List[str]:
        """Zero 3's 15 stage slots in order, each holding its own stage or, with shuffle, a Zero 2 one."""
        stages = list(stage_names)
        if self.options.legacy_stages != LegacyStages.option_shuffle:
            return stages
        count = self.options.legacy_shuffle_count.value
        if count:
            slots = self.random.sample(range(len(stages)), count)
        else:
            slots = []
            while not slots:
                slots = [slot for slot in range(len(stages)) if self.random.random() < 0.5]
        for slot, stage in zip(slots, self.random.sample(legacy_stage_names, len(slots))):
            stages[slot] = stage
        return stages

    def stages(self) -> List[str]:
        """Every stage in the seed but the final one."""
        if self.options.legacy_stages == LegacyStages.option_all:
            return self.slot_stages + legacy_stage_names
        return self.slot_stages

    def location_region(self, name: str) -> Optional[str]:
        """The region a location is in this seed, None if the seed does not have it.

        A boss's chip stays with its slot when a Zero 2 stage takes the slot.
        """
        data = location_data_table[name]
        if not data.can_create(self):
            return None
        if data.region in stage_names and data.region not in self.slot_stages:
            if name.startswith("Collect "):
                return self.slot_stages[stage_names.index(data.region)]
            return None
        if data.region in legacy_stage_names and data.region not in self.stages():
            return None
        return data.region

    def free_location_count(self) -> int:
        return sum(1 for name, data in location_data_table.items()
                   if not data.locked_item and self.location_region(name))

    def pool_names(self) -> List[str]:
        """Every item the pool always holds, a name per copy: all but the plain disks and the filler."""
        locked_item_names = {data.locked_item for data in locked_locations.values() if data.locked_item}
        return [name for name, item in item_data_table.items()
                if item.code and item.can_create(self) and name not in locked_item_names
                and not (name.startswith("Disk ") and disk_cut_tier(int(name[5:8])) is not None)
                for _ in range(item.count(self))]

    def disks_in_seed(self) -> int:
        """180 Secret Disks, less the plain ones a full pool has no room for when cut_secret_disks allows it."""
        if not self.options.cut_secret_disks:
            return 180
        plain = sum(1 for disk in range(1, 181) if disk_cut_tier(disk) is not None)
        room = self.free_location_count() - len(self.pool_names())
        return 180 - max(0, plain - room)

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
        names = self.pool_names()
        free = self.free_location_count()

        # Plain disks in the order they leave a full pool, shuffled within each tier
        plain = [name for name in item_data_table
                 if name.startswith("Disk ") and disk_cut_tier(int(name[5:8])) is not None]
        self.random.shuffle(plain)
        plain.sort(key=lambda name: disk_cut_tier(int(name[5:8])))
        cut = 180 - self.disks_in_seed()
        if cut:
            logging.warning(f"Mega Man Zero 3 ({self.player_name}): the item pool is full, so {cut} plain Secret "
                            f"Disks are left out. More shop_slots, itemsanity or extra_life_sanity bring them back.")
        names += plain[cut:]
        if len(names) > free:
            raise OptionError(
                f"Mega Man Zero 3 ({self.player_name}): {len(names)} items for {free} locations, "
                f"{len(names) - free} short. Turn on itemsanity or extra_life_sanity, stock more shop_slots, "
                f"shuffle in fewer Zero 2 stages, or turn on cut_secret_disks.")

        self.multiworld.itempool += [self.create_item(name) for name in names]
        for _ in range(free - len(names)):
            self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))

    def create_regions(self) -> None:
        stages = set(self.stages())
        names = [name for name in region_data_table
                 if name not in stage_names and name not in legacy_stage_names or name in stages]
        for region_name in names:
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        for region_name in names:
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if self.location_region(location_name) == region_name
            }, MMZero3Location)
            region.add_exits({target: f"To {target}" for target in region_data_table[region_name].connecting_regions
                              if target in names})

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not self.location_region(location_name):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.get_location(location_name).place_locked_item(locked_item)

    def get_filler_item_name(self) -> str:
        traps = sorted(self.options.enabled_traps.value)
        if traps and self.random.randrange(100) < self.options.trap_percentage.value:
            return f"{self.random.choice(traps)} Trap"
        return "100 Energy Crystals"
    
    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "required_secret_disks": self.options.required_secret_disks.value,
            "required_disk_count": self.required_disk_count,
            "required_stage_clears": self.options.required_stage_clears.value,
            "required_stage_count": self.required_stage_count,
            "slot_stages": self.slot_stages,
            "ex_skill_rank": self.options.ex_skill_rank.value,
            "final_stage_rank": self.options.final_stage_rank.value,
            "starting_weapons": sorted(self.starting_weapons),
            "itemsanity": self.options.itemsanity.value,
            "extra_life_sanity": self.options.extra_life_sanity.value,
            "death_link": self.options.death_link.value,
            "randomize_enemies": self.options.randomize_enemies.value,
            "legacy_stages": self.options.legacy_stages.value,
        }

    ELF_PRICE_COSTS = (70, 100, 150, 200, 250, 300, 400, 500, 700)

    def roll_shop_prices(self) -> None:
        self.shop_prices = []
        for _ in range(self.options.shop_slots.value):
            price = self.random.choice(self.ELF_PRICE_COSTS)
            price = price * self.options.shop_price_scale.value // 100
            price = price // 10 * 10        # every vanilla elf cost is a round ten

            if price < 10:
                price = 10
            if price > 9990:
                price = 9990

            self.shop_prices.append(price)

    def add_location_rule(self, loc_name: str, rule) -> None:
        """add_rule, but skips a location this seed does not have."""
        if self.location_region(loc_name):
            add_rule(self.multiworld.get_location(loc_name, self.player), rule)

    def roll_palettes(self) -> None:
        """Decide on the palette preset that each stage will be drawn on."""
        self.stage_palettes = {}
        if not self.options.randomized_palettes.value:
            return
        for stage_id in Data.STAGE_PALETTES:
            choices = Palettes.HUES + Palettes.STAGE_THEMES[stage_id]
            self.stage_palettes[stage_id] = self.random.choice(choices)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_output(self, output_directory: str) -> None:
        patch = MMZero3ProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff4"))
        write_tokens(self, patch)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

        #from Utils import visualize_regions
        #visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data
