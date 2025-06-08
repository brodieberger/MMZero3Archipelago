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

    synced_in_game = False
    synced_hub = False
    in_results_screen = False
    player_warned = False
    
    in_game_inventory = bytearray(45)
    real_inventory = bytearray(45)
    empty_inventory = bytearray([0xFF] * 45)

    required_disks = 80 # Will be overwritten from settings
    goal_type = 0 # will also be overwritten. 0 is for default (kill boss with enough disks), 1 is vanilla (just kill the boss)
    easy_ex_skill = 0
    
    options_set = False
    received_index = 0
    collected_disks = 0

    

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
                #print(f"Required secret disks: {self.required_disks}")
                #print(f"Goal Type Set: {self.goal_type}")
                #print(self.easy_ex_skill)
                self.options_set = True
            
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
                    self.in_results_screen = False
                    #print("Entering Level, Starting Inventory Sync.")
                    #print(f"Real Inventory :{self.real_inventory}")
                    #print(f"In-Game Inventory :{self.in_game_inventory}")
                    #print(f"RAM Inventory :{save_data}")
                    
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

                    # If easy EX skill is enabled, give player S rank
                    if self.easy_ex_skill == 1:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x0372B1, [0x06], "Combined WRAM")]
                        )

                    self.synced_in_game = True

                    # Unlocks Z Saber, just a temp thing here cause of my AP rules that I don't feel like changing ATM
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [999]
                    }])

                    #print("Level Write Complete.")
                    #print(f"Real Inventory :{self.real_inventory}")
                    #print(f"In-Game Inventory :{self.in_game_inventory}")
                    #print(f"RAM Inventory :{save_data}")

                # Check if an item was picked up in a level
                if save_data != self.in_game_inventory and results_screen == b'\x00':
                    #print("Item pickup detected!")

                    # Find item that you picked up and send the location check for that item, then update the in game inventory (not ram data)
                    new_locations = []
                    for i in range(len(save_data)):
                        # Only look at the lower nibble (0x0F mask)
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

                # Check if the player has completed a level
                if results_screen != b'\x00' and not self.in_results_screen:
                    current_level = int.from_bytes(level_data, byteorder='little')
                    location_id = level_to_location.get(current_level)

                    if location_id:
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": [location_id]
                        }]) 

                    # Completion condition
                    # If the level that was finished was the last level
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
                        
                    # Fill player inventory so that player cant open items in result screen
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, list(self.empty_inventory), "Combined WRAM")]
                    )
                    self.in_results_screen = True

            #IF THE PLAYER IS NOT IN A LEVEL (hub)
            else:
                # Reset level sync flag
                self.synced_in_game = False
                self.in_results_screen = False

                # Sync to real inventory once on entering hub
                if not self.synced_hub:
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, list(self.real_inventory), "Combined WRAM")]
                    )

                    # Read save data again after writing it
                    save_data = (await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [(0x0371B8, 45, "Combined WRAM")])
                    )[0]
                    self.synced_hub = True

                # Check if an item was picked up or opened while in the hub.
                if save_data != self.real_inventory:
                    for i in range(len(save_data)):
                        real_byte = self.real_inventory[i]
                        save_byte = save_data[i]

                        # Identify new bits that are ON in save_data but OFF in real_inventory
                        new_bits = save_byte & (~real_byte)

                        if new_bits:
                            self.real_inventory[i] |= new_bits  # Only add bits, never remove

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
                    self.collected_disks += 1

                    # Only update the memory if the player is in the hub
                    if is_in_hub:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x0371B8, list(self.real_inventory), "Combined WRAM")]
                        )
            self.received_index = len(ctx.items_received)

            # Additional check to see if the player collected enough disks AFTER beating final stage. Only used in default game goal
            if self.player_warned == True and self.collected_disks >= self.required_disks and ctx.finished_game == False:
                await ctx.send_msgs([{
                    "cmd": "Say", "text": f"{self.required_disks} Disks collected! Game completed!"
                }])
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True


        except bizhawk.RequestFailedError:
            pass


