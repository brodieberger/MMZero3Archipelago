from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import MMZero3World


class MMZero3Location(Location):
    game = "Mega Man Zero 3"


class MMZero3LocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["MMZero3World"], bool] = lambda world: True
    locked_item: Optional[str] = None


# Stage names as they appear in game order
stage_names = [
    "Derelict Spacecraft", "Aegis Volcano Base", "Oceanic Highway Ruins",
    "Weapons Repair Factory", "Old Residential", "Missile Factory",
    "Twilight Desert", "Forest of Anatre", "Frontline Ice Base",
    "Area X-2", "Energy Facility", "Snowy Plains",
    "Sunken Library", "Giant Elevator", "Sub Arcadia"
]


location_data_table: Dict[str, MMZero3LocationData] = {

    "Get Z Saber (Start Game)": MMZero3LocationData(region="Derelict Spacecraft", locked_item="Z Saber", address=999),
    "Derelict Spacecraft 133: 5th Grand Cannon Kill": MMZero3LocationData(region="Derelict Spacecraft", address=133),
    "Derelict Spacecraft 140: 3rd Shrimpolin Kill": MMZero3LocationData(region="Derelict Spacecraft", address=140),
    "Derelict Spacecraft 158: 4th Shotcounter Kill": MMZero3LocationData(region="Derelict Spacecraft", address=158),
    "Derelict Spacecraft 156: 4th Batring Kill": MMZero3LocationData(region="Derelict Spacecraft", address=156),
    "Derelict Spacecraft (1) 024: 1st Pit Secret Wall": MMZero3LocationData(region="Derelict Spacecraft", address=24),
    "Derelict Spacecraft (2) 037: Ledge Past Entrance": MMZero3LocationData(region="Derelict Spacecraft", address=37),
    "Derelict Spacecraft (3) 050: Ice Side Room": MMZero3LocationData(region="Derelict Spacecraft", address=50),
    "Derelict Spacecraft (4) 101: Ledge in Top Right": MMZero3LocationData(region="Derelict Spacecraft", address=101),
    "Derelict Spacecraft (5) 111: Final Ascent Bottom": MMZero3LocationData(region="Derelict Spacecraft", address=111),
    "Derelict Spacecraft (6) 007: Final Ascent Ledge": MMZero3LocationData(region="Derelict Spacecraft", address=7),
    
    "Aegis Volcano Base 141: 3rd Volcaire Kill": MMZero3LocationData(region="Aegis Volcano Base", address=141),
    "Aegis Volcano Base 146: 4th Lamplort Kill": MMZero3LocationData(region="Aegis Volcano Base", address=146),
    "Aegis Volcano Base (1) 047: Ledge Above Lava": MMZero3LocationData(region="Aegis Volcano Base", address=47),
    "Aegis Volcano Base (2) 102: 1st Box Inside": MMZero3LocationData(region="Aegis Volcano Base", address=102),
    "Aegis Volcano Base (3) 026: Platform Above First Room": MMZero3LocationData(region="Aegis Volcano Base", address=26),
    "Aegis Volcano Base (4) 114: Push 1st Container": MMZero3LocationData(region="Aegis Volcano Base", address=114),
    "Aegis Volcano Base (5) 073: Container Before Miniboss, Platform After": MMZero3LocationData(region="Aegis Volcano Base", address=73),
    "Aegis Volcano Base (6) 152: 10th Crossbyne Kill (Miniboss)": MMZero3LocationData(region="Aegis Volcano Base", address=152),
    "Aegis Volcano Base (7) 072: Lamplort Box": MMZero3LocationData(region="Aegis Volcano Base", address=72),
    "Aegis Volcano Base (8) 008: Top Gabyoall Box": MMZero3LocationData(region="Aegis Volcano Base", address=8),
    
    "Oceanic Highway Ruins 159: 4th Sharkseal X Kill": MMZero3LocationData(region="Oceanic Highway Ruins", address=159),
    "Oceanic Highway Ruins 161: 3rd Icebon Kill": MMZero3LocationData(region="Oceanic Highway Ruins", address=161),
    "Oceanic Highway Ruins 160: 4th Shelluno Kill": MMZero3LocationData(region="Oceanic Highway Ruins", address=160),
    "Oceanic Highway Ruins (1) 005: 1st Pit Breakable": MMZero3LocationData(region="Oceanic Highway Ruins", address=5),
    "Oceanic Highway Ruins (2) 075: 1st Underwater Pit": MMZero3LocationData(region="Oceanic Highway Ruins", address=75),
    "Oceanic Highway Ruins (3) 009: Above Cyber Door": MMZero3LocationData(region="Oceanic Highway Ruins", address=9),
    "Oceanic Highway Ruins (4) 059: Above 1st Spike Wall": MMZero3LocationData(region="Oceanic Highway Ruins", address=59),
    "Oceanic Highway Ruins (5) 079: Miniboss Kill": MMZero3LocationData(region="Oceanic Highway Ruins", address=79),
    "Oceanic Highway Ruins (6) 049: Spiked Platforms": MMZero3LocationData(region="Oceanic Highway Ruins", address=49),
    "Oceanic Highway Ruins (7) 113: Left of Final Button": MMZero3LocationData(region="Oceanic Highway Ruins", address=113),
    
    "Weapons Repair Factory 147: 5th Lemmingles Kill": MMZero3LocationData(region="Weapons Repair Factory", address=147),
    "Weapons Repair Factory 131: 5th Deathlock Kill": MMZero3LocationData(region="Weapons Repair Factory", address=131),
    "Weapons Repair Factory 052: 3rd Lemmingles Generator Kill": MMZero3LocationData(region="Weapons Repair Factory", address=52),
    "Weapons Repair Factory (1) 012: Below 3rd Hammer": MMZero3LocationData(region="Weapons Repair Factory", address=12),
    "Weapons Repair Factory (2) 115: Hit 3rd Hammer": MMZero3LocationData(region="Weapons Repair Factory", address=115),
    "Weapons Repair Factory (3) 104: Past 4th Hammer": MMZero3LocationData(region="Weapons Repair Factory", address=104),
    "Weapons Repair Factory (4) 093: Miniboss Kill": MMZero3LocationData(region="Weapons Repair Factory", address=93),
    "Weapons Repair Factory (5) 100: Behind Lemmingles Generator": MMZero3LocationData(region="Weapons Repair Factory", address=100),
    "Weapons Repair Factory (6) 084: Conveyor Descent Ledge": MMZero3LocationData(region="Weapons Repair Factory", address=84),
    "Weapons Repair Factory (7) 053: Ladder Into Junk": MMZero3LocationData(region="Weapons Repair Factory", address=53),
    
    "Old Residential 145: 5th Seimeran Kill": MMZero3LocationData(region="Old Residential", address=145),
    "Old Residential 135: 3rd Pillar Cannon Kill": MMZero3LocationData(region="Old Residential", address=135),
    "Old Residential (1) 039: 1st Door": MMZero3LocationData(region="Old Residential", address=39),
    "Old Residential (2) 001: Stump Door": MMZero3LocationData(region="Old Residential", address=1),
    "Old Residential (3) 112: Floor Breakables": MMZero3LocationData(region="Old Residential", address=112),
    "Old Residential (4) 074: Left Fork Door": MMZero3LocationData(region="Old Residential", address=74),
    "Old Residential (5) 067: Miniboss Kill": MMZero3LocationData(region="Old Residential", address=67),
    "Old Residential (6) 028: Box After Bombers": MMZero3LocationData(region="Old Residential", address=28),
    "Old Residential (7) 048: Top Right Secret Door": MMZero3LocationData(region="Old Residential", address=48),
    "Old Residential (8) 013: 2 Pits Left of Secret Door Exit": MMZero3LocationData(region="Old Residential", address=13),
    
    "Missile Factory 139: 4th Eye Cannon Kill": MMZero3LocationData(region="Missile Factory", address=139),
    "Missile Factory 127: 4th Pantheon Guardian Kill": MMZero3LocationData(region="Missile Factory", address=127),
    "Missile Factory 138: 4th Generator Cannon Kill": MMZero3LocationData(region="Missile Factory", address=138),
    "Missile Factory 098: 6th Generator Cannon Spawn Kill": MMZero3LocationData(region="Missile Factory", address=98),
    "Missile Factory (1) 057: Spiky Side Room": MMZero3LocationData(region="Missile Factory", address=57),
    "Missile Factory (2) 030: By Cyber Door": MMZero3LocationData(region="Missile Factory", address=30),
    "Missile Factory (3) 090: 2nd Conveyor Slopes Ledge": MMZero3LocationData(region="Missile Factory", address=90),
    "Missile Factory (4) 055: Left of 2nd Conveyor Slope": MMZero3LocationData(region="Missile Factory", address=55),
    "Missile Factory (5) 117: Above 2nd Conveyor Slope": MMZero3LocationData(region="Missile Factory", address=117),
    "Missile Factory (6) 021: Top Left Ledge": MMZero3LocationData(region="Missile Factory", address=21),
    
    "Twilight Desert 091: 5th Shrimpolin Kill": MMZero3LocationData(region="Twilight Desert", address=91),
    "Twilight Desert 153: 5th Flopper Kill": MMZero3LocationData(region="Twilight Desert", address=153),
    "Twilight Desert 154: 5th PurpleNerple Kill": MMZero3LocationData(region="Twilight Desert", address=154),
    "Twilight Desert (1) 085: After Long Quicksand": MMZero3LocationData(region="Twilight Desert", address=85),
    "Twilight Desert (2) 089: Miniboss Kill": MMZero3LocationData(region="Twilight Desert", address=89),
    "Twilight Desert (3) 031: Above 1st Pillar Cannon": MMZero3LocationData(region="Twilight Desert", address=31),
    "Twilight Desert (4) 022: Above 2nd Cyber Door": MMZero3LocationData(region="Twilight Desert", address=22),
    "Twilight Desert (5) 105: After 1st Helicopter": MMZero3LocationData(region="Twilight Desert", address=105),
    "Twilight Desert (6) 118: After 1st Helicopter": MMZero3LocationData(region="Twilight Desert", address=118),
    "Twilight Desert (7) 065: 2nd Helicopter Kill": MMZero3LocationData(region="Twilight Desert", address=65),
    
    "Forest of Anatre 157: 5th Mellnet Kill": MMZero3LocationData(region="Forest of Anatre", address=157),
    "Forest of Anatre 134: 7th Tile Cannon Kill": MMZero3LocationData(region="Forest of Anatre", address=134),
    "Forest of Anatre (1) 063: Treetops Above Start": MMZero3LocationData(region="Forest of Anatre", address=63),
    "Forest of Anatre (2) 002: Ledge Above 1st Door": MMZero3LocationData(region="Forest of Anatre", address=2),
    "Forest of Anatre (3) 071: 3rd Button Lower Path": MMZero3LocationData(region="Forest of Anatre", address=71),
    "Forest of Anatre (4) 014: Above 7th Button": MMZero3LocationData(region="Forest of Anatre", address=14),
    "Forest of Anatre (5) 119: 7th Button Lower Path": MMZero3LocationData(region="Forest of Anatre", address=119),
    "Forest of Anatre (6) 108: 8th Button Spike Pit": MMZero3LocationData(region="Forest of Anatre", address=108),
    "Forest of Anatre (7) 076: Above 9th Button": MMZero3LocationData(region="Forest of Anatre", address=76),
    "Forest of Anatre (8) 040: Breakables Below Boss Room": MMZero3LocationData(region="Forest of Anatre", address=40),
    
    "Frontline Ice Base 132: 3rd Gyro Cannon Kill": MMZero3LocationData(region="Frontline Ice Base", address=132),
    "Frontline Ice Base 128: 3rd Pantheon Aqua Kill": MMZero3LocationData(region="Frontline Ice Base", address=128),
    "Frontline Ice Base 136: 3rd Heavy Cannon Kill": MMZero3LocationData(region="Frontline Ice Base", address=136),
    "Frontline Ice Base (1) 066: Top Route Tower": MMZero3LocationData(region="Frontline Ice Base", address=66),
    "Frontline Ice Base (2) 109: Top Route Indoor Ledge": MMZero3LocationData(region="Frontline Ice Base", address=109),
    "Frontline Ice Base (3) 015: Top Route Pipe Passage": MMZero3LocationData(region="Frontline Ice Base", address=15),
    "Frontline Ice Base (4) 032: Ledge Before 2nd Door": MMZero3LocationData(region="Frontline Ice Base", address=32),
    "Frontline Ice Base (5) 035: Ledge After 2nd Door": MMZero3LocationData(region="Frontline Ice Base", address=35),
    "Frontline Ice Base (6) 120: Heavy Cannon Box": MMZero3LocationData(region="Frontline Ice Base", address=120),
    "Frontline Ice Base (7) 068: Final Ascent": MMZero3LocationData(region="Frontline Ice Base", address=68),
    
    "Area X-2 137: 4th Capsule Cannon Kill": MMZero3LocationData(region="Area X-2", address=137),
    "Area X-2 (1) 110: 1st Descent Ledge": MMZero3LocationData(region="Area X-2", address=110),
    "Area X-2 (2) 121: 1st Descent Bottom": MMZero3LocationData(region="Area X-2", address=121),
    "Area X-2 (3) 062: Ledge Above Platforms": MMZero3LocationData(region="Area X-2", address=62),
    "Area X-2 (4) 034: 1st Ascent Top": MMZero3LocationData(region="Area X-2", address=34),
    "Area X-2 (5) 042: Spiky Ascent Bottom": MMZero3LocationData(region="Area X-2", address=42),
    "Area X-2 (6) 070: Spiky Ascent Middle": MMZero3LocationData(region="Area X-2", address=70),
    "Area X-2 (7) 077: Spiky Ascent Top": MMZero3LocationData(region="Area X-2", address=77),
    "Area X-2 (8) 069: Platforms Side Room (Lower)": MMZero3LocationData(region="Area X-2", address=69),
    "Area X-2 (9) 061: Platforms Side Room (Upper)": MMZero3LocationData(region="Area X-2", address=61),
    
    "Energy Facility 155: 9th Mothjiro Kill": MMZero3LocationData(region="Energy Facility", address=155),
    "Energy Facility 150: 4th Snakecord Kill": MMZero3LocationData(region="Energy Facility", address=150),
    "Energy Facility (1) 056: Box Past 1st Cyber Door": MMZero3LocationData(region="Energy Facility", address=56),
    "Energy Facility (2) 124: 1st Ascent Right Path": MMZero3LocationData(region="Energy Facility", address=124),
    "Energy Facility (3) 082: Box After 1st Ascent": MMZero3LocationData(region="Energy Facility", address=82),
    "Energy Facility (4) 149: Miniboss Kill": MMZero3LocationData(region="Energy Facility", address=149),
    "Energy Facility (5) 064: Girder Ride Left": MMZero3LocationData(region="Energy Facility", address=64),
    "Energy Facility (6) 095: Girder Ride Right": MMZero3LocationData(region="Energy Facility", address=95),
    "Energy Facility (7) 078: Snakecord Guarded Secret Wall": MMZero3LocationData(region="Energy Facility", address=78),
    "Energy Facility (8) 004: Girder Maze Top Left": MMZero3LocationData(region="Energy Facility", address=4),
    
    "Snowy Plains 162: 4th Shellcrawler Kill": MMZero3LocationData(region="Snowy Plains", address=162),
    "Snowy Plains (1) 003: 2nd Slope Secret Wall": MMZero3LocationData(region="Snowy Plains", address=3),
    "Snowy Plains (2) 029: 1st Rail Set Start": MMZero3LocationData(region="Snowy Plains", address=29),
    "Snowy Plains (3) 025: 1st Rail Set Middle": MMZero3LocationData(region="Snowy Plains", address=25),
    "Snowy Plains (4) 103: 1st Rail Set 2nd Pit Secret Wall": MMZero3LocationData(region="Snowy Plains", address=103),
    "Snowy Plains (5) 046: 5th Miniboss Snowball Kill": MMZero3LocationData(region="Snowy Plains", address=46),
    "Snowy Plains (6) 060: Miniboss Kill": MMZero3LocationData(region="Snowy Plains", address=60),
    "Snowy Plains (7) 123: 2nd Rail Set Start": MMZero3LocationData(region="Snowy Plains", address=123),
    "Snowy Plains (8) 086: 2nd Rail Set Middle": MMZero3LocationData(region="Snowy Plains", address=86),
    
    "Sunken Library (1) 125: Ledge Above First Pool": MMZero3LocationData(region="Sunken Library", address=125),
    "Sunken Library (2) 051: Under Second Pool": MMZero3LocationData(region="Sunken Library", address=51),
    "Sunken Library (3) 043: Last Exposed Wire": MMZero3LocationData(region="Sunken Library", address=43),
    "Sunken Library (4) 033: Past Exposed Wires": MMZero3LocationData(region="Sunken Library", address=33),
    "Sunken Library (5) 094: End of 1st Passage": MMZero3LocationData(region="Sunken Library", address=94),
    "Sunken Library (6) 096: Above 1st Door": MMZero3LocationData(region="Sunken Library", address=96),
    "Sunken Library 010: Dr. Weil Data": MMZero3LocationData(region="Sunken Library", address=10),
    "Sunken Library 017: Omega Data": MMZero3LocationData(region="Sunken Library", address=17),
    "Sunken Library 016: Dark Elf Data": MMZero3LocationData(region="Sunken Library", address=16),
    "Sunken Library 018: Elf Wars Data": MMZero3LocationData(region="Sunken Library", address=18),
    
    "Giant Elevator 148: 5th Cattatank Kill": MMZero3LocationData(region="Giant Elevator", address=148),
    "Giant Elevator 144: 6th Shotloid Kill": MMZero3LocationData(region="Giant Elevator", address=144),
    "Giant Elevator 129: 4th Pantheon Fist Kill": MMZero3LocationData(region="Giant Elevator", address=129),
    "Giant Elevator (1) 045: 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=45),
    "Giant Elevator (2) 041: 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=41),
    "Giant Elevator (3) 080: 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=80),
    "Giant Elevator (4) 054: 1st Passage High Ledges": MMZero3LocationData(region="Giant Elevator", address=54),
    "Giant Elevator (5) 122: 1st Descent Ledge": MMZero3LocationData(region="Giant Elevator", address=122),
    "Giant Elevator (6) 027: 1st Descent Bottom Left Breakable": MMZero3LocationData(region="Giant Elevator", address=27),
    "Giant Elevator (7) 088: Miniboss Kill": MMZero3LocationData(region="Giant Elevator", address=88),
    
    "Sub Arcadia 163: 5th Cannonhopper Kill": MMZero3LocationData(region="Sub Arcadia", address=163),
    "Sub Arcadia 143: 3rd Petatria Kill": MMZero3LocationData(region="Sub Arcadia", address=143),
    "Sub Arcadia 142: 5th Claveker Kill": MMZero3LocationData(region="Sub Arcadia", address=142),
    "Sub Arcadia (1) 036: 1st Descent Ledge": MMZero3LocationData(region="Sub Arcadia", address=36),
    "Sub Arcadia (2) 081: Platforms Room Under Start": MMZero3LocationData(region="Sub Arcadia", address=81),
    "Sub Arcadia (3) 038: Platforms Room Top Left": MMZero3LocationData(region="Sub Arcadia", address=38),
    "Sub Arcadia (4) 006: Phantom Kill (Platforms Top Left, in Cyberspace)": MMZero3LocationData(region="Sub Arcadia", address=6),
    "Sub Arcadia (5) 180: Platforms Room Bottom": MMZero3LocationData(region="Sub Arcadia", address=180),
    "Sub Arcadia (6) 087: Box Past 1st Door": MMZero3LocationData(region="Sub Arcadia", address=87),
    "Sub Arcadia (7) 083: Final Descent Left": MMZero3LocationData(region="Sub Arcadia", address=83),
    
    "Abandoned Research Laboratory 126: 5th Pantheon Hunter Kill": MMZero3LocationData(region="Abandoned Research Laboratory", address=126),
    "Abandoned Research Laboratory (1) 097: 1st Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=97),
    "Abandoned Research Laboratory (2) 177: Ledge Above Spike Zone": MMZero3LocationData(region="Abandoned Research Laboratory", address=177),
    "Abandoned Research Laboratory (3) 151: Ice Zone Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=151),
    "Abandoned Research Laboratory (4) 019: Ice Zone Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=19),
    "Abandoned Research Laboratory (5) 020: Ice Zone Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=20),
    "Abandoned Research Laboratory (6) 178: Ice Zone Alarm Ledge": MMZero3LocationData(region="Abandoned Research Laboratory", address=178),
    "Abandoned Research Laboratory (7) 164: Ice Zone Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=164),
    "Abandoned Research Laboratory (8) 179: Final Section Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=179),
    "Abandoned Research Laboratory (9) 011: Final Section Box": MMZero3LocationData(region="Abandoned Research Laboratory", address=11),

    **{
        f"Complete {stage}": MMZero3LocationData(
            region=f"{stage}",
            locked_item=f"{stage} Cleared",
            address=180 + idx + 1,
        )
        for idx, stage in enumerate(stage_names)
    },

    "Complete Abandoned Research Laboratory": MMZero3LocationData(
        region="Abandoned Research Laboratory",
        locked_item="Victory",
        address=196,
    ),
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
