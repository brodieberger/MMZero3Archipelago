from dataclasses import dataclass
from Options import (Choice, Range, NamedRange, Toggle, DefaultOnToggle, OptionSet, DeathLink, OptionGroup,
                     StartInventoryPool, PerGameCommonOptions, Visibility)

from .data import Data


class RequiredSecretDisks(Range):
    """Percentage of the seed's Secret Disks you must hold to open the final stage."""
    display_name = "Required Secret Disks"
    range_start = 0
    range_end = 100
    default = 67

class RequiredStageClears(Range):
    """Percentage of the available stages you must clear to open the final stage."""
    display_name = "Required Stage Clears"
    range_start = 0
    range_end = 100
    default = 100


class ExSkillRank(Choice):
    """The rank you must get in a stage to send that stage's "A+ Rank Clear" check.

    Note: The ranking system has been modified, and you are now judged per stage rather than your average. 
    
    F sends the check on any clear.
    """
    display_name = "EX Skill Rank"
    option_s = Data.RANK_S
    option_a = Data.RANK_A
    option_b = Data.RANK_B
    option_c = Data.RANK_C
    option_d = Data.RANK_D
    option_e = Data.RANK_E
    option_f = Data.RANK_F
    default = Data.RANK_A


class FinalStageRank(Choice):
    """The rank you need to get on a stage completion, for it to count toward opening the final stage."""
    display_name = "Final Stage Rank"
    option_s = Data.RANK_S
    option_a = Data.RANK_A
    option_b = Data.RANK_B
    option_c = Data.RANK_C
    option_d = Data.RANK_D
    option_e = Data.RANK_E
    option_f = Data.RANK_F
    default = Data.RANK_F


class StartingWeapons(OptionSet):
    """Which weapons Zero starts with.
    The weapon will still start at its first tier, and progressive unlocks (charge attacks and saber combos) will need to be unlocked.
    If this is left empty, one random weapon is granted instead.
    
    Valid Keys: {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}"""
    display_name = "Starting Weapons"
    valid_keys = {"Buster", "Z-Saber", "Recoil Rod", "Shield Boomerang"}
    default = frozenset({"Buster", "Z-Saber"})

class Itemsanity(Toggle):
    """Makes every static life energy and E-Crystal pickup a location check (82 in total)."""
    display_name = "Itemsanity"


class ExtraLifeSanity(DefaultOnToggle):
    """Makes every 1-UP pickup a location check (10 in Zero 3's stages, 21 in Zero 2's)."""
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


class CyberElves(Choice):
    """Modifications to Cyber Elf usage. Satellite elves remain unmodified.

    Vanilla: Unmodified Vanilla. Upgrading elves costs E-Crystals and using fusion elves decrease rank.

    No Penalty: Fusing an elf does not affect rank.

    Auto: Every passive elf received via disk is automatically opened and applied. 
    Does not affect rank. Gives the game a nice sense of progression, but makes it a lot easier.
    """
    display_name = "Cyber-elves"
    option_vanilla = Data.AP_ELVES_VANILLA
    option_no_penalty = Data.AP_ELVES_NO_PENALTY
    option_auto = Data.AP_ELVES_AUTO
    default = option_vanilla


class WeaponDamageUpgrades(DefaultOnToggle):
    """Whether the last three steps of each progressive weapon raise its damage.

    A few players disliked this feature since it departed the gameplay from vanilla.

    WIP: Disabling this still keeps the extra three progressive weapon items in the pool, 
    they just don't provide any bonuses.
    """
    display_name = "Weapon Damage Upgrades"


class RandomizedPalettes(Toggle):
    """Every stage is drawn in a randomly chosen color scheme."""
    display_name = "Randomized Palettes"


class RandomizeEnemies(Toggle):
    """
    Randomize each enemy spawn location.

    WARNING: VERY EARLY WORK IN PROGRESS. DO NOT TAKE INTO BIG MULTIWORLDS!

    This mode is very buggy, see the readme section to know what to expect.

    Recommended to enable enemy disk markers!
    """
    display_name = "Randomize Enemies (WIP)"


class EnemyDifficulty(Choice):
    """
    Only applies if enemy randomization is enabled. Higher difficulties put more enemies in the spot for one, based off of the health of the spot being replaced.
    
    Minimal: Tries to match enemy placements by health. If a less health enemy replaces one with more health, place multiple copies at that location.
    
    Chaos: Places multiple enemies around every spawnpoint regardless of HP or enemy type. Leads to many more enemies per stage. Developer's choice!
    
    Insanity: Places as many enemies as possible. Tries to prioritize enemies with higher HP. Expect many shield enemies in tight quarters. Good luck!
    """
    display_name = "Randomized Enemy Difficulty (WIP)"
    option_minimal = 0
    option_chaos = 1
    option_insanity = 2
    default = 0


class DiskNamePopup(DefaultOnToggle):
    """
    When a Secret Disk arrives from Archipelago, an on screen notification describes its contents.

    The visual is slightly screen obscuring, so it is kept optional.
    """
    display_name = "Disk Name Popup"


class EnemyDiskMarkers(DefaultOnToggle):
    """
    Show a small Archipelago logo above enemies that can drop disks.
    Recommended with enemy randomizer!
    """
    display_name = "Enemy Disk Markers"


class LegacyStages(Choice):
    """
    Adds stages from Mega Man Zero 2 to the seed. Chain Rod included as a fifth weapon. Zero 2 forms are also added as location checks.

    Enemy Randomizer, Stage Palette Randomizer, and Itemsanity are not currently supported for these stages.

    Off: Zero 3's 16 stages only.

    Shuffle: still 16 stages, but Zero 2 stages take the place of some of Zero 3's.

    All: all 16 Zero 2 stages added to the world, for 32 stages in total.
    
    Needs your own Mega Man Zero 2 (USA) ROM: set zero2_rom_file under MMZero3_settings in host.yaml, in your
    Archipelago folder.
    """
    display_name = "Legacy Stages"
    option_off = 0
    option_shuffle = 1
    option_all = 2
    default = 0


class CutSecretDisks(Toggle):
    """
    (WIP)

    Your seed may fail to generate if not enough locations are included (likely due to shuffling Zero 2 stages which have fewer checks).

    You can try to add more shop slots, extra life sanity, or itemsanity to prevent this, or finally enable this option as a last resort.

    Off: the seed fails to generate, saying how many checks it is short.

    On: Secret Disks are removed until the seed can successfully generate. The world will remove the least useful disks first, from text files, cosmetics,
    base decorations, E-Crystal disks, then cyber elves.
    """
    display_name = "Cut Secret Disks"


class LegacyShuffleCount(NamedRange):
    """When Zero 2 stages are shuffled in, how many of Zero 3's 15 stages (all but the final one) they replace.

    1 to 15: exactly that many Zero 3 stages to replace with Zero 2 stages.
    Coin flip (0): each stage has a 50/50 chance of being replaced.
    """
    display_name = "Legacy Shuffle Count"
    range_start = 0
    range_end = 15
    default = 0
    special_range_names = {"coin_flip": 0}


class InfiniteLives(Toggle):
    """Get infinite lives."""
    display_name = "Infinite Lives"


class AttackModeB(Toggle):
    """
    Start a new game with the attack mode set to Type B instead of Type A.

    You can still change it in game after the fact. This is just to save you several seconds every time you start a new game.
    """
    display_name = "Attack Mode B"


class DoubleTapDash(DefaultOnToggle):
    """Tapping left or right twice dashes, as how it works in the vanilla game. Disable to dash only with the dash button."""
    display_name = "Double-Tap Dash"


class AirSpinSlash(Choice):
    """How an air spinning slash is performed when cyber elf Malthas (Disk 066) is active.

    Hold Up: Hold up while slashing in the air, as in the vanilla game.

    Jump Slash: Every slash in the air spins, as in Mega Man Zero 1 and 2. Hold up for a normal slash.

    Double Tap: Press attack again during an air slash to spin after it, as in Mega Man ZX.
    """
    display_name = "Air Spin Slash"
    option_hold_up = Data.AP_AIR_SPIN_HOLD_UP
    option_jump_slash = Data.AP_AIR_SPIN_JUMP_SLASH
    option_double_tap = Data.AP_AIR_SPIN_DOUBLE_TAP
    default = option_hold_up


class ShopSlots(Range):
    """How many slots Cerveau's shop stocks."""
    display_name = "Shop Slots"
    range_start = 0
    range_end = 48
    default = 16


class ShopPriceScale(Range):
    """How expensive Cerveau's shop is, as a percentage.

    Items range from 70 to 700 E-Crystals, with most being in the 100 to 300 range.
    """
    display_name = "Shop Price Scale"
    range_start = 25
    range_end = 400
    default = 100

class TrapPercentage(Range):
    """The percentage of filler items that are replaced with traps."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class EnabledTraps(OptionSet):
    """
    Which traps may be placed. More interesting traps will come in a later update!
    Valid Keys: {"Earthquake", "Pixelate", "Slippery Floor"}
    """
    display_name = "Enabled Traps"
    valid_keys = {"Earthquake", "Pixelate", "Slippery Floor"}
    default = frozenset(valid_keys)


mmzero3_option_groups = [
    OptionGroup("Goal Options", [
        RequiredSecretDisks,
        RequiredStageClears,
        FinalStageRank,
    ]),
    OptionGroup("Legacy Stages (Zero 2)", [
        LegacyStages,
        LegacyShuffleCount,
        CutSecretDisks,
    ]),
    OptionGroup("Sanity Options", [
        ExtraLifeSanity,
        Itemsanity,
        ShopSlots,
        ShopPriceScale,
    ]),
    OptionGroup("Optional Randomization", [
        RandomizeEnemies,
        EnemyDifficulty,
    ]),
    OptionGroup("Gameplay", [
        StartingWeapons,
        WeaponDamageUpgrades,
        SelectButton,
        CyberElves,
        ExSkillRank,
        InfiniteLives,
        AttackModeB,
        DoubleTapDash,
        AirSpinSlash,
        DeathLink,
    ]),
    OptionGroup("Traps", [
        TrapPercentage,
        EnabledTraps,
    ]),
    OptionGroup("Aesthetics", [
        RandomizedPalettes,
        DiskNamePopup,
        EnemyDiskMarkers,
    ]),
]


@dataclass
class MMZero3Options(PerGameCommonOptions):
    required_secret_disks: RequiredSecretDisks
    required_stage_clears: RequiredStageClears
    ex_skill_rank: ExSkillRank
    final_stage_rank: FinalStageRank
    starting_weapons: StartingWeapons
    itemsanity: Itemsanity
    extra_life_sanity: ExtraLifeSanity
    randomized_palettes: RandomizedPalettes
    select_button: SelectButton
    weapon_damage_upgrades: WeaponDamageUpgrades
    cyber_elves: CyberElves
    disk_name_popup: DiskNamePopup
    enemy_disk_markers: EnemyDiskMarkers
    infinite_lives: InfiniteLives
    attack_mode_b: AttackModeB
    double_tap_dash: DoubleTapDash
    air_spin_slash: AirSpinSlash
    randomize_enemies: RandomizeEnemies
    enemy_difficulty: EnemyDifficulty
    start_inventory_from_pool: StartInventoryPool
    shop_slots: ShopSlots
    shop_price_scale: ShopPriceScale
    legacy_stages: LegacyStages
    legacy_shuffle_count: LegacyShuffleCount
    cut_secret_disks: CutSecretDisks
    trap_percentage: TrapPercentage
    enabled_traps: EnabledTraps
    death_link: DeathLink
