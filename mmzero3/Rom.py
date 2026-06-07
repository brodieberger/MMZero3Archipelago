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
    if world.options.reward_notification:
        disk_detection_loop(patch)
    EXSkill_chips_patch(patch)
    weapons_patch(patch)

    patch.write_file("token_data.bin", patch.get_token_binary())

def general_changes_patch(patch: MMZero3ProcedurePatch) -> None:
    # Prevent disks from being opened in mission complete screen
    patch.write_token(
        APTokenTypes.WRITE,
        0x24B4B,
        bytes([0xE0]),
    )
    # Make disks display as locked in mission complete screen.
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

    # Collecting subtanks no longer rewards them to the player, sets RAM address 0203733D to be 1/2 instead.
    # 0xE0882 - 0xE08AF (46 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0xE0882,
        bytes([
            0x01, 0x20,              # mov r0,#0x1
            0x02, 0x49,              # ldr r1,[0x080e0890]
            0x08, 0x70,              # strb r0,[r1,#0x0]
            0x00, 0x00,              # mov r0,r0
            0x00, 0x00,              # mov r0,r0
            0x00, 0x00,              # mov r0,r0
            0x0F, 0xE0,              # b 0x080e08b0
            0x3D, 0x73, 0x03, 0x02,  # PTR_gGameState.save.unused_240[9]_080e0890: 0203733d
            0xC0, 0xF5, 0x02, 0x02,  # PTR_pZero2_080e0894: 0202f5c0
            0x08, 0x28,              # cmp r0,#0x8
            0x09, 0xD1,              # bne 0x080e08b0
            0x02, 0x20,              # mov r0,#0x2
            0x03, 0x49,              # ldr r1,[0x080e08ac]
            0x08, 0x70,              # strb r0,[r1,#0x0]
            0x05, 0xE0,              # b 0x080e08b0
            0x00, 0x00,              # mov r0,r0
            0x00, 0x00,              # mov r0,r0
            0x00, 0x00,              # mov r0,r0
            0x00, 0x00,              # mov r0,r0
            0x3D, 0x73, 0x03, 0x02,  # PTR_gGameState.save.unused_240[9]_080e08ac: 0203733d
        ]),
    )

    # Branch on game start (to force sync)
    patch.write_token(
        APTokenTypes.WRITE,
        0x0B3CA,
        bytes([0xFA,0xF0,0x77,0xFD]),
    )

    # 0x105EBC - 0x105ECB (16 bytes)
    patch.write_token(
    APTokenTypes.WRITE,
    0x105EBC,
    bytes([
        0x02, 0x48,              # ldr r0,[0x08105ec8]
        0x00, 0x70,              # strb r0,[r0,#0x0]
        0x90, 0x20,              # mov r0,#0x90
        0x40, 0x02,              # lsl r0,r0,#0x9
        0xF7, 0x46,              # mov pc,lr
        0x00, 0x00,              # mov r0,r0
        0x42, 0x73, 0x03, 0x02,  # PTR_gGameState.save.unused_240[14]_08105ec8: 02037342
    ]),
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
    # 0x105D50 - 0x105D6B (28 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105D50,
        bytes([
            0x0C, 0x48,              # ldr r0,[0x08105d84]
            0x00, 0x78,              # ldrb r0,[r0,#0x0]
            0x01, 0x28,              # cmp r0,#0x1
            0x01, 0xD0,              # beq 0x08105d5c
            0x10, 0x28,              # cmp r0,#0x10
            0x04, 0xD1,              # bne 0x08105d66
            0x01, 0x20,              # mov r0,#0x1
            0xFE, 0xF6, 0xDD, 0xFC,  # bl 0x0800471c
            0xEE, 0xF7, 0x97, 0xFB,  # bl 0x080f4494
            0xEE, 0xF7, 0x31, 0xFB,  # bl 0x080f43cc
            0xF7, 0x46,              # mov pc,lr
        ]),
    )

    # Custom code block 2. Checks if player can leave the level. Renders the appropriate text.
    # 0x105D6C - 0x105DAD (66 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105D6C,
        bytes([
            0x05, 0x48,              # ldr r0,[0x08105d84]
            0x00, 0x78,              # ldrb r0,[r0,#0x0]
            0x01, 0x28,              # cmp r0,#0x1
            0x04, 0xD0,              # beq 0x08105d7e
            0x10, 0x28,              # cmp r0,#0x10
            0x02, 0xD0,              # beq 0x08105d7e
            0x04, 0x48,              # ldr r0,[0x08105d8c]
            0xEF, 0xF7, 0xF7, 0xFA,  # bl 0x080f536c
            0x02, 0x48,              # ldr r0,[0x08105d88]
            0xEF, 0xF7, 0xF4, 0xFA,  # bl 0x080f536c
            0x64, 0x01, 0x03, 0x02,  # PTR_gMission.currentStageID_08105d84: 02030164
            0x90, 0x5D, 0x10, 0x08,  # PTR_text_you_cant_escape_this_level_08105d88: 08105d90
            0x1B, 0x0C, 0x37, 0x08,  # PTR_text_abort_completed_missions_08105d8c: 08370c1b
            # text_you_cant_escape_this_level
            0x23, 0x33, 0x39, 0x00, 0x27, 0x25, 0x32, 0xD0, 0x38, 0x00, 0x29, 0x37, 0x27, 0x25, 0x34, 0x29, 0x00, 0x38, 0x2C, 0x2D, 0x37, 0x00, 0x30, 0x29, 0x3A, 0x29, 0x30, 0xCA, 0xFF,
            0x00,                    # 00h
        ]),
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
    """Separates in game inventory (items collected by player) and Cervau inventory (items awarded by AP)
    
    Note: In RAM, there are two structs that store the players inventory. The first inventory is the disks the player has collected and what the player has opened using Cervau. After that block there is another struct that copies the first as a backup in case the player dies and needs to have their inventory wiped. This backup struct is overwritten here to be used for archipelago purposes."""
    
    # When disk analysis screen is opened, replace inventory pointer to AP inventory
    patch.write_token(
        APTokenTypes.WRITE,
        0xF7976,
        bytes([0x0E, 0xF0, 0x53, 0xFA]),
    )

    # 0x105E20 - 0x105E33 (20 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105E20,
        bytes([
            0x57, 0x46,              # mov r7,r10
            0x4E, 0x46,              # mov r6,r9
            0x02, 0x4D,              # ldr r5,[0x08105e30]
            0x01, 0x4C,              # ldr r4,[0x08105e2c]
            0x25, 0x60,              # str r5,[r4,#0x0]
            0xF7, 0x46,              # mov pc,lr
            0x90, 0xDF, 0x03, 0x02,  # PTR_gStageDiskManager_08105e2c: 0203df90
            0xE8, 0x71, 0x03, 0x02,  # PTR_gGameState.save.savedDisk[3]_08105e30: 020371e8
        ]),
    )

    # When disk analysis screen is closed, return to normal inventory pointer
    patch.write_token(
        APTokenTypes.WRITE,
        0xF7F42,
        bytes([0x0D, 0xF0, 0x77, 0xFF]),
    )

    # 0x105E34 - 0x105E47 (20 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105E34,
        bytes([
            0x04, 0x1C,              # add r4,r0,#0x0
            0x40, 0x20,              # mov r0,#0x40
            0x01, 0x49,              # ldr r1,[0x08105e40]
            0x02, 0x4A,              # ldr r2,[0x08105e44]
            0x0A, 0x60,              # str r2,[r1,#0x0]
            0xF7, 0x46,              # mov pc,lr
            0x90, 0xDF, 0x03, 0x02,  # PTR_gStageDiskManager_08105e40: 0203df90
            0xB8, 0x71, 0x03, 0x02,  # PTR_inventory_start_08105e44: 020371b8
        ]),
    )

    # No Ops branches that saves current inventory to back up inventory.
    patch.write_token(
        APTokenTypes.WRITE,
        0x1A0F2,
        bytes([0x00, 0x00, 0x00, 0x00]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0x1A100,
        bytes([0x00, 0x00, 0x00, 0x00]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xEF31E,
        bytes([0x00, 0x00, 0x00, 0x00]),
    )

    patch.write_token(
        APTokenTypes.WRITE,
        0xEF32C,
        bytes([0x00, 0x00, 0x00, 0x00]),
    )

def disk_collection_npc_patch(patch: MMZero3ProcedurePatch) -> None:
    """When player collects disk from NPC, record dialogue ID and save to RAM address 20371E6"""
    
    # Branch at the end of the dialogue function
    patch.write_token(
        APTokenTypes.WRITE,
        0xD971A,
        bytes([0x2C, 0xF0, 0x48, 0xFB]),
    )

    # Record dialogue ID to memory address 20371E6 
    # 0x105DAE - 0x105DBB (14 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105DAE,
        bytes([
            0x68, 0x73,              # strb r0,[r5,#0xd]
            0xA8, 0x73,              # strb r0,[r5,#0xe]
            0x01, 0x48,              # ldr r0,[0x08105db8]
            0x01, 0x80,              # strh r1,[r0,#0x0]
            0xF7, 0x46,              # mov pc,lr
            0xE6, 0x71, 0x03, 0x02,  # PTR_gGameState.save.savedDisk[1]_08105db8: 020371e6
        ]),
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
    # 0x105DE2 - 0x105E1F (62 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105DE2,
        bytes([
            0x00, 0xB5,              # push {lr}
            0x58, 0x68,              # ldr r0,[r3,#0x4]
            0x60, 0x61,              # str r0,[r4,#0x14]
            0x09, 0x4C,              # ldr r4,[0x08105e10]
            0x20, 0x78,              # ldrb r0,[r4,#0x0]
            0x00, 0x28,              # cmp r0,#0x0
            0x00, 0xD1,              # bne 0x08105df2
            0x00, 0xBD,              # pop {pc}
            0x00, 0x25,              # mov r5,#0x0
            0x25, 0x70,              # strb r5,[r4,#0x0]
            0x05, 0x00,              # mov r5,r0
            0xAD, 0x00,              # lsl r5,r5,#0x2
            0x46, 0x00,              # lsl r6,r0,#0x1
            0xAD, 0x19,              # add r5,r5,r6
            0x06, 0x48,              # ldr r0,[0x08105e18]
            0x40, 0x19,              # add r0,r0,r5
            0x04, 0x4D,              # ldr r5,[0x08105e14]
            0x28, 0x60,              # str r0,[r5,#0x0]
            0x05, 0x48,              # ldr r0,[0x08105e1c]
            0xE5, 0x21,              # mov r1,#0xe5
            0xE4, 0xF7, 0xDD, 0xF9,  # bl 0x080ea1c8
            0x00, 0xBD,              # pop {pc}
            0xE5, 0x71, 0x03, 0x02,  # PTR_ap_item_received_address_08105e10: 020371e5
            0xE4, 0x0B, 0x03, 0x02,  # PTR_disk_number_to_render_address_08105e14: 02030be4
            0x5E, 0x2D, 0x37, 0x08,  # PTR_Begin_Number_Text_Table_08105e18: 08372d5e
            0x00, 0x01, 0x00, 0x00,  # INT_08105e1c: 100h
        ]),
    )

    # Shorten text string so it all fits on one line.
    patch.write_token(
        APTokenTypes.WRITE,
        0x376969,
        bytes([0x00]),
    )

def EXSkill_chips_patch(patch: MMZero3ProcedurePatch) -> None:
    """Prevents EXSkills and Chips from being rewarded by the game, so that they can be rewarded by Archipelago instead."""
    
    # NO OP Reward Chip
    patch.write_token(
        APTokenTypes.WRITE,
        0x2437C,
        bytes([0x00,0xF0,0x00,0x00]),
    )

    # NO OP EX Skill
    patch.write_token(
        APTokenTypes.WRITE,
        0x24392,
        bytes([0x00,0x00,0x00,0x00]),
    )     
    
    # Branches to custom code on using rank changing cyber elf.
    patch.write_token(
        APTokenTypes.WRITE,
        0xe34ac,
        bytes([0x22, 0xF0, 0x86, 0xFC]),
    ) 

    # Saves cyber elf usage into memory address 0203733c
    # 0x105DBC - 0x105DCB (16 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105DBC,
        bytes([
            0x05, 0x20,              # mov r0,#0x5
            0x48, 0x70,              # strb r0,[r1,#0x1]
            0x01, 0x49,              # ldr r1,[0x08105dc8]
            0x01, 0x20,              # mov r0,#0x1
            0x08, 0x70,              # strb r0,[r1,#0x0]
            0xF7, 0x46,              # mov pc,lr
            0x3C, 0x73, 0x03, 0x02,  # PTR_gGameState.save.unused_240[8]_08105dc8: 0203733c
        ]),
    )

def weapons_patch(patch: MMZero3ProcedurePatch) -> None:
    
    # Branches from function that renders weapon icons
    patch.write_token(
        APTokenTypes.WRITE,
        0xE5A76,
        bytes([0x20,0xF0,0xF9,0xF9]),
    )

    # Renders weapon icons as locked or unlocked based on AP items
    # 0x105E6C - 0x105E97 (44 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105E6C,
        bytes([
            0x02, 0xB5,              # push {r1,lr}
            0xFF, 0x22,              # mov r2,#0xff
            0x0A, 0x40,              # and r2,r1
            0x08, 0x4B,              # ldr r3,[0x08105e94]
            0x9B, 0x5C,              # ldrb r3,[r3,r2]
            0x01, 0x2B,              # cmp r3,#0x1
            0x05, 0xD0,              # beq 0x08105e86
            0x02, 0xBC,              # pop {r1}
            0x04, 0x49,              # ldr r1,[0x08105e90]
            0x00, 0x00,              # mov r0,r0
            0x11, 0xF7, 0x3E, 0xFC,  # bl 0x08017700
            0x02, 0xE0,              # b 0x08105e8c
            0x02, 0xBC,              # pop {r1}
            0x11, 0xF7, 0x3A, 0xFC,  # bl 0x08017700
            0x08, 0xBC,              # pop {r3}
            0x18, 0x47,              # bx r3
            0x06, 0x0E,              # WORD_08105e90: E06h
            0x00,                    # 00h
            0x00,                    # 00h
            0x3E, 0x73, 0x03, 0x02,  # PTR_gGameState.save.unused_240[10]_08105e94: 0203733e
        ]),
    )


    # Branches from main weapon selection function
    patch.write_token(
        APTokenTypes.WRITE,
        0xF4564,
        bytes([0x11,0xF0,0x70,0xFC,0x02,0x20,0x00,0x00,0x00,0x00,0x43,0xe0]),
    )

    # Handles logic for selecting main weapon
    # 0x105E48 - 0x105E6B (36 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105E48,
        bytes([
            0x00, 0xB5,              # push {lr}
            0x07, 0x48,              # ldr r0,[0x08105e68]
            0x80, 0x5C,              # ldrb r0,[r0,r2]
            0x01, 0x28,              # cmp r0,#0x1
            0x05, 0xD1,              # bne 0x08105e5e
            0x0A, 0x73,              # strb r2,[r1,#0xc]
            0x02, 0x20,              # mov r0,#0x2
            0xFE, 0xF6, 0x61, 0xFC,  # bl 0x0800471c
            0x08, 0xBC,              # pop {r3}
            0x18, 0x47,              # bx r3
            0x03, 0x20,              # mov r0,#0x3
            0xFE, 0xF6, 0x5C, 0xFC,  # bl 0x0800471c
            0x08, 0xBC,              # pop {r3}
            0x18, 0x47,              # bx r3
            0x3E, 0x73, 0x03, 0x02,  # PTR_gGameState.save.unused_240[10]_08105e68: 0203733e
        ]),
    )

    # Branches from sub weapon selection function. No Op other code.
    patch.write_token(
        APTokenTypes.WRITE,
        0xF46C0,
        bytes([0x11,0xF0,0xEA,0xFB, 0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x43, 0xe0]),
    )

    # Handles logic for selecting sub weapon
    # 0x105E98 - 0x105EBB (36 bytes)
    patch.write_token(
        APTokenTypes.WRITE,
        0x105E98,
        bytes([
            0x00, 0xB5,              # push {lr}
            0x07, 0x48,              # ldr r0,[0x08105eb8]
            0x80, 0x5C,              # ldrb r0,[r0,r2]
            0x01, 0x28,              # cmp r0,#0x1
            0x05, 0xD1,              # bne 0x08105eae
            0x4A, 0x73,              # strb r2,[r1,#0xd]
            0x02, 0x20,              # mov r0,#0x2
            0xFE, 0xF6, 0x39, 0xFC,  # bl 0x0800471c
            0x08, 0xBC,              # pop {r3}
            0x18, 0x47,              # bx r3
            0x03, 0x20,              # mov r0,#0x3
            0xFE, 0xF6, 0x34, 0xFC,  # bl 0x0800471c
            0x08, 0xBC,              # pop {r3}
            0x18, 0x47,              # bx r3
            0x3E, 0x73, 0x03, 0x02,  # PTR_gGameState.save.unused_240[10]_08105eb8: 0203733e
        ]),
    )

    # Equips buster into both slots when game begins (temp fix)
    patch.write_token(
        APTokenTypes.WRITE,
        0x322BE,
        bytes([0x42,0x73]),
    )

    # Makes all weapons collected by default (weapon unlocking no longer handled by game)
    patch.write_token(
        APTokenTypes.WRITE,
        0x322DA,
        bytes([0x0F,0x20]),
    )

    

class MMZero3Settings(settings.Group):
    class MMZero3RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 3 (USA) """
        required = True
        description = "Mega Man Zero 3 (USA) ROM File"
        copy_to = "Mega Man Zero 3 (USA).gba"
        md5s = [MMZero3ProcedurePatch.hash]


    rom_file: MMZero3RomFile = MMZero3RomFile(MMZero3RomFile.copy_to)