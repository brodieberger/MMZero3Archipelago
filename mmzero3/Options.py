from dataclasses import dataclass
from Options import (Choice, Range, Toggle, DefaultOnToggle, OptionSet, DeathLink, OptionGroup,
                     PerGameCommonOptions)

from . import Data


class RequiredSecretDisks(Range):
    """Number of Secret Disks required to unlock the final stage.

    The Abandoned Research Laboratory opens once every other stage has been cleared and
    you are holding this many disks. Clearing it completes the game.
    Setting it above 170 is not recommended, as it will place a lot of useful items in the final stage, which
    at that point, the game is basically completed.
    """
    display_name = "Required Secret Disks"
    range_start = 0
    range_end = 180
    default = 120

class EasyExSkill(Toggle):
    """Rewards player with EX-Skill at the end of a level regardless of ranking."""
    display_name = "Always reward EX-Skill"
    

class StartingWeapons(OptionSet):
    """Which weapons Zero starts with.
    The weapon will still start at its first tier, and progressive unlocks (charge attacks and saber combos) will need to be unlocked.
    If this is left empty, one random weapon is granted instead.
    
    Valid Keys: {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}"""
    display_name = "Starting Weapons"
    valid_keys = {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}
    default = frozenset({"Buster", "Z-Saber"})

class Itemsanity(Toggle):
    """Makes every static energy and E-Crystal pickup a location check (82 in total)."""
    display_name = "Itemsanity"


class ExtraLifeSanity(DefaultOnToggle):
    """Makes every 1-UP pickup a location check (10 in total)."""
    display_name = "Extra Life Sanity"


class SelectButton(Choice):
    """Select buttons functionality.

    Cycle Sub Weapon (Default)
    Cycle Main Weapon
    Cycle Head Chip
    Cycle Body Chip
    Cycle Foot Chip
    Use Subtank (Uses fullest Subtank)
    """
    display_name = "Select Button"
    option_cycle_sub_weapon = Data.AP_SELECT_CYCLE_SUB_WEAPON
    option_cycle_main_weapon = Data.AP_SELECT_CYCLE_MAIN_WEAPON
    option_cycle_head_chip = Data.AP_SELECT_CYCLE_HEAD_CHIP
    option_cycle_body_chip = Data.AP_SELECT_CYCLE_BODY_CHIP
    option_cycle_foot_chip = Data.AP_SELECT_CYCLE_FOOT_CHIP
    option_use_subtank = Data.AP_SELECT_USE_SUBTANK
    default = option_cycle_sub_weapon


class WeaponDamageUpgrades(DefaultOnToggle):
    """Whether the last three steps of each progressive weapon raise its damage.

    A few players disliked this feature since it departed the gameplay from vanilla.

    WIP: Disabling this still keeps the extra three progressive weapon items in the pool, 
    they just dont provde any bonuses.
    """
    display_name = "Weapon Damage Upgrades"


class RandomizedPalettes(Toggle):
    """Every stage is drawn in a randomly chosen color scheme."""
    display_name = "Randomized Palettes"


class ShopSlots(Range):
    """How many slots Cerveau's shop stocks."""
    display_name = "Shop Slots"
    range_start = 0
    range_end = 48
    default = 16


class ShopPriceScale(Range):
    """How expensive Cerveau's shop is, as a percentage.

    Items range from 70 to 700 eCrystals, with most being in the 100 to 300 range.
    """
    display_name = "Shop Price Scale"
    range_start = 25
    range_end = 400
    default = 100

mmzero3_option_groups = [
    OptionGroup("Goal Options", [
        RequiredSecretDisks,
    ]),
    OptionGroup("Sanity Options", [
        ExtraLifeSanity,
        Itemsanity,
        ShopSlots,
        ShopPriceScale,
    ]),
    OptionGroup("Gameplay", [
        StartingWeapons,
        WeaponDamageUpgrades,
        SelectButton,
        EasyExSkill,
        DeathLink,
    ]),
    OptionGroup("Aesthetics", [
        RandomizedPalettes,
    ]),
]


@dataclass
class MMZero3Options(PerGameCommonOptions):
    required_secret_disks: RequiredSecretDisks
    easy_ex_skill: EasyExSkill
    starting_weapons: StartingWeapons
    itemsanity: Itemsanity
    extra_life_sanity: ExtraLifeSanity
    randomized_palettes: RandomizedPalettes
    select_button: SelectButton
    weapon_damage_upgrades: WeaponDamageUpgrades
    shop_slots: ShopSlots
    shop_price_scale: ShopPriceScale
    death_link: DeathLink
