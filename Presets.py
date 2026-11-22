from typing import Any, Dict

mmzero3_options_presets: Dict[str, Dict[str, Any]] = {
    "Developer's Choice": {
        # Goal Options
        "required_secret_disks": 80,
        "required_stage_clears": 80,
        "final_stage_rank": "f",

        # Legacy Stages (Zero 2)
        "legacy_stages": "shuffle",
        "legacy_shuffle_count": "coin_flip",
        "cut_secret_disks": True,

        # Sanity Options
        "extra_life_sanity": True,
        "itemsanity": False,
        "shop_slots": 30,
        "shop_price_scale": 100,

        # Optional Randomization
        "randomize_enemies": True,
        "enemy_difficulty": "chaos",

        # Gameplay
        "starting_weapons": ["Buster", "Z-Saber"],
        "weapon_damage_upgrades": True,
        "select_button": "cycle_sub_weapon",
        "cyber_elves": "auto",
        "ex_skill_rank": "a",
        "infinite_lives": True,
        "attack_mode_b": True,
        "double_tap_dash": False,
        "death_link": False,

        # Traps
        "trap_percentage": 25,
        "enabled_traps": ["Earthquake", "Pixelate", "Slippery Floor"],

        # Aesthetics
        "randomized_palettes": True,
        "disk_name_popup": True,
        "enemy_disk_markers": True,
    },
}
