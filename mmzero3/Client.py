from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class MMZero3Client(BizHawkClient):
    game = "Mega Man Zero 3"
    system = "GBA"
    patch_suffix = ".apmmzero3"

    synced_in_game = False
    synced_hub = False
    in_game_inventory = bytearray(45)
    real_inventory = bytearray(45)
    empty_inventory = bytearray([0xFF] * 45)
    received_index = 0


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

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            # Read save data
            save_data = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0371B8, 45, "Combined WRAM")])
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
            
            # When the player loads into the hub or a level, it should sync the inventory
            # This value keeps track of that
            is_in_hub = level_data.hex() in ('11', '00')

            # IF THE PLAYER IS IN A LEVEL
            if not is_in_hub:
                # Reset hub sync flag
                self.synced_hub = False

                # Sync in-game inventory once on entering a level
                if not self.synced_in_game:
                    print("Entering Level, Starting Inventory Sync.")
                    print(f"Real Inventory :{self.real_inventory}")
                    print(f"In-Game Inventory :{self.in_game_inventory}")
                    print(f"RAM Inventory :{save_data}")
                    
                    # Sync in game inventory inventory once on entering level
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, list(self.in_game_inventory), "Combined WRAM")]
                    )

                    # Read save data again after writing it
                    save_data = (await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, 45, "Combined WRAM")])
                    )[0]

                    self.synced_in_game = True

                    # Unlocks Z Saber, just a temp thing here cause of my AP rules that I don't feel like changing ATM
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [999]
                    }])

                    print("Level Write Complete.")
                    print(f"Real Inventory :{self.real_inventory}")
                    print(f"In-Game Inventory :{self.in_game_inventory}")
                    print(f"RAM Inventory :{save_data}")

                # Check if an item was picked up in a level
                if save_data != self.in_game_inventory and results_screen == b'\x00':
                    #print("Item pickup detected!")

                    # Find item that you picked up and send the location check for that item, then update the in game inventory (not ram data)
                    new_locations = []
                    for i in range(len(save_data)):
                        # Only look at the lower nibble (0x0F mask I think)
                        old_bits = self.in_game_inventory[i] & 0x0F
                        new_bits = save_data[i] & 0x0F

                        changed_bits = new_bits & (~old_bits)  # Bits that were 0 and are now 1
                        for bit in range(4):
                            if changed_bits & (1 << bit):
                                location_id = i * 4 + bit + 1  # Items are 1-indexed
                                new_locations.append(location_id)

                    if new_locations:
                        #print(f"New Locations Found: {new_locations}")
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": new_locations
                        }])
                    #else:
                        #print("No new locations found.") # Player scanned a disk or loaded a save/savestate?
                    
                    # Update in game inventory to have the new item so it doesn't show again.
                    # TODO, this should be removed and replaced with logic that scans the
                    # AP inventory, then updates the in game inventory to match. That would make
                    # things less prone to breaking when the player uses save staes.
                    self.in_game_inventory = bytearray(save_data)

                # TODO, this should probably be in the locations.py file
                level_to_location = {
                    0x01: 181,  # spacecraft
                    0x02: 182,  # volcano base
                    0x03: 183,  # highway
                    0x04: 184,  # weapons repair factory
                    0x05: 185,  # old residential
                    0x06: 186,  # omega missile
                    0x07: 187,  # twighlight desert
                    0x08: 188,  # ice base
                    0x09: 189,  # forest
                    0x0A: 190,  # area x2
                    0x0B: 191,  # energy facility
                    0x0C: 192,  # snowy plaiuns
                    0x0D: 193,  # sunken library
                    0x0E: 194,  # giant elevator
                    0x0F: 195,  # sub arcadia
                    0x10: 196,  # final level
                }

                # Check if the player has completed a level
                if results_screen != b'\x00':
                    current_level = int.from_bytes(level_data, byteorder='little')
                    location_id = level_to_location.get(current_level)

                    if location_id:
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": [location_id]
                        }])
                    
                    # Fill player inventory so that player cant open items in result screen
                    print("Inventory Emptied")
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, list(self.empty_inventory), "Combined WRAM")]
                    )


            #IF THE PLAYER IS NOT IN A LEVEL
            else:
                # Reset level sync flag
                self.synced_in_game = False

                # Sync to real inventory once on entering hub
                if not self.synced_hub:
                    print("Entering hub, syncing inventory")
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, list(self.real_inventory), "Combined WRAM")]
                    )
                    self.synced_hub = True

            # receive an item from AP and add it to ram.
            # If in hub, add it to real inventory AND insert into memory, else just real inventory
            for i in range(self.received_index, len(ctx.items_received)):
                item = ctx.items_received[i]
                #print(f"AP Item Received: {item.item} (from player {item.player})")

                # If the item is a secret disk, add to real inventory
                if item.item >= 1 and item.item <= 180: 
                    item_index = item.item - 1  # Items are 1-indexed
                    byte_index = item_index // 4
                    bit_position = item_index % 4

                    # Update real inventory
                    self.real_inventory[byte_index] |= (1 << bit_position)

                    # Only update the memory if the player is in the hub
                    if is_in_hub:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x0371B8, list(self.real_inventory), "Combined WRAM")]
                        )

            self.received_index = len(ctx.items_received)

        except bizhawk.RequestFailedError:
            pass


