# Fields to be read from gAp and gApSeedConfig.
# EWRAM address minus 0x02000000

# gAp.ready reads AP_READY once the game has booted, and gAp.version reads AP_VERSION.
AP_READY = 0x335A5041      # Spells out 'APZ3' in little endian
AP_VERSION = 26

# Constants from ap.h and constants/constants.h
AP_KILL_REQUESTED = 1
AP_TAKEN_BYTE = 8
AP_TAKEN_SUBTANK1 = 1
AP_TAKEN_SUBTANK2 = 2
AP_LOC_SUBTANK_1 = 221
AP_LOC_SUBTANK_2 = 222
AP_ITEM_DISK_FIRST = 1
AP_ITEM_DISK_LAST = 180
AP_DISK_BYTES = 45
AP_UNLOCK_BYTE = 12
AP_MAX_LOCATION_ID = 655
AP_SELECT_CYCLE_SUB_WEAPON = 0
AP_SELECT_CYCLE_MAIN_WEAPON = 1
AP_SELECT_CYCLE_HEAD_CHIP = 2
AP_SELECT_CYCLE_BODY_CHIP = 3
AP_SELECT_CYCLE_FOOT_CHIP = 4
AP_SELECT_USE_SUBTANK = 5
AP_ELVES_VANILLA = 0
AP_ELVES_NO_PENALTY = 1
AP_ELVES_AUTO = 2
AP_LOC_EXLIFE_FIRST = 231
AP_EXLIFE_COUNT = 10
AP_LOC_ITEMSANITY_FIRST = 301
AP_ITEMSANITY_COUNT = 82
AP_LOC_IMPORT_FIRST = 400
AP_IMPORT_ELF_COUNT = 28
AP_ITEM_IMPORT_ACCESS_FIRST = 320
AP_IMPORT_COUNT = 7
AP_SHOP_LOCATION_FIRST = 253
AP_SHOP_TEXT_COLS = 12
AP_SHOP_NAME_LINES = 3
AP_SHOP_PLAYER_LINES = 2
AP_SHOP_TEXT_END = 255
AP_SHOP_KIND_PLAIN = 0
AP_SHOP_KIND_PROGRESSION = 1
AP_SHOP_KIND_TRAP = 2
AP_SHOP_OWN_WORLD = 4
AP_SHOP_SLOTS_MAX = 48
AP_ITEM_STORY_MID = 229
AP_ITEM_STORY_LATE = 230
AP_ITEM_WEAPON_LEVEL_FIRST = 400
AP_ITEM_CODES_PER_WEAPON = 8
RANK_F = 0
RANK_E = 1
RANK_D = 2
RANK_C = 3
RANK_B = 4
RANK_A = 5
RANK_S = 6
AP_FINAL_RANK_NONE = 255

# gAp
GAP = 0x0003EE80
READY = 0x0003EE80
VERSION = 0x0003EE84
ITEM_INBOX = 0x0003EE86
ITEM_INBOX_COUNT = 16
ITEM_INBOX_ELEMENT_SIZE = 2
ITEMS_APPLIED = 0x0003EEA6
INBOX_WRITE_INDEX = 0x0003EEA8
INBOX_READ_INDEX = 0x0003EEA9
CHECKED_LOCATIONS = 0x0003EEAA
CHECKED_LOCATIONS_COUNT = 82
SERVER_CHECKED = 0x0003EEFC
SERVER_CHECKED_COUNT = 82
RANK_ELF_USED = 0x0003EF4E
DISKS_OWNED = 0x0003EF50
DEATH_COUNT = 0x0003EF52
KILL_REQUEST = 0x0003EF54
CAN_ACCEPT_ITEMS = 0x0003EF55
SHOP_SEEN = 0x0003EF56
SHOP_SEEN_COUNT = 6

# gStageRun.id: Current stage
STAGE_ID = 0x000301A0

# gSpawnManager.area: Individual area of the stage
STAGE_AREA = 0x000300E1

# gApShopPrices
SHOP_PRICES_ROM_OFFSET = 0x00102A8C
SHOP_PRICES_COUNT = 48
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems
SHOP_ITEMS_ROM_OFFSET = 0x00102AEC
SHOP_ITEMS_COUNT = 48
SHOP_ITEMS_SIZE = 68

# The game's text encoding, for names the shop prints
CHARMAP = {
    ' ': 0x00,
    '!': 0xCA,
    '"': 0xE9,
    '#': 0xCC,
    '$': 0xFF,
    '%': 0xCE,
    '&': 0xCF,
    "'": 0xD0,
    '(': 0xD1,
    ')': 0xD2,
    '*': 0xD3,
    '+': 0xD4,
    ',': 0xE8,
    '-': 0xD6,
    '.': 0xE5,
    '/': 0xD8,
    '0': 0x01,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    ':': 0xD9,
    '=': 0xDB,
    '?': 0xDD,
    'A': 0x0B,
    'B': 0x0C,
    'C': 0x0D,
    'D': 0x0E,
    'E': 0x0F,
    'F': 0x10,
    'G': 0x11,
    'H': 0x12,
    'I': 0x13,
    'J': 0x14,
    'K': 0x15,
    'L': 0x16,
    'M': 0x17,
    'N': 0x18,
    'O': 0x19,
    'P': 0x1A,
    'Q': 0x1B,
    'R': 0x1C,
    'S': 0x1D,
    'T': 0x1E,
    'U': 0x1F,
    'V': 0x20,
    'W': 0x21,
    'X': 0x22,
    'Y': 0x23,
    'Z': 0x24,
    '[': 0xDE,
    ']': 0xDF,
    '_': 0xE0,
    'a': 0x25,
    'b': 0x26,
    'c': 0x27,
    'd': 0x28,
    'e': 0x29,
    'f': 0x2A,
    'g': 0x2B,
    'h': 0x2C,
    'i': 0x2D,
    'j': 0x2E,
    'k': 0x2F,
    'l': 0x30,
    'm': 0x31,
    'n': 0x32,
    'o': 0x33,
    'p': 0x34,
    'q': 0x35,
    'r': 0x36,
    's': 0x37,
    't': 0x38,
    'u': 0x39,
    'v': 0x3A,
    'w': 0x3B,
    'x': 0x3C,
    'y': 0x3D,
    'z': 0x3E,
}

# gApSeedConfig, ROM data
SEED_CONFIG_ROM_OFFSET = 0x00100114
SEED_CONFIG_SIZE = 16
SEED_CONFIG_FIELDS = {   # ap.h name: (offset, size)
    "requiredDisks": (0, 2),
    "startingWeapons": (2, 1),
    "exSkillRank": (3, 1),
    "itemsanity": (4, 1),
    "exLifeSanity": (5, 1),
    "selectButton": (6, 1),
    "damageUpgrades": (7, 1),
    "cyberElves": (8, 1),
    "diskNamePopup": (9, 1),
    "infiniteLives": (10, 1),
    "finalStageRank": (11, 1),
    "enemyDiskMarkers": (12, 1),
    "legacyStages": (13, 1),
    "unused": (14, 1),
}

# Stage id: the ROM offset and byte size of each BG palette
STAGE_PALETTES = {
    1: [(0x9BFD28, 96), (0x9C2888, 128), (0x9C6348, 192), (0x9C8EC8, 192), (0x9CB05C, 128)],
    2: [(0x9DD32C, 192), (0x9E0FEC, 192), (0x9E4A6C, 192), (0x9E8AAC, 224), (0x9EAAB8, 192), (0x9ECA4C, 192), (0x9EE010, 96)],
    3: [(0x9F0FAC, 192), (0x9F2FCC, 224), (0x9F5868, 224), (0x9F7350, 160)],
    4: [(0x9FEF5C, 224), (0xA02F3C, 128), (0xA065FC, 32), (0xA0A61C, 192), (0xA0E6DC, 224)],
    5: [(0xA1166C, 160), (0xA13F80, 192), (0xA16CBC, 160), (0xA19270, 96)],
    6: [(0xA1AFD0, 192), (0xA1CD7C, 192), (0xA1E4D4, 64), (0xA1FB44, 224), (0xA21228, 224), (0xA23E1C, 192), (0xA25150, 224)],
    7: [(0xA277B4, 224), (0xA2B594, 224), (0xA2C4B4, 32), (0xA2CF6C, 32)],
    8: [(0xA2F8F8, 224), (0xA32C28, 192), (0xA346F8, 224), (0xA36534, 224)],
    9: [(0xA37CE0, 224), (0xA3AB70, 224), (0xA3D134, 224), (0xA3ECE8, 224), (0xA41020, 192)],
    10: [(0xA43404, 192), (0xA451A4, 224), (0xA4738C, 160), (0xA48F40, 96)],
    11: [(0xA4D004, 224), (0xA50564, 224), (0xA53C84, 192), (0xA56804, 128), (0xA5A884, 224)],
    12: [(0x9BFD28, 96), (0x9CF09C, 96), (0x9D297C, 64), (0x9D65BC, 160), (0x9D9260, 64)],
    13: [(0x9F2FCC, 224), (0x9F8F0C, 224), (0x9FA924, 224), (0x9FC68C, 224)],
    14: [(0xA5CE2C, 160), (0xA5F12C, 96), (0xA61C3C, 96), (0xA63FE8, 96), (0xA66CBC, 96)],
    15: [(0xA68FA0, 224), (0xA6B23C, 160), (0xA6C9AC, 128), (0xA6F174, 224)],
    16: [(0xA71404, 224), (0xA7407C, 192), (0xA75078, 160), (0xA77934, 224), (0xA7B520, 192), (0xA7E988, 224)],
    17: [(0xA802E4, 224), (0xA81EB0, 224), (0xA85F90, 224), (0xA8A070, 224), (0xA8C130, 224), (0xA8D4C4, 160)],
}
