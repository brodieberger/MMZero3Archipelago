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
    general_changes_patch(patch)
    leave_level_patch(patch)
    separate_inventory_patch(patch)
    disk_collection_npc_patch(patch)
    disk_collection_item_patch(patch)
    disk_detection_loop(patch)

    patch.write_file("token_data.bin", patch.get_token_binary())

def general_changes_patch(patch: MMZero3ProcedurePatch) -> None:
    # Prevent disks from being opened in mission complete screen
    patch.write_token(
        APTokenTypes.WRITE,
        0x24B4B,
        bytes([0xE0]),
    )
    # Make disks show up greyed out in mission complete screen.
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

def leave_level_patch(patch: MMZero3ProcedurePatch) -> None:
    """Check if player can leave level. Allow them do to so or play error sound. Display the proper text."""
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

def separate_inventory_patch(patch: MMZero3ProcedurePatch) -> None:
    """Separates in game inventory (items collected by player) and Cervau inventory (items awarded by AP)"""
    # Note: In RAM, there are two structs that store the players inventory. The first inventory is the disks the player has collected
    # and what the player has opened using Cervau. After that block there is another struct that copies the first as a backup in case
    # the player dies and needs to have their inventory wiped. This backup struct is overwritten here to be used for archipelago purposes.
    
    # Changes a pointer, makes Cervau check backup inventory.
    patch.write_token(
        APTokenTypes.WRITE,
        0xEE198,
        bytes([0x48]),
    )

    # No Ops branch that saves current inventory to back up inventory.
    patch.write_token(
        APTokenTypes.WRITE,
        0x1A0F4,
        bytes([0x00, 0x00]),
    )

def disk_collection_npc_patch(patch: MMZero3ProcedurePatch) -> None:
    """When player collects disk from NPC, send collected item to memory location"""

    # Reroutes all NPC dialogues to custom code
    patch.write_token(
        APTokenTypes.WRITE,
        0xD93DE,
        bytes([0x2C, 0xF0, 0xE6, 0xFC]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xD9420,
        bytes([0x2C, 0xF0, 0xC5, 0xFC]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xD945C,
        bytes([0x2C, 0xF0, 0xA7, 0xFC]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xD94DA,
        bytes([0x2C, 0xF0, 0x87, 0xFC]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xD950E,
        bytes([0x2C, 0xF0, 0x4E, 0xFC]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xD9540,
        bytes([0x2C, 0xF0, 0x35, 0xFC]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xD9580,
        bytes([0x2C, 0xF0, 0x15, 0xFC]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xD95B6,
        bytes([0x2C, 0xF0, 0xFA, 0xFB]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xD95E8,
        bytes([0x2C, 0xF0, 0xE1, 0xFB]),
    )

    # Places AP item into the correct RAM location. Located right after the secret disk struct
    # Contains the item number (1-4) and offset.
    patch.write_token(
        APTokenTypes.WRITE,
        0x105DAE,
        bytes([0x08, 0xB5, 0x09, 0x4B, 0x18, 0x70, 0x10, 0x43, 0x08, 0x70, 0x59, 0x70, 0x00, 0x00, 0x08, 0xbc, 0x00, 0xbd]),
    )

def disk_collection_item_patch(patch: MMZero3ProcedurePatch) -> None:
    """When player collects disk item, send collected item to memory location"""

    # Reroutes to custom code on collecting disk
    patch.write_token(
        APTokenTypes.WRITE,
        0xF889C,
        bytes([0x0D, 0xF0, 0x90, 0xFA]),
    )

    # Places AP item into the correct RAM location. Located right after the secret disk struct
    patch.write_token(
        APTokenTypes.WRITE,
        0x105DC0,
        bytes([0x10, 0xB5, 0x05, 0x4C, 0x20, 0x70, 0x08, 0x43, 0x10, 0x70, 0x04, 0x49, 0x51, 0x1A, 0x61, 0x70, 0x00, 0x00, 0x10, 0xBC, 0x00, 0xBD, 0x70, 0x47, 0xE5, 0x71, 0x03, 0x02, 0xB8, 0x71, 0x03, 0x02]),
    )

def disk_detection_loop(patch: MMZero3ProcedurePatch) -> None:
    """On AP item retreival, play sound and display info box"""

    # Reroutes to custom code on AP item getting placed into memory by client.py
    patch.write_token(
        APTokenTypes.WRITE,
        0x4886,
        bytes([0x01, 0xF1, 0xAC, 0xFA]),
    )

    # play sound and display info box
    patch.write_token(
        APTokenTypes.WRITE,
        0x105DE2,
        bytes([0x00, 0xB5, 0x58, 0x68, 0x60, 0x61, 0x09, 0x4c, 0x20, 0x78, 0x00, 0x28, 0x00, 0xd1, 0x00, 0xbd, 0x00, 0x25, 0x25, 0x70, 0x05, 0x00, 0xad, 0x00, 0x46, 0x00, 0xad, 0x19, 0x06, 0x48, 0x40, 0x19, 0x04, 0x4d, 0x28, 0x60, 0x05, 0x48, 0xe5, 0x21, 0xe4, 0xf7, 0xdd, 0xf9, 0x00, 0xbd, 0x15, 0x72, 0x03, 0x02, 0xe4, 0x0b, 0x03, 0x02, 0x5E, 0x2D, 0x37, 0x08, 0x00, 0x01]),
    )

class MMZero3Settings(settings.Group):
    class MMZero3RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 3 (USA) """
        required = True
        description = "Mega Man Zero 3 (USA) ROM File"
        copy_to = "Mega Man Zero 3 (USA).gba"
        md5s = [MMZero3ProcedurePatch.hash]


    rom_file: MMZero3RomFile = MMZero3RomFile(MMZero3RomFile.copy_to)