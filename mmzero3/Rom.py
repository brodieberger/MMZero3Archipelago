from dataclasses import dataclass
import os
import Utils
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import TYPE_CHECKING, Optional
from settings import get_settings
import settings
import json

if TYPE_CHECKING:
    from . import MMZero3World


class MMZero3ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mega Man Zero 3"
    hash = "aa1d5eeffcd5e4577db9ee6d9b1100f9"
    patch_file_ending = ".apmmzero3"
    result_file_ending = ".gba"

    # BSDIFF file is exclusively sprite edits. ASM changes are found in the write_tokens function.
    procedure = [
        ("apply_bsdiff4", ["mmz3-ap.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        file_name = get_settings().MMZero3_settings["rom_file"]
        if not os.path.exists(file_name):
          file_name = Utils.user_path(file_name)
        with open(file_name, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes

def write_tokens(world: "MMZero3World", patch: MMZero3ProcedurePatch) -> None:

    # Prevent disks from being opened in mission complete screen
    patch.write_token(
        APTokenTypes.WRITE,
        0x24B4B,
        bytes([0xE0]),
    )
    # Make disks show up greyed out in mission complete screen.
    # TODO: 0xE78F6 does something that I did not document, 01 78 > 00 20
    #  probably something related to text changes?
    patch.write_token(
        APTokenTypes.WRITE,
        0xE78D0,
        bytes([0xFF, 0x21]),
    )

    # Allow opening cutscenes to be skippable.
    patch.write_token(
        APTokenTypes.WRITE,
        0x236EE,
        bytes([0x00, 0x00]),
    )

    # PATCH: CHECK IF PLAYER CAN LEAVE LEVEL ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Jump to custom code block 1 on level exit, which is written to a chunk of unused ROM.
    patch.write_token(
        APTokenTypes.WRITE,
        0xF43DE,
        bytes([0x11, 0xF0, 0xB7, 0xFC]),
    )

    # Jump to custom code block 2 on hovering over level exit button, also written to unused ROM.
    patch.write_token(
        APTokenTypes.WRITE,
        0xF51F4,
        bytes([0x10, 0xF0, 0xBA, 0xFD]),
    )

    # Custom code block 1. Checks if player can leave the level. If so, leaves; If not, plays error sound.
    patch.write_token(
        APTokenTypes.WRITE,
        0x105D50,
        bytes([0x0c, 0x48, 0x00, 0x78, 0x01, 0x28, 0x01, 0xD0, 0x06, 0x28, 0x04, 0xD1, 0x01, 0x20, 0xFE, 0xF6, 0xDD, 0xFC, 0xEE, 0xF7, 0x97, 0xFB, 0xEE, 0xF7, 0x31, 0xFB, 0x00, 0x00]),
    )

    # Custom code block 2. Checks if player can leave the level. Renders the appropriate text.
    patch.write_token(
        APTokenTypes.WRITE,
        0x105D6C,
        bytes([0x05, 0x48, 0x00, 0x78, 0x01, 0x28, 0x04, 0xD0, 0x06, 0x28, 0x02, 0xD0, 0x04, 0x48, 0xEF, 0xF7, 0xF7, 0xFA, 0x02, 0x48, 0xEF, 0xF7, 0xF4, 0xFA, 0x64, 0x01, 0x03, 0x02, 0x90, 0x5D, 0x10, 0x08, 0x1B, 0x0C, 0x37, 0x08, 0x23, 0x33, 0x39, 0x00, 0x27, 0x25, 0x32, 0xD0, 0x38, 0x00, 0x29, 0x37, 0x27, 0x25, 0x34, 0x29, 0x00, 0x38, 0x2C, 0x2D, 0x37, 0x00, 0x30, 0x29, 0x3A, 0x29, 0x30, 0xCA, 0xFF]),
    )

    # Prevents text from changing when you are not allowed to exit level.
    patch.write_token(
        APTokenTypes.WRITE,
        0xF535E,
        bytes([0x00, 0x00]),
    )

    # Replaces text when hovering over exit level button while in exitable level.
    # Abort Completed Missions -> Press A to return to hub.
    patch.write_token(
        APTokenTypes.WRITE,
        0x370C1B,
        bytes([0x1A, 0x36, 0x29, 0x37, 0x37, 0x00, 0x0B, 0x00, 0x38, 0x33, 0x00, 0x36, 0x29, 0x38, 0x39, 0x36, 0x32, 0x00, 0x38, 0x33, 0x00, 0x2C, 0x39, 0x26, 0xE5, 0xFF]),
    )

    # Replaces text when hovering over exit level button while NOT in exitable level.
    # You can't escape now! -> You can't escape this level!
    patch.write_token(
        APTokenTypes.WRITE,
        0x370C63,
        bytes([0x2C, 0x29, 0x36, 0x29]),
    )
    # PATCH OVER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    patch.write_file("token_data.bin", patch.get_token_binary())

class MMZero3Settings(settings.Group):
    class MMZero3RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 3 (USA) """
        required = True
        description = "Mega Man Zero 3 (USA) ROM File"
        copy_to = "Mega Man Zero 3 (USA).gba"
        md5s = [MMZero3ProcedurePatch.hash]


    rom_file: MMZero3RomFile = MMZero3RomFile(MMZero3RomFile.copy_to)