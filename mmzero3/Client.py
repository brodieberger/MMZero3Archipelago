from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from .Options import MMZero3Options
from worlds._bizhawk.client import BizHawkClient

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
    
    cervau_inventory = bytearray(45)

    required_disks = 80 # Will be overwritten from settings
    goal_type = 0 # will also be overwritten. 0 is for default (kill boss with enough disks), 1 is vanilla (just kill the boss)
    easy_ex_skill = 0
    
    options_set = False
    received_index = 0
    collected_disks = 0

    level_to_location = {
        0x01: 181,  # spacecraft
        0x02: 182,  # volcano base
        0x03: 183,  # highway
        0x04: 184,  # weapons repair factory
        0x05: 185,  # old residential
        0x06: 186,  # omega missile
        0x07: 187,  # twighlight desert
        0x08: 188,  # forest
        0x09: 189,  # ice base
        0x0A: 190,  # area x2
        0x0B: 191,  # energy facility
        0x0C: 192,  # snowy plaiuns
        0x0D: 193,  # sunken library
        0x0E: 194,  # giant elevator
        0x0F: 195,  # sub arcadia
        0x10: 196,  # final level
    }


    # eReader content memory array
    eReader_bitflag_inventory = [0] * 12 

    # eReader byte-map inventory (10 bytes covering IDs 141–180)
    eReader_byte_map_inventory = [0] * 10

    # Bitflags for eReader content. AP Item ID -> (word_index, bit_position)
    bitflags = {
        111: (0, 1),
        112: (0, 6),
        113: (0, 7),
        114: (0, 10),
        115: (1, 1),
        117: (1, 4),
        118: (1, 10),
        119: (1, 12),
        120: (1, 13),
        121: (1, 15),
        122: (2, 2),
        123: (2, 4),
        124: (2, 5),
        125: (2, 7),
        126: (2, 8),
        127: (2, 13),
        128: (2, 15),
        129: (3, 4),
        130: (3, 5),
        131: (3, 7),
        132: (3, 8),
        133: (3, 10),
        134: (3, 13),
        135: (4, 2),
        136: (4, 11),
        137: (4, 13),
        138: (5, 3),
        139: (5, 5),
        140: (5, 6),
    }

    # Byte map for for eReader content. AP Item ID -> (Ram Address, Value)
    byte_map = {
        # Dialogue Window (0x2002474)
        141: (0x02474, 0x01),
        142: (0x02474, 0x02),
        143: (0x02474, 0x03),
        144: (0x02474, 0x04),
        145: (0x02474, 0x05),
        146: (0x02474, 0x06),
        147: (0x02474, 0x07),
        148: (0x02474, 0x08),

        # Title Screen Design (0x2002475)
        149: (0x02475, 0x01),
        150: (0x02475, 0x02),
        151: (0x02475, 0x03),
        152: (0x02475, 0x04),

        # Elevator Design (0x2002476)
        153: (0x02476, 0x01),
        154: (0x02476, 0x02),

        # Base Environment (0x2002477)
        155: (0x02477, 0x01),
        156: (0x02477, 0x02),

        # Ciel's Computer Design (0x2002478)
        157: (0x02478, 0x01),
        158: (0x02478, 0x02),
        159: (0x02478, 0x03),
        160: (0x02478, 0x04),

        # Life Pickup Design (0x2002479)
        161: (0x02479, 0x01),
        162: (0x02479, 0x02),

        # E-Crystals Design (0x200247A)
        163: (0x0247A, 0x01),
        164: (0x0247A, 0x02),

        # Z Plate Design (0x200247C)
        177: (0x0247C, 0x01),
        178: (0x0247C, 0x02),

        # Buster Shot Design (0x200247D)
        179: (0x0247D, 0x01),
        180: (0x0247D, 0x02),
    }

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
            
            # Retrieves update from game
            # First Byte: Bit representing item, Second Byte: Inventory Offset
            item_update = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0371E5, 2, "Combined WRAM")])
            )[0]
            
            # Read current level
            level_data = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x030164, 1, "Combined WRAM")] 
            ))[0]

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
            if item_update != b'\x00\x00' and demo_screen != b'\x00':
                await self.item_found(ctx, self.zero_inventory)
                needs_sync = True

            # Check if the player has completed a level
            # TODO: Make this use a similar system as the one for checking items
            if results_screen != b'\x00' and not self.in_results_screen:
                current_level = int.from_bytes(level_data, byteorder='little')
                location_id = self.level_to_location.get(current_level)

                if location_id:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [location_id]
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

                # If the item is a secret disk, add to cervau inventory
                if item.item >= 1 and item.item <= 180: 
                    item_index = item.item - 1  # Items are 1-indexed
                    byte_index = item_index // 4
                    bit_position = item_index % 4

                    # Update cervau inventory
                    self.cervau_inventory[byte_index] |= (1 << bit_position)
                    self.collected_disks += 1
            
                # If the item is an eReader bitflag item
                if item.item >= 111 and item.item <= 140:
                    if item.item not in self.bitflags:
                        continue
                    word_index, bit = self.bitflags[item.item]

                    byte_index = word_index * 2
                    mask = 1 << (bit - 1) 

                    if bit <= 8:
                        self.eReader_bitflag_inventory[byte_index]     |= mask
                    else:
                        self.eReader_bitflag_inventory[byte_index + 1] |= (mask >> 8)

                # If the item is an eReader byte map item
                if item.item in self.byte_map:
                    addr, value = self.byte_map[item.item]
                    self.eReader_byte_map_inventory[addr - 0x02474] = value

            self.received_index = len(ctx.items_received)

            if needs_sync:
                await self.sync_game_state(ctx)
            self.prev_level_value = is_in_hub

            # Needs to be read last in order to compare new items
            self.zero_inventory = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0371B8, 45, "Combined WRAM")])
            )[0]


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
        
    async def item_found(self, ctx, zero_inventory):
        """Find item that was picked up and send the location check for that item"""

        print("item found!")
        print(zero_inventory)

        new_save_data = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(0x0371B8, 45, "Combined WRAM")])
        )[0]
        print(new_save_data)

        new_locations = []
        for i in range(len(new_save_data)):
            # Only look at the lower nibble (0x0F mask)
            old_bits = zero_inventory[i] & 0x0F
            new_bits = new_save_data[i] & 0x0F

            changed_bits = new_bits & (~old_bits)  # Bits that were 0 and are now 1
            print(changed_bits)
            for bit in range(4):
                if changed_bits & (1 << bit):
                    location_id = i * 4 + bit + 1  # Items are 1-indexed
                    new_locations.append(location_id)

        print(new_locations)
        if new_locations:
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": new_locations
            }])

        # Clear update in memory now that it has been read
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(0x0371E5, [0,0], "Combined WRAM")]
        )

    async def sync_game_state(self, ctx):
        """Syncronizes the player's collected items and inventory."""
        
        self.synced_hub = False
        self.in_results_screen = False

        if self.easy_ex_skill == 1:
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x0372B1, [0x06], "Combined WRAM")]
            )

        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(0x0371E8, list(self.cervau_inventory), "Combined WRAM")]
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
