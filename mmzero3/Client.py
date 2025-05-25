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

            if not is_in_hub:
                # Reset hub sync flag
                self.synced_hub = False

                # Sync in-game inventory once on entering a level
                if not self.synced_in_game:
                    self.in_game_inventory = bytearray(save_data)
                    self.synced_in_game = True
                    print("Synced in-game inventory on level start.")

                # Check if an item was picked up
                if save_data != self.in_game_inventory:
                    print("Item pickup detected!")
                    
                    # TODO: Determine which item was picked up.
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [1]
                    }])

                    # Update real inventory
                    # TODO get the actual item that was picked up through AP
                    self.real_inventory = bytearray(save_data)

                    # Update in-game inventory to reflect new state
                    self.in_game_inventory = bytearray(save_data)

            else:
                # Reset level sync flag
                self.synced_in_game = False

                # Sync real inventory once on entering hub
                if not self.synced_hub:
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, list(self.real_inventory), "Combined WRAM")]
                    )
                    self.synced_hub = True
                    print("Wrote real inventory to game RAM in hub.")

            # debug shit
            #print(f"Level Data: {level_data.hex()}")
            #print(f"In-Game Inventory: {self.in_game_inventory.hex()}")
            #print(f"Real Inventory:   {self.real_inventory.hex()}")

            # Check AP locations (outdated example)
            if save_data[0] == 0x02:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [1]
                }])

            # Check for game clear
            if save_data[0] == 0x22:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            pass
