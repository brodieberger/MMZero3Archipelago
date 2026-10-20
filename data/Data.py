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
AP_MAX_LOCATION_ID = 390
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
AP_LOC_IMPORT_ELF_FIRST = 383
AP_IMPORT_ELF_COUNT = 6
AP_ITEM_IMPORT_ACCESS = 196
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
CHECKED_LOCATIONS_COUNT = 49
SERVER_CHECKED = 0x0003EEDB
SERVER_CHECKED_COUNT = 49
RANK_ELF_USED = 0x0003EF0C
DISKS_OWNED = 0x0003EF0E
DEATH_COUNT = 0x0003EF10
KILL_REQUEST = 0x0003EF12
CAN_ACCEPT_ITEMS = 0x0003EF13
SHOP_SEEN = 0x0003EF14
SHOP_SEEN_COUNT = 6

# gStageRun.id: Current stage
STAGE_ID = 0x000301A0

# gSpawnManager.area: Individual area of the stage
STAGE_AREA = 0x000300E1

# gApShopPrices
SHOP_PRICES_ROM_OFFSET = 0x00102680
SHOP_PRICES_COUNT = 48
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems
SHOP_ITEMS_ROM_OFFSET = 0x001026E0
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
SEED_CONFIG_ROM_OFFSET = 0x000FFD48
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
    1: [(0x7CFEE4, 96), (0x7D2A44, 128), (0x7D6504, 192), (0x7D9084, 192), (0x7DB218, 128)],
    2: [(0x7ED4E8, 192), (0x7F11A8, 192), (0x7F4C28, 192), (0x7F8C68, 224), (0x7FAC74, 192), (0x7FCC08, 192), (0x7FE1CC, 96)],
    3: [(0x801168, 192), (0x803188, 224), (0x805A24, 224), (0x80750C, 160)],
    4: [(0x80F118, 224), (0x8130F8, 128), (0x8167B8, 32), (0x81A7D8, 192), (0x81E898, 224)],
    5: [(0x821828, 160), (0x82413C, 192), (0x826E78, 160), (0x82942C, 96)],
    6: [(0x82B18C, 192), (0x82CF38, 192), (0x82E690, 64), (0x82FD00, 224), (0x8313E4, 224), (0x833FD8, 192), (0x83530C, 224)],
    7: [(0x837970, 224), (0x83B750, 224), (0x83C670, 32), (0x83D128, 32)],
    8: [(0x83FAB4, 224), (0x842DE4, 192), (0x8448B4, 224), (0x8466F0, 224)],
    9: [(0x847E9C, 224), (0x84AD2C, 224), (0x84D2F0, 224), (0x84EEA4, 224), (0x8511DC, 192)],
    10: [(0x8535C0, 192), (0x855360, 224), (0x857548, 160), (0x8590FC, 96)],
    11: [(0x85D1C0, 224), (0x860720, 224), (0x863E40, 192), (0x8669C0, 128), (0x86AA40, 224)],
    12: [(0x7CFEE4, 96), (0x7DF258, 96), (0x7E2B38, 64), (0x7E6778, 160), (0x7E941C, 64)],
    13: [(0x803188, 224), (0x8090C8, 224), (0x80AAE0, 224), (0x80C848, 224)],
    14: [(0x86CFE8, 160), (0x86F2E8, 96), (0x871DF8, 96), (0x8741A4, 96), (0x876E78, 96)],
    15: [(0x87915C, 224), (0x87B3F8, 160), (0x87CB68, 128), (0x87F330, 224)],
    16: [(0x8815C0, 224), (0x884238, 192), (0x885234, 160), (0x887AF0, 224), (0x88B6DC, 192), (0x88EB44, 224)],
    17: [(0x8904A0, 224), (0x89206C, 224), (0x89614C, 224), (0x89A22C, 224), (0x89C2EC, 224), (0x89D680, 160)],
}
