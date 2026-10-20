import hashlib
import json
import os
import pkgutil
from typing import List, TYPE_CHECKING

import settings
import Utils
from BaseClasses import ItemClassification
from settings import get_settings
from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes

from .data import Data
from .randomizers import EnemyRando, Palettes
from .Locations import shop_location_names

# Zero 2 Data locations to copy from player's ROM.
LEGACY = json.loads(pkgutil.get_data(__package__, "data/legacy.json"))

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


def get_zero2_rom_bytes() -> bytes:
    file_name = get_settings().MMZero3_settings["zero2_rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    if not os.path.exists(file_name):
        raise FileNotFoundError(
            "This seed has the legacy stages, which are built from your own Mega Man Zero 2 (USA) "
            f"ROM: set MMZero3_settings.zero2_rom_file in host.yaml (looked for {file_name})")
    with open(file_name, "rb") as infile:
        data = infile.read()
    if hashlib.md5(data).hexdigest() != LEGACY["zero2_md5"]:
        raise Exception(f"{file_name} is not Mega Man Zero 2 (USA): its md5 does not match")
    return data


def lz77(data: bytes, at: int) -> bytes:
    """GBA LZ77 compression."""
    size = int.from_bytes(data[at + 1:at + 4], "little")
    out = bytearray()
    i = at + 4
    while len(out) < size:
        flags = data[i]
        i += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                b0, b1 = data[i], data[i + 1]
                i += 2
                disp = (((b0 & 0xF) << 8) | b1) + 1
                for _ in range((b0 >> 4) + 3):
                    out.append(out[-disp])
            else:
                out.append(data[i])
                i += 1
    return bytes(out[:size])


def decompress_art(data: bytes, src: int, stored: int) -> bytes:
    """Zero 2"""
    out = bytearray()
    p = src
    while p < src + stored:
        head = int.from_bytes(data[p:p + 4], "little")
        if head == 0:
            break
        n = head & 0xFFFFFF
        out += lz77(data, p + 4) if head & 0x80000000 else data[p + 4:p + n]
        p += n
    return bytes(out)


class MMZero3ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mega Man Zero 3"
    hash = "aa1d5eeffcd5e4577db9ee6d9b1100f9"
    patch_file_ending = ".apmmzero3"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
        ("fill_legacy_stages", []),
        ("recolor_palettes", ["palettes.json"]),
        ("recolor_enemies", ["enemies.json"]),
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
    words = []
    for word in text.split():
        while len(word) > cols:
            words.append(word[:cols])
            word = word[cols:]
        words.append(word)

    out = []
    line = ""
    for word in words:
        longer = word if line == "" else line + " " + word
        if len(longer) <= cols:
            line = longer
        else:
            out.append(line)
            line = word
    if line != "":
        out.append(line)

    if len(out) > lines:
        out = out[:lines]
        last = out[-1]
        if len(last) + 3 > cols:
            last = last[:cols - 3].rstrip()
        out[-1] = last + "..."
    return out


class MMZero3PatchExtensions(APPatchExtension):
    game = "Mega Man Zero 3"

    @staticmethod
    def recolor_palettes(caller: APProcedurePatch, rom: bytes, rolls_file: str) -> bytes:
        """Randomized level palettes"""
        rolls = json.loads(caller.get_file(rolls_file).decode("utf-8"))
        by_offset = {}
        for stage_id, preset in rolls.items():
            for offset, size in Data.STAGE_PALETTES[int(stage_id)]:
                by_offset[offset] = (size, preset)

        rom = bytearray(rom)
        for offset, (size, preset) in by_offset.items():
            rom[offset:offset + size] = Palettes.recolor(rom[offset:offset + size],
                                                          Palettes.PRESETS[preset])
        return bytes(rom)

    @staticmethod
    def fill_legacy_stages(caller: APProcedurePatch, rom: bytes) -> bytes:
        """
        Art, stage layout bytes, and sound effects from Zero 2 ROM, provided by the player.
        Also handles compressed assets.
        """
        at, _ = Data.SEED_CONFIG_FIELDS["legacyStages"]
        if not rom[Data.SEED_CONFIG_ROM_OFFSET + at]:
            return rom
        zero2 = get_zero2_rom_bytes()
        art = [decompress_art(zero2, int(src, 16), stored) for src, stored in LEGACY["compressed_art"]]
        rom = bytearray(rom)
        for offset, src, size in LEGACY["zero2_copies"]:
            offset, src = int(offset, 16), int(src, 16)
            rom[offset:offset + size] = zero2[src:src + size]
        for offset, i, src, size in LEGACY["art_copies"]:
            offset, src = int(offset, 16), int(src, 16)
            rom[offset:offset + size] = art[i][src:src + size]
        for offset, data in LEGACY["new_bytes"]:
            offset, data = int(offset, 16), bytes.fromhex(data)
            rom[offset:offset + len(data)] = data
        return bytes(rom)

    @staticmethod
    def recolor_enemies(caller: APProcedurePatch, rom: bytes, flag_file: str) -> bytes:
        """
        Trim and redraw each enemy sheets to match the correct palettes. Used for Randomized enemies.
        """
        if not json.loads(caller.get_file(flag_file).decode("utf-8")):
            return rom
        rom = bytearray(rom)
        EnemyRando.trim_sheets(rom)
        EnemyRando.recolor(rom)
        return bytes(rom)


def shop_record(name_lines: List[str], player_lines: List[str], kind: int, code: int) -> bytes:
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
    while len(out) % 2 != 0:          # the item code is a u16, so it needs to start on an even byte
        out.append(0)
    out += code.to_bytes(2, "little")
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
            out += shop_record([], [], 0, 0)
            continue

        item = world.multiworld.get_location(shop_location_names[slot], world.player).item

        if item.advancement:
            kind = Data.AP_SHOP_KIND_PROGRESSION
        elif item.classification == ItemClassification.trap:
            kind = Data.AP_SHOP_KIND_TRAP
        else:
            kind = Data.AP_SHOP_KIND_PLAIN

        if item.player == world.player:
            kind |= Data.AP_SHOP_OWN_WORLD
            code = item.code
            player = ""
        else:
            code = 0
            player = world.multiworld.get_player_name(item.player)

        name_lines = wrap_text(item.name, cols, Data.AP_SHOP_NAME_LINES)
        player_lines = wrap_text(player, cols, Data.AP_SHOP_PLAYER_LINES)
        out += shop_record(name_lines, player_lines, kind, code)

    return bytes(out)


def write_tokens(world: "MMZero3World", patch: MMZero3ProcedurePatch) -> None:
    """Write this seed's settings over ApSeedConfig in the ROM.

    struct ApSeedConfig {
        u16 requiredDisks;
        u8  startingWeapons;
        u8  exSkillRank;
        u8  itemsanity;
        u8  exLifeSanity;
        u8  selectButton;
        u8  damageUpgrades;
        u8  cyberElves;
        u8  diskNamePopup;
        u8  infiniteLives;
        u8  finalStageRank;
        u8  enemyDiskMarkers;
        u8  legacyStages;
        u8  unused[2];
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
        "exSkillRank": world.options.ex_skill_rank.value,
        "itemsanity": 1 if world.options.itemsanity.value else 0,
        "exLifeSanity": 1 if world.options.extra_life_sanity.value else 0,
        "selectButton": world.options.select_button.value,
        "damageUpgrades": 1 if world.options.weapon_damage_upgrades.value else 0,
        "cyberElves": world.options.cyber_elves.value,
        "diskNamePopup": 1 if world.options.disk_name_popup.value else 0,
        "infiniteLives": 1 if world.options.infinite_lives.value else 0,
        "finalStageRank": world.options.final_stage_rank.value,
        "enemyDiskMarkers": 1 if world.options.enemy_disk_markers.value else 0,
        "legacyStages": 1 if world.options.legacy_stages.value else 0,
        "unused": 0,
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

    if world.enemies:
        for offset, data in EnemyRando.writes(world.enemies):
            patch.write_token(APTokenTypes.WRITE, offset, data)

    patch.write_file("token_data.bin", patch.get_token_binary())

    patch.write_file("palettes.json", json.dumps(world.stage_palettes).encode("utf-8"))
    patch.write_file("enemies.json", json.dumps(bool(world.enemies)).encode("utf-8"))


class MMZero3Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 3 (USA) ROM"""
        required = True
        description = "Mega Man Zero 3 (USA) ROM File"
        copy_to = "Mega Man Zero 3 (USA).gba"
        md5s = [MMZero3ProcedurePatch.hash]

    class Zero2RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 2 (USA) ROM, for seeds with the legacy stages"""
        required = False
        description = "Mega Man Zero 2 (USA) ROM File"
        copy_to = "Mega Man Zero 2 (USA).gba"
        md5s = [LEGACY["zero2_md5"]]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    zero2_rom_file: Zero2RomFile = Zero2RomFile(Zero2RomFile.copy_to)
