from typing import Dict, List, NamedTuple


class MMZero3RegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, MMZero3RegionData] = {
    "Menu": MMZero3RegionData([
        # Hub. Contains different checks based on game progress flags.
        "Resistance Base 1",
        "Resistance Base 2",
        "Resistance Base 3",

        # Intro
        "Derelict Spacecraft",

        # First 4 selectable main stages
        "Aegis Volcano Base",
        "Oceanic Highway Ruins",
        "Weapons Repair Factory",
        "Old Residential",

        # Intermission 1
        "Missile Factory",

        # Second 3
        "Twilight Desert",
        "Forest of Anatre",
        "Frontline Ice Base",

        # Intermission 2
        "Area X-2",

        #Final 4
        "Energy Facility",
        "Snowy Plains",
        "Sunken Library",
        "Giant Elevator",

        # Intermission 3
        "Sub Arcadia",

        # Final Level
        "Abandoned Research Laboratory",

        # Zero 2's forms, can be earned in any stage when a zero 2 stage exists in the seed.
        "Zero 2 Forms",

        # Legacy stages, with legacy_stages option:
        "Z2 Sand Wilderness",
        "Z2 Computer Zone",
        "Z2 Train",
        "Z2 Power Room",
        "Z2 Forest of Dysis",
        "Z2 Residential Area",
        "Z2 Bombardment Aircraft",
        "Z2 Forest of Notus",
        "Z2 Computer Zone 2",
        "Z2 Crystal Cave",
        "Z2 Shuttle Factory",
        "Z2 Neo Arcadia Temple",
        "Z2 Temple of Flame",
        "Z2 Temple of Ice",
        "Z2 Temple of Wind",
        "Z2 Yggdrasil",
    ]),

    "Resistance Base 1": MMZero3RegionData(),
    "Resistance Base 2": MMZero3RegionData(),
    "Resistance Base 3": MMZero3RegionData(),

    "Derelict Spacecraft": MMZero3RegionData(),

    "Aegis Volcano Base": MMZero3RegionData(),
    "Oceanic Highway Ruins": MMZero3RegionData(),
    "Weapons Repair Factory": MMZero3RegionData(),
    "Old Residential": MMZero3RegionData(),

    # Crea and Prea (two baby elves)
    "Missile Factory": MMZero3RegionData(),

    "Twilight Desert": MMZero3RegionData(),
    "Forest of Anatre": MMZero3RegionData(),
    "Frontline Ice Base": MMZero3RegionData(),

    # Copy X
    "Area X-2": MMZero3RegionData(),

    "Energy Facility": MMZero3RegionData(),
    "Snowy Plains": MMZero3RegionData(),
    "Sunken Library": MMZero3RegionData(),
    "Giant Elevator": MMZero3RegionData(),

    # Crea and Prea rematch (and shadow guy)
    "Sub Arcadia": MMZero3RegionData(),

    # Final stage
    "Abandoned Research Laboratory": MMZero3RegionData(),

    "Zero 2 Forms": MMZero3RegionData(),

    "Z2 Sand Wilderness": MMZero3RegionData(),
    "Z2 Computer Zone": MMZero3RegionData(),
    "Z2 Train": MMZero3RegionData(),
    "Z2 Power Room": MMZero3RegionData(),
    "Z2 Forest of Dysis": MMZero3RegionData(),
    "Z2 Residential Area": MMZero3RegionData(),
    "Z2 Bombardment Aircraft": MMZero3RegionData(),
    "Z2 Forest of Notus": MMZero3RegionData(),
    "Z2 Computer Zone 2": MMZero3RegionData(),
    "Z2 Crystal Cave": MMZero3RegionData(),
    "Z2 Shuttle Factory": MMZero3RegionData(),
    "Z2 Neo Arcadia Temple": MMZero3RegionData(),
    "Z2 Temple of Flame": MMZero3RegionData(),
    "Z2 Temple of Ice": MMZero3RegionData(),
    "Z2 Temple of Wind": MMZero3RegionData(),
    "Z2 Yggdrasil": MMZero3RegionData(),
}
