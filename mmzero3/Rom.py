import os
from typing import List, TYPE_CHECKING

import settings
import Utils
from BaseClasses import ItemClassification
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from . import Data
from .Locations import shop_location_names

if TYPE_CHECKING:
    from . import MMZero3World


# Bit positions in ZeroStatus.unlockedWeapon.
WEAPON_BITS = {"Buster": 0, "Z-Saber": 1, "Recoil Rod": 2, "Shield Boomerang": 3}


def get_base_rom_bytes() -> bytes:
    file_name = get_settings().MMZero3_settings["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    with open(file_name, "rb") as infile:
        return infile.read()


class MMZero3ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mega Man Zero 3"
    hash = "aa1d5eeffcd5e4577db9ee6d9b1100f9"
    patch_file_ending = ".apmmzero3"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def encode_text(text: str, cols: int) -> bytes:
    """
    String into a series of bytes the ROM can print using the charmap.
    
    For shop's text. Anything not in Data's charmap becomes a ?.
    """
    out = bytearray()
    for letter in text[:cols]:
        if letter in Data.CHARMAP:
            out.append(Data.CHARMAP[letter])
        else:
            out.append(Data.CHARMAP["?"])

    out.append(Data.AP_SHOP_TEXT_END)
    while len(out) < cols + 1:
        out.append(0)
    return bytes(out)


def wrap_text(text: str, cols: int, lines: int) -> List[str]:
    out = []
    line = ""

    for word in text.split():
        if len(word) > cols:
            word = word[:cols]

        if line == "":
            longer = word
        else:
            longer = line + " " + word

        if len(longer) <= cols:
            line = longer
        else:
            out.append(line)
            line = word

        if len(out) == lines:
            return out

    if line != "":
        out.append(line)
    return out[:lines]


def shop_record(name_lines: List[str], player_lines: List[str], kind: int) -> bytes:
    """
    Get data for one shop item. 68 Bytes total: 
    The name lines, the player lines, the kind byte, then padding.
    """
    cols = Data.AP_SHOP_TEXT_COLS
    out = bytearray()

    for i in range(Data.AP_SHOP_NAME_LINES):
        if i < len(name_lines):
            out += encode_text(name_lines[i], cols)
        else:
            out += encode_text("", cols)

    for i in range(Data.AP_SHOP_PLAYER_LINES):
        if i < len(player_lines):
            out += encode_text(player_lines[i], cols)
        else:
            out += encode_text("", cols)

    out.append(kind)
    while len(out) < Data.SHOP_ITEMS_SIZE:
        out.append(0)
    return bytes(out)


def shop_item_records(world: "MMZero3World") -> bytes:
    """
    Gets all shop item information from world to place into ROM, formatting when needed.
    """
    cols = Data.AP_SHOP_TEXT_COLS
    out = bytearray()

    for slot in range(Data.SHOP_ITEMS_COUNT):
        if slot >= world.options.shop_slots.value:
            out += shop_record([], [], 0)
            continue

        item = world.multiworld.get_location(shop_location_names[slot], world.player).item

        if item.advancement:
            kind = Data.AP_SHOP_KIND_PROGRESSION
        elif item.classification == ItemClassification.trap:
            kind = Data.AP_SHOP_KIND_TRAP
        else:
            kind = Data.AP_SHOP_KIND_PLAIN

        # TODO render each MMZERO3 item as its own icon.
        if item.player == world.player:
            kind |= Data.AP_SHOP_OWN_WORLD
            if item.name.startswith("Secret Disk"):
                kind |= Data.AP_SHOP_IS_DISK
            player = ""
        else:
            player = world.multiworld.get_player_name(item.player)

        name_lines = wrap_text(item.name, cols, Data.AP_SHOP_NAME_LINES)
        player_lines = wrap_text(player, cols, Data.AP_SHOP_PLAYER_LINES)
        out += shop_record(name_lines, player_lines, kind)

    return bytes(out)


def write_tokens(world: "MMZero3World", patch: MMZero3ProcedurePatch) -> None:
    """Write this seed's settings over ApSeedConfig in the ROM.

    struct ApSeedConfig {
        u16 requiredDisks;
        u8  startingWeapons;
        u8  easyExSkill;
    };

    Theres also gApShopPrices, one u16 per shop slot: 
    what that slot costs, or 0 for a slot this seed does not stock

    And gApShopItems, one record a slot saying what is in it.
    """
    starting_weapons = 0
    for name in world.starting_weapons:
        starting_weapons |= 1 << WEAPON_BITS[name]

    values = {
        "requiredDisks": world.options.required_secret_disks.value,
        "startingWeapons": starting_weapons,
        "easyExSkill": 1 if world.options.easy_ex_skill.value else 0,
    }

    seed_config = bytearray(Data.SEED_CONFIG_SIZE)
    for name, (offset, size) in Data.SEED_CONFIG_FIELDS.items():
        seed_config[offset:offset + size] = values[name].to_bytes(size, "little")

    patch.write_token(APTokenTypes.WRITE, Data.SEED_CONFIG_ROM_OFFSET, bytes(seed_config))

    prices = bytearray()
    for slot in range(Data.SHOP_PRICES_COUNT):
        if slot < len(world.shop_prices):
            price = world.shop_prices[slot]
        else:
            price = 0
        prices += price.to_bytes(Data.SHOP_PRICES_ELEMENT_SIZE, "little")
    patch.write_token(APTokenTypes.WRITE, Data.SHOP_PRICES_ROM_OFFSET, bytes(prices))

    patch.write_token(APTokenTypes.WRITE, Data.SHOP_ITEMS_ROM_OFFSET, shop_item_records(world))

    patch.write_file("token_data.bin", patch.get_token_binary())


class MMZero3Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 3 (USA) ROM"""
        required = True
        description = "Mega Man Zero 3 (USA) ROM File"
        copy_to = "Mega Man Zero 3 (USA).gba"
        md5s = [MMZero3ProcedurePatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)
