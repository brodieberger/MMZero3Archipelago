from typing import TYPE_CHECKING

from worlds.generic.Rules import add_item_rule, set_rule
from .Items import STORY_LATE, STORY_MID, weapon_ability_level
from .Locations import shop_location_names

if TYPE_CHECKING:
    from . import MMZero3World


def set_rules(world: "MMZero3World") -> None:
    player = world.player

    def has_weapon_at(state, weapon: str, ability: str) -> bool:
        copies_needed = weapon_ability_level(weapon, ability)
        if weapon in world.starting_weapons:
            copies_needed -= 1
        return state.has(f"Progressive {weapon}", player, copies_needed)

    # Breaking blocks, moving platforms, and the rod jump.
    def has_rod(state):
        return has_weapon_at(state, "Recoil Rod", "Charged Rod")

    def has_mobility(state):
        return state.has("Double Jump Foot Chip", player) or has_rod(state)

    def has_flame(state):
        if not state.has("Flame Body Chip", player):
            return False
        return (has_weapon_at(state, "Buster", "Full Charge")
                or has_weapon_at(state, "Z-Saber", "Charged Slash")
                or has_weapon_at(state, "Recoil Rod", "Charged Rod")
                or has_weapon_at(state, "Shield Boomerang", "Charged Throw")
                or (state.has("EX Skill: Split Heavens", player)
                    and has_weapon_at(state, "Z-Saber", "Owns")))

    # Access items.
    for stage_name in world.stages():
        set_rule(
            world.multiworld.get_entrance(f"To {stage_name}", player),
            lambda state, item=f"{stage_name} Access": state.has(item, player),
        )
    slot_access_names = [f"{stage} Access" for stage in world.slot_stages]

    # Cerveau's shop.
    for slot in range(world.options.shop_slots.value):
        set_rule(
            world.multiworld.get_location(shop_location_names[slot], player),
            lambda state: state.has_any(slot_access_names, player),
        )

    # Zero 2's form. Most need a specific weapon to do their challenges.
    set_rule(world.multiworld.get_entrance("To Zero 2 Forms", player),
             lambda state: state.has_any([f"{stage} Access" for stage in world.stages()], player))
    world.add_location_rule("Erase Form", lambda state: has_weapon_at(state, "Shield Boomerang", "Owns"))
    world.add_location_rule("Defense Form", lambda state: has_weapon_at(state, "Shield Boomerang", "Charged Throw"))
    world.add_location_rule("Rise Form", lambda state: has_weapon_at(state, "Z-Saber", "Owns"))
    world.add_location_rule("Power Form", lambda state: has_weapon_at(state, "Chain Rod", "Owns"))
    world.add_location_rule("Active Form", lambda state: has_weapon_at(state, "Z-Saber", "Owns"))
    world.add_location_rule("X Form", lambda state: has_weapon_at(state, "Buster", "Owns"))

    # The base's later mission sets.
    set_rule(world.multiworld.get_entrance("To Resistance Base 2", player),
             lambda state: state.has("Story Progress", player, STORY_MID))

    set_rule(world.multiworld.get_entrance("To Resistance Base 3", player),
             lambda state: state.has("Story Progress", player, STORY_LATE))

    # The final stage. Needs the access items of stages needed, and the required disks
    stage_access_names = [f"{stage} Access" for stage in world.stages()]
    set_rule(
        world.multiworld.get_entrance("To Abandoned Research Laboratory", player),
        lambda state: state.has_from_list(stage_access_names, player, world.required_stage_count)
        and state.has_group("Secret Disks", player, world.required_disk_count),
    )
    # Since its lame that important items could spawn here, prevent progressive items
    for location in world.multiworld.get_region("Abandoned Research Laboratory", player).locations:
        add_item_rule(location, lambda item: not item.advancement)

    # Location rules: Recoil Rod required
    for loc_name in [
        "Oceanic Highway Ruins (1) 005: 1st Pit Breakable",
        "Weapons Repair Factory (2) 115: Hit 3rd Hammer",
        "Old Residential (1) 039: 1st Door",
        "Old Residential (3) 112: Floor Breakables",
        "Old Residential Energy (6): Breakable Blocks by Bombers",
        "Forest of Anatre (8) 040: Breakables Below Boss Room",
        "Giant Elevator (2) 041: 1st Passage High Ledges",
        "Giant Elevator (6) 027: 1st Descent Bottom Left Breakable",
        "Oceanic Highway Ruins E-Crystal (1): 1st Pit Breakable",
        "Oceanic Highway Ruins E-Crystal (2): 1st Pit Breakable",
        "Weapons Repair Factory E-Crystal (1): Hit 3rd Hammer",
        "Weapons Repair Factory E-Crystal (2): Hit 3rd Hammer",
        "Forest of Anatre Energy (3): Breakables Below Boss Room",
    ]:
        world.add_location_rule(loc_name, has_rod)

    # Location rules: Mobility required (Double Jump or Recoil Rod)
    for loc_name in [
        "Aegis Volcano Base (3) 026: Platform Above First Room",
        "Aegis Volcano Base (5) 073: Platform After Pushed Container",
        "Old Residential Subtank: Top Left Past Bombers",
        "Forest of Anatre (7) 076: Above 9th Button",
        "Giant Elevator 1-UP: 1st Passage High Ledges",
        "Aegis Volcano Base Energy: Platform Above First Room",
        "Old Residential E-Crystal (13): Top Left Past Bombers",
    ]:
        world.add_location_rule(loc_name, has_mobility)

    # Location rules: Flame Body Chip required
    for loc_name in [
        "Old Residential (4) 074: Left Fork Door",
        "Forest of Anatre (1) 063: Treetops Above Start",
        "Forest of Anatre (2) 002: Ledge Above 1st Door",
        "Old Residential 1-UP (1): Right of Fork",
        "Old Residential 1-UP (2): Left Fork Door",
        "Forest of Anatre 1-UP: In Tree Near Start",
        "Old Residential E-Crystal (1): Stump Door",
        "Old Residential Energy (1): Stump Door",
        "Old Residential E-Crystal (4): Door after Cutscene",
        "Old Residential E-Crystal (5): Door after Cutscene",
        "Old Residential E-Crystal (6): Door after Cutscene",
        "Forest of Anatre Energy (1): Treetops Above Generator Cannon",
        "Forest of Dysis Cyber Elf Yeppie: Forest Treetop",
        "Forest of Dysis Cyber Elf Ashiro: Forest Treetop (2)",
    ]:
        world.add_location_rule(loc_name, has_flame)

    # Flame Body Chip + Recoil Rod
    world.add_location_rule("Old Residential (2) 001: Stump Door",
                            lambda state: has_flame(state) and has_rod(state))

    # Mobility OR Splash Jump Foot Chip
    for loc_name in [
        "Frontline Ice Base (1) 066: Top Route Tower",
        "Frontline Ice Base Energy: Top Route Tower",
    ]:
        world.add_location_rule(
            loc_name,
            lambda state: state.has("Disk 005: Splash Jump Foot Chip", player) or has_mobility(state))

    # Technically reachable without
    world.add_location_rule("Missile Factory Energy (2): Missile Top Right",
                            lambda state: state.has("Double Jump Foot Chip", player))

    # Double Mobility: Double Jump Foot Chip + Recoil Rod
    world.add_location_rule("Giant Elevator (1) 045: 1st Passage High Ledges",
                            lambda state: state.has("Double Jump Foot Chip", player) and has_rod(state))

    # Collectable 1-UP spawns in the new room
    world.add_location_rule("Resistance Base 1-UP: In Locked Room by Andrew",
                            lambda state: state.has("Disk 120: New Room Near Andrew", player))

    # Recoil Rod pushes, Chain Rod pulls
    for loc_name in [
        "Aegis Volcano Base (4) 114: Push 1st Container",
        "Aegis Volcano Base E-Crystal (2): Push 1st Container",
        "Aegis Volcano Base E-Crystal (3): Push 1st Container",
    ]:
        world.add_location_rule(loc_name, lambda state: has_rod(state) or has_weapon_at(state, "Chain Rod", "Owns"))

    # You need to pogo off enemies for these ones.
    if world.options.randomize_enemies:
        for loc_name in [
            "Old Residential Subtank: Top Left Past Bombers",
            "Old Residential E-Crystal (13): Top Left Past Bombers",
        ]:
            world.add_location_rule(
                loc_name, lambda state: state.has("Double Jump Foot Chip", player) and has_rod(state))

    # Completion condition
    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
