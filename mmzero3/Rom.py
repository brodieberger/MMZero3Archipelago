import os
from typing import TYPE_CHECKING

import settings
import Utils
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from . import Data

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


def write_tokens(world: "MMZero3World", patch: MMZero3ProcedurePatch) -> None:
    """Write this seed's settings over ApSeedConfig in the ROM.

    struct ApSeedConfig {
        u16 requiredDisks;
        u8  startingWeapons;
        u8  easyExSkill;
    };
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
    patch.write_file("token_data.bin", patch.get_token_binary())


class MMZero3Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 3 (USA) ROM"""
        required = True
        description = "Mega Man Zero 3 (USA) ROM File"
        copy_to = "Mega Man Zero 3 (USA).gba"
        md5s = [MMZero3ProcedurePatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)
