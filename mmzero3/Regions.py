from typing import Dict, List, NamedTuple


class MMZero3RegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, MMZero3RegionData] = {
    "Menu": MMZero3RegionData(["Opening Stage"]),
    "Opening Stage": MMZero3RegionData(["Level 1"]),
    "Level 1": MMZero3RegionData(["Boss Stage"]),
    "Boss Stage": MMZero3RegionData(),
}

