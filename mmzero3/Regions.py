from typing import Dict, List, NamedTuple


class MMZero3RegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, MMZero3RegionData] = {
    "Menu": MMZero3RegionData(["Derelict Spacecraft"]),
    "Derelict Spacecraft": MMZero3RegionData(["Resistance Base"]),
    "Resistance Base": MMZero3RegionData(["Stage Group 1"]),

    # First 4 selectable main stages
    "Stage Group 1": MMZero3RegionData(["Aegis Volcano Base", "Oceanic Highway Ruins", "Weapons Repair Factory", "Old Residential", "Missile Factory"]),
    "Aegis Volcano Base": MMZero3RegionData(),
    "Oceanic Highway Ruins": MMZero3RegionData(),
    "Weapons Repair Factory": MMZero3RegionData(),
    "Old Residential": MMZero3RegionData(),

    # Crea and Prea (two baby elves)
    "Missile Factory": MMZero3RegionData(["Stage Group 2"]),
    
    # Next 3 selectable stages
    "Stage Group 2": MMZero3RegionData(["Twilight Desert", "Frontline Ice Base", "Forest of Anatre", "Area X-2"]),
    "Twilight Desert": MMZero3RegionData(),
    "Frontline Ice Base": MMZero3RegionData(),
    "Forest of Anatre": MMZero3RegionData(),

    # Copy X
    "Area X-2": MMZero3RegionData(["Stage Group 3"]),

    # Final 4 selectable stages
    "Stage Group 3": MMZero3RegionData(["Energy Facility", "Snowy Plains", "Sunken Library", "Giant Elevator", "Sub Arcadia"]),
    "Energy Facility": MMZero3RegionData(),
    "Snowy Plains": MMZero3RegionData(),
    "Sunken Library": MMZero3RegionData(),
    "Giant Elevator": MMZero3RegionData(),

    # Crea and Prea rematch (and shadow guy)
    "Sub Arcadia": MMZero3RegionData(["Abandoned Research Laboratory"]),

    # Final stage
    "Abandoned Research Laboratory": MMZero3RegionData(),
}

