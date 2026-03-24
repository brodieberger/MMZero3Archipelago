from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from .Options import MMZero3Options
from worlds._bizhawk.client import BizHawkClient

from .Data import *

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from . import MMZero3World

class MMZero3Client(BizHawkClient):
    game = "Mega Man Zero 3"
    system = "GBA"
    patch_suffix = ".apmmzero3"

    prev_level_value = None
    in_results_screen = False
    player_warned = False
    
    cerveau_inventory = bytearray(45)
    disks_found = bytearray(10)
    dialogue_id = bytearray(2)

    options_set = False
    required_disks = 80 # Will be overwritten from settings
    goal_type = 0 # will also be overwritten. 0 is for default (kill boss with enough disks), 1 is vanilla (just kill the boss)
    easy_ex_skill = 0
    
    received_index = 0
    collected_disks = 0

    eReader_bitflag_inventory = [0] * 12 
    eReader_byte_map_inventory = [0] * 10
    ex_skill_inventory = bytearray(2)
    body_inventory = bytearray([0x01])
    foot_inventory = bytearray([0x01])
    

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x0a0, 12, "ROM")]))[0]).decode("ascii")
            if rom_name != "MEGAMANZERO3":
                return False  # Not a Mega Man Zero 3 ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        ctx.game = self.game
        ctx.items_handling = 0b011 # gets items from other worlds and OWN world
        ctx.want_slot_data = True

        return True

    # TODO: This function could probably be split/optimized
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            # Set the required amount of secret disks
            if ctx.slot_data and not self.options_set:
                self.required_disks = ctx.slot_data.get("required_secret_disks", 80)
                self.goal_type = ctx.slot_data.get("goal", 0)
                self.easy_ex_skill = ctx.slot_data.get("easy_ex_skill", 0)
                self.options_set = True

            # Disks found in level
            disks_found = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x3DF94, 10, "Combined WRAM")])
            )[0]

            # Most recent npc dialogue. Used to reward items
            dialogue_id = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x371E6, 2, "Combined WRAM")])
            )[0]
            
            # Read current level
            level_data = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x030164, 1, "Combined WRAM")] 
            ))[0]

            # AP inventory used in disk analysis screen
            self.cerveau_inventory = bytearray((await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0371E8, 45, "Combined WRAM")]
            ))[0])

            # Read if the player is in results screen
            results_screen = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x030165, 1, "Combined WRAM")] 
            ))[0]

            # Read if player is in demo screen
            demo_screen = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x042AE2, 1, "Combined WRAM")] 
            ))[0]

            # Will be changed to true if the gamestate needs to be syncronised.
            # Either on some update or the player changing stages.
            needs_sync = False
            
            # When the player loads into the hub or a level, it should sync the inventory
            is_in_hub = level_data.hex() in ('11', '00')
            if self.prev_level_value != is_in_hub:
                needs_sync = True

            # Check if an item was picked up in a level
            if disks_found != self.disks_found and demo_screen != b'\x00':
                new_locations = []

                for old, new in zip(self.disks_found, disks_found):
                    if old == 0xFF and new != 0xFF:
                        new_locations.append(new+1)

                if new_locations:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": new_locations
                    }])

                    #needs_sync = True

                self.disks_found = disks_found

            # Check if an NPC has given a disk (or is talked to after their reward period is expired)
            if dialogue_id != self.dialogue_id:

                new_dialogue = int.from_bytes(dialogue_id, "little")
                location = DIALOGUE_LOCATION_MAP.get(new_dialogue)

                if location is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [location]
                    }])

                self.dialogue_id = dialogue_id

            # Check if the player has completed a level
            # TODO: This method of checking is prone to breaking using savestates
            if results_screen != b'\x00' and not self.in_results_screen:
                current_level = int.from_bytes(level_data, byteorder='little')
                location_id = LEVEL_TO_LOCATION.get(current_level)

                if location_id:

                    # Send completion item
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [location_id]
                    }]) 

                    if LOCATION_TO_CHIP.get(location_id):
                        # Send necessary chip
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": [LOCATION_TO_CHIP.get(location_id)]
                        }]) 
                    
                    if await self.should_reward_exskill(ctx) or self.easy_ex_skill == 1:
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": [LOCATION_TO_EXSKILL.get(location_id)]
                        }]) 

                # Completion condition. Runs If the level that was finished was the last level
                # Logic for Default game goal
                if self.goal_type == 0:
                    if level_data == b'\x10' and self.collected_disks >= self.required_disks and not ctx.finished_game:
                        await ctx.send_msgs([{
                            "cmd": "Say", "text": f"Final stage cleared! You had {self.collected_disks} Disks, which was {self.collected_disks - self.required_disks} more disks than needed!"
                            }])
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                    elif level_data == b'\x10' and self.collected_disks < self.required_disks and not self.player_warned and not ctx.finished_game:
                        await ctx.send_msgs([
                            {"cmd": "Say", "text": f"Final stage cleared! You still need {self.required_disks - self.collected_disks} more disks."},
                            {"cmd": "Say", "text": "Load a previous save and collect more disks."},
                            {"cmd": "Say", "text": "Do NOT save over your file after the credits!"}
                        ])
                        self.player_warned = True
                # Logic for Vanilla
                elif self.goal_type == 1:
                        if level_data == b'\x10' and ctx.finished_game == False:
                            await ctx.send_msgs([{
                                "cmd": "Say", "text": "Final Stage Cleared! Game completed!"
                                }])
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                    
                self.in_results_screen = True

            # Additional check to see if the player collected enough disks AFTER beating final stage. Only used in default game goal
            if self.player_warned == True and self.collected_disks >= self.required_disks and ctx.finished_game == False:
                await ctx.send_msgs([{
                    "cmd": "Say", "text": f"{self.required_disks} Disks collected! Game completed!"
                }])
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

            # Receive an item from AP
            for i in range(self.received_index, len(ctx.items_received)):
                needs_sync = True
                item = ctx.items_received[i]

                # Disk items
                if 1 <= item.item <= 180:
                    disk_number = item.item - 1           # 0-based index
                    byte_index = disk_number // 4         # which byte
                    disk_in_byte = disk_number % 4        # which nibble in byte

                    # Calculate the mask for the "found" bit
                    found_mask = 1 << disk_in_byte       # 0x01, 0x02, 0x04, 0x08

                    # Update inventory: only the found bit, everything else untouched
                    self.cerveau_inventory[byte_index] |= found_mask

                    self.collected_disks += 1

                    # Send notification to player
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x0371E5, [item.item], "Combined WRAM")]
                    )

                # If the item is an eReader bitflag item
                if item.item >= 111 and item.item <= 140:
                    if item.item not in BIT_FLAGS:
                        continue
                    word_index, bit = BIT_FLAGS[item.item]

                    byte_index = word_index * 2
                    mask = 1 << (bit - 1) 

                    if bit <= 8:
                        self.eReader_bitflag_inventory[byte_index]     |= mask
                    else:
                        self.eReader_bitflag_inventory[byte_index + 1] |= (mask >> 8)

                # If the item is an eReader byte map item
                if item.item in BYTE_MAP:
                    addr, value = BYTE_MAP[item.item]
                    self.eReader_byte_map_inventory[addr - 0x02474] = value
        
                # EX Skills
                if item.item in EX_SKILL_MAP:
                    byte_index, mask = EX_SKILL_MAP[item.item]
                    self.ex_skill_inventory[byte_index] |= mask

                # Body Chips
                if item.item in BODY_CHIP_MAP:
                    byte_index, mask = BODY_CHIP_MAP[item.item]
                    self.body_inventory[byte_index] |= mask

                # Foot Chips
                if item.item in FOOT_CHIP_MAP:
                    byte_index, mask = FOOT_CHIP_MAP[item.item]

                    self.foot_inventory = bytearray((await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [(0x03806d, 1, "Combined WRAM")] 
                    ))[0])

                    self.foot_inventory[byte_index] |= mask

            self.received_index = len(ctx.items_received)

            if needs_sync:
                await self.sync_game_state(ctx)
            self.prev_level_value = is_in_hub

            self.disks_found = disks_found
            self.dialogue_id = dialogue_id

        except bizhawk.RequestFailedError:
            pass

    def get_items(self, ctx) -> bytearray:
        """Updates items collected by Zero based on ctx.checked_locations. Used in case of player using savestates. 
        Only lower nibble (found state) is updated. Upper nibble (opened state) is untouched."""

        inventory = bytearray(45)

        for location_id in ctx.checked_locations:
            if 1 <= location_id <= 180:
                item_index = location_id - 1
                byte_index = item_index // 4
                bit_position = item_index % 4

                # Only set the lower nibble bit (bit positions 0–3)
                inventory[byte_index] |= (1 << bit_position)

        return inventory
    
    async def should_reward_exskill(self, ctx) -> bool:
        """Determine if an EX Skill should be rewarded after a level."""

        level_rank, elf_flag = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (0x30165, 1, "Combined WRAM"),
                (0x3733C, 1, "Combined WRAM"),
            ]
        )
        if level_rank[0] > 85:
            return True

        # If the player has used a rank increasing cyber elf
        if elf_flag[0] == 0x01:
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x3733C, [0], "Combined WRAM")]
            )
            return True

        return False

    async def sync_game_state(self, ctx) -> None:
        """Syncronizes the player's collected items and inventory in order to prevent desyncs when using savestates.
        
        Done whenever the player collects or receives an item, or transitions between stages."""

        self.in_results_screen = False

        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(0x0371E8, list(self.cerveau_inventory), "Combined WRAM")]
        )
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(0x0371B8, list(self.get_items(ctx)), "Combined WRAM")]
        )
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(0x02438, list(self.eReader_bitflag_inventory), "Combined WRAM")]
        )
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(0x02474, self.eReader_byte_map_inventory, "Combined WRAM")]
        )
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(0x038068, self.ex_skill_inventory, "Combined WRAM")]
        )
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(0x03806C, self.body_inventory, "Combined WRAM")]
        )
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(0x03806D, self.foot_inventory, "Combined WRAM")]
        )
