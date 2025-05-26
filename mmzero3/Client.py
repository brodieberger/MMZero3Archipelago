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


    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x0a0, 12, "ROM")]))[0]).decode("ascii")
            if rom_name != "MEGAMANZERO3":
                return False  # Not a Mega Man Zero 3 ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        ctx.game = self.game
        ctx.items_handling = 0b001
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
            
            # When the player loads into the hub or a level, it should sync the inventory
            # This value keeps track of that
            is_in_hub = (level_data.hex() == '11')

            # IF THE PLAYER IS IN A LEVEL
            if not is_in_hub:
                # Reset hub sync flag
                self.synced_hub = False

                # Sync in-game inventory once on entering a level
                if not self.synced_in_game:
                    print("Entering Level, Starting Inventory Sync.")

                    # Sync in game inventory inventory once on entering level
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, list(self.in_game_inventory), "Combined WRAM")]
                    )
                    self.synced_in_game = True
                    print("Synced in-game inventory on level start.")
                    print(f"Level Data: {level_data.hex()}")
                    print(f"In-Game Inventory: {self.in_game_inventory.hex()}")
                    print(f"Real Inventory:   {self.real_inventory.hex()}")

                    # Unlocks Z Saber, just a temp thing here cause of my AP rules that I don't feel like changing ATM
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [999]
                    }])

                # Check if an item was picked up
                if save_data != self.in_game_inventory:
                    print("Item pickup detected!")


                    # nothing about this currently works
                    # it should find item that you picked up and send the location check for that item, then update the in game inventory (not ram data)

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
                        print(f"New Locations Found: {new_locations}")
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": new_locations
                        }])
                    else:
                        print("No new locations found.") # Player scanned a disk or loaded a save/savestate?
                    
                    # Update inventory. Real inventory only updated when AP item is given
                    self.in_game_inventory = bytearray(save_data)

                    print(f"Level Data: {level_data.hex()}")
                    print(f"In-Game Inventory: {self.in_game_inventory.hex()}")
                    print(f"Real Inventory:   {self.real_inventory.hex()}")

            #IF THE PLAYER IS NOT IN A LEVEL
            else:
                # Reset level sync flag
                self.synced_in_game = False

                # Sync to real inventory once on entering hub
                if not self.synced_hub:
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, list(self.real_inventory), "Combined WRAM")]
                    )
                    self.synced_hub = True
                    print("Entering Hub, Starting Inventory Sync.")
                    print("Wrote real inventory to game RAM in hub.")
                    print(f"Level Data: {level_data.hex()}")
                    print(f"In-Game Inventory: {self.in_game_inventory.hex()}")
                    print(f"Real Inventory:   {self.real_inventory.hex()}")

            # TODO receive an item from AP and add it to ram.
            # Should check if the player is in a level or in the hub.
            # If in level, add it to real inventory
            for i in range(len(ctx.items_received)):
                print(f"AP Item Received: {ctx.items_received}")

            # Check for game clear (Not currently used)
            if save_data[0] == 0xFF:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            pass


