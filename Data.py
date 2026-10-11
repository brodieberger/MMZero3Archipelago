# Fields to be read from gAp and gApSeedConfig.
# EWRAM address minus 0x02000000

# gAp.ready reads AP_READY once the game has booted, and gAp.version reads AP_VERSION.
AP_READY = 0x335A5041      # Spells out 'APZ3' in little endian
AP_VERSION = 25

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
AP_MAX_LOCATION_ID = 382
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
CHECKED_LOCATIONS_COUNT = 48
SERVER_CHECKED = 0x0003EEDA
SERVER_CHECKED_COUNT = 48
RANK_ELF_USED = 0x0003EF0A
DISKS_OWNED = 0x0003EF0C
DEATH_COUNT = 0x0003EF0E
KILL_REQUEST = 0x0003EF10
CAN_ACCEPT_ITEMS = 0x0003EF11
SHOP_SEEN = 0x0003EF12
SHOP_SEEN_COUNT = 6

# gStageRun.id: Current stage
STAGE_ID = 0x000301A0

# gSpawnManager.area: Individual area of the stage
STAGE_AREA = 0x000300E1

# gApShopPrices
SHOP_PRICES_ROM_OFFSET = 0x00102520
SHOP_PRICES_COUNT = 48
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems
SHOP_ITEMS_ROM_OFFSET = 0x00102580
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
SEED_CONFIG_ROM_OFFSET = 0x000FFC14
SEED_CONFIG_SIZE = 12
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
}

# Stage id: the ROM offset and byte size of each BG palette
STAGE_PALETTES = {
    1: [(0x71C4A0, 96), (0x71F000, 128), (0x722AC0, 192), (0x725640, 192), (0x7277D4, 128)],
    2: [(0x739AA4, 192), (0x73D764, 192), (0x7411E4, 192), (0x745224, 224), (0x747230, 192), (0x7491C4, 192), (0x74A788, 96)],
    3: [(0x74D724, 192), (0x74F744, 224), (0x751FE0, 224), (0x753AC8, 160)],
    4: [(0x75B6D4, 224), (0x75F6B4, 128), (0x762D74, 32), (0x766D94, 192), (0x76AE54, 224)],
    5: [(0x76DDE4, 160), (0x7706F8, 192), (0x773434, 160), (0x7759E8, 96)],
    6: [(0x777748, 192), (0x7794F4, 192), (0x77AC4C, 64), (0x77C2BC, 224), (0x77D9A0, 224), (0x780594, 192), (0x7818C8, 224)],
    7: [(0x783F2C, 224), (0x787D0C, 224), (0x788C2C, 32), (0x7896E4, 32)],
    8: [(0x78C070, 224), (0x78F3A0, 192), (0x790E70, 224), (0x792CAC, 224)],
    9: [(0x794458, 224), (0x7972E8, 224), (0x7998AC, 224), (0x79B460, 224), (0x79D798, 192)],
    10: [(0x79FB7C, 192), (0x7A191C, 224), (0x7A3B04, 160), (0x7A56B8, 96)],
    11: [(0x7A977C, 224), (0x7ACCDC, 224), (0x7B03FC, 192), (0x7B2F7C, 128), (0x7B6FFC, 224)],
    12: [(0x71C4A0, 96), (0x72B814, 96), (0x72F0F4, 64), (0x732D34, 160), (0x7359D8, 64)],
    13: [(0x74F744, 224), (0x755684, 224), (0x75709C, 224), (0x758E04, 224)],
    14: [(0x7B95A4, 160), (0x7BB8A4, 96), (0x7BE3B4, 96), (0x7C0760, 96), (0x7C3434, 96)],
    15: [(0x7C5718, 224), (0x7C79B4, 160), (0x7C9124, 128), (0x7CB8EC, 224)],
    16: [(0x7CDB7C, 224), (0x7D07F4, 192), (0x7D17F0, 160), (0x7D40AC, 224), (0x7D7C98, 192), (0x7DB100, 224)],
    17: [(0x7DCA5C, 224), (0x7DE628, 224), (0x7E2708, 224), (0x7E67E8, 224), (0x7E88A8, 224), (0x7E9C3C, 160)],
}
