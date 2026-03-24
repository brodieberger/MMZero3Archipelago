# level RAM byte -> archipelago location ID
LEVEL_TO_LOCATION = {
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

# Bitflags for eReader content. AP Item ID -> (word_index, bit_position)
BIT_FLAGS = {
    111: (0, 1),
    112: (0, 6),
    113: (0, 7),
    114: (0, 10),
    115: (1, 1),
    117: (1, 4),
    118: (1, 10),
    119: (1, 12),
    120: (1, 13),
    121: (1, 15),
    122: (2, 2),
    123: (2, 4),
    124: (2, 5),
    125: (2, 7),
    126: (2, 8),
    127: (2, 13),
    128: (2, 15),
    129: (3, 4),
    130: (3, 5),
    131: (3, 7),
    132: (3, 8),
    133: (3, 10),
    134: (3, 13),
    135: (4, 2),
    136: (4, 11),
    137: (4, 13),
    138: (5, 3),
    139: (5, 5),
    140: (5, 6),
}

# Byte map for for eReader content. AP Item ID -> (Ram Address, Value)
BYTE_MAP = {
    # Dialogue Window (0x2002474)
    141: (0x02474, 0x01),
    142: (0x02474, 0x02),
    143: (0x02474, 0x03),
    144: (0x02474, 0x04),
    145: (0x02474, 0x05),
    146: (0x02474, 0x06),
    147: (0x02474, 0x07),
    148: (0x02474, 0x08),

    # Title Screen Design (0x2002475)
    149: (0x02475, 0x01),
    150: (0x02475, 0x02),
    151: (0x02475, 0x03),
    152: (0x02475, 0x04),

    # Elevator Design (0x2002476)
    153: (0x02476, 0x01),
    154: (0x02476, 0x02),

    # Base Environment (0x2002477)
    155: (0x02477, 0x01),
    156: (0x02477, 0x02),

    # Ciel's Computer Design (0x2002478)
    157: (0x02478, 0x01),
    158: (0x02478, 0x02),
    159: (0x02478, 0x03),
    160: (0x02478, 0x04),

    # Life Pickup Design (0x2002479)
    161: (0x02479, 0x01),
    162: (0x02479, 0x02),

    # E-Crystals Design (0x200247A)
    163: (0x0247A, 0x01),
    164: (0x0247A, 0x02),

    # Z Plate Design (0x200247C)
    177: (0x0247C, 0x01),
    178: (0x0247C, 0x02),

    # Buster Shot Design (0x200247D)
    179: (0x0247D, 0x01),
    180: (0x0247D, 0x02),
}

# Which location check to give based on dialogue. (So that no disks can be missed based on dialogue)
# Dialogue ID: location check to give (NPC)
DIALOGUE_LOCATION_MAP = {
    0x241: 107, #(Andrew)
    0x242: 107,
    0x243: 107,
    0x2CF: 107,
    0x2D0: 107,
    0x2D1: 107,
    0x2D2: 107,

    0x247: 116, #(Alouette)
    0x248: 116,
    0x249: 116,
    0x24A: 116,

    0x24e: 169, # (Hibou)
    0x24f: 160,
    0x250: 169,
    0x251: 169,

    0x253: 175, # (Menart)
    0x254: 175,
    0x255: 175,
    0x256: 175,
    0x257: 175,
    0x268: 175,

    0x25a: 167, # (Rocinolle)
    0x25C: 167,
    0x25d: 44, #(Rocinolle unmissable)
    0x25e: 167,

    0x271: 173, #(Hirondelle unmissable)

    0x284: 174, #(Doigt unmissable)

    0x2a6: 58, # (Tower guy)
    0x2A9: 58,
    0x2AB: 58,

    0x2b1: 23, #(guy in room 02D)
    0x2B3: 23,

    #207: 92 (cerveau),
    0x20b: 92,
    0x20c: 92,
    0x20d: 92,
}

BODY_CHIP_MAP = {
    197: (0, 0x20),  # Ice
    198: (0, 0x08),  # Thunder
    199: (0, 0x10),  # Flame
    200: (0, 0x02),  # Light
    201: (0, 0x04),  # Absorber
}

FOOT_CHIP_MAP = {
    202: (0, 0x20),  # Spike
    203: (0, 0x10),  # Quick
    204: (0, 0x04),  # Double Jump
    205: (0, 0x08),  # Shadow Dash
}

EX_SKILL_MAP = {
    206: (0, 0x04),  # Burst Shot
    207: (0, 0x80),  # Throw Blade
    208: (0, 0x20),  # Saber Smash
    209: (1, 0x01),  # 1000 Slash
    210: (1, 0x04),  # Shield Sweep
    211: (0, 0x40),  # Split Heavens
    212: (0, 0x08),  # Blizzard Arrow
    213: (0, 0x01),  # Reflect Laser
    214: (1, 0x02),  # Soul Launcher
    215: (1, 0x08),  # Orbit Shield
    216: (0, 0x02),  # V-Shot
    217: (0, 0x10),  # Gale Attack
}

LOCATION_TO_EXSKILL = {
    182: 206,
    183: 207,
    184: 208,
    185: 209,
    187: 210,
    188: 211,
    189: 212,
    190: 213,
    191: 214,
    192: 215,
    193: 216,
    194: 217
}

LOCATION_TO_CHIP = {
    182: 199,
    183: 197,
    184: 198,
    185: 200,
    190: 203, 
    191: 204,
    192: 202, 
    193: 205,
    194: 201
}