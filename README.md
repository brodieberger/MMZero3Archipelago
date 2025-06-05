# Mega Man Zero 3 Archipelago

Welcome to my project. Things are still under heavy development, but here you will find my development of a custom Archipelago World for Mega Man Zero 3 on the GBA. You should probably read everything here so you know what to expect before playing!

## General Information
- As of right now, the only thing randomized are the secret disks that are found in levels. Each one is a location check and an AP item.

- To beat the game, players must defeat the final boss while collecting a configurable number of secret disks (default: 80). You can set this number using the required_secret_disks option in your YAML file.

- There is another option to always give the player an S ranking. Remember that this will also give each boss a new attack, making the game harder.

- You *should* be able to use savestates throughout the game without anything breaking.

- Included in the releases page is a completed save file of the game. Starting a new game with the save file loaded will allow you to skip cutscenes.

## Options

- `goal`:  
  - `default` – Beat the final boss*with enough Secret Disks (default).
  - `vanilla` – Beat the final boss regardless of disks.

- `required_secret_disks`:  
  Set the number of disks needed for completion. Default is 80, max is 160.

- `easy_ex_skill`:  
  Gives you S-Rank at the end of every stage, guaranteeing EX Skill rewards. Will make some bosses harder.

## Known Bugs
- There are only 160 Secret Disks, the 20 disks that appear in the hub areas are currently not implemented in AP due to how I have the memory reading set up. They are still collectable in game, but they are just not going to be items or location checks.

- Save states have the possibility to screw things up, but I am not sure where.

- Theres probably some more bugs especially with world generation; I haven't really tested this too much. Seriously please help out.



## Planned Features
- The primary planned feature is more routing changes. 
  - Like how Mega Man 2 limits the available robot masters you could fight until you have the proper AP item, this world should likely do the same. 
  - Limiting Zero's default abilities (wall climb, dash, charge attack, sword combo) like how Mario World does it can also work. Although it would require editing the first level, as it cannot be completed without wall climbing.
- Fix hub area items to be collectable. 
- Deathlink support.
- Filler items (Energy Crystals, Health, Extra Lives). These are in the item pool but are currently unimplemented.
- EX Skills as optional location checks.
- Other collectables as location checks. Like static health pickups, extra lives, etc.
- Have skippable cutscenes unlocked by default. Right now having a completed save game on your file allows you to skip most cutscenes, but this should likely be a Rom edit or something similar.
- Let the player leave every level at will. By default you can only escape levels that you have beaten previously. This will be much more important later once the routing changes are implemented.

---
If you have any questions, feel free to contact me on Discord: Stingrays110, though I'd prefer if you kept it to the Zero channel on the Archipelago Discord