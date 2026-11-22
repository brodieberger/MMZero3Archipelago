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
AP_MAX_LOCATION_ID = 696
AP_SELECT_CYCLE_SUB_WEAPON = 0
AP_SELECT_CYCLE_MAIN_WEAPON = 1
AP_SELECT_CYCLE_HEAD_CHIP = 2
AP_SELECT_CYCLE_BODY_CHIP = 3
AP_SELECT_CYCLE_FOOT_CHIP = 4
AP_SELECT_USE_SUBTANK = 5
AP_ELVES_VANILLA = 0
AP_ELVES_NO_PENALTY = 1
AP_ELVES_AUTO = 2
AP_AIR_SPIN_HOLD_UP = 0
AP_AIR_SPIN_JUMP_SLASH = 1
AP_AIR_SPIN_DOUBLE_TAP = 2
AP_LOC_EXLIFE_FIRST = 231
AP_EXLIFE_COUNT = 10
AP_LOC_ITEMSANITY_FIRST = 301
AP_ITEMSANITY_COUNT = 82
AP_LOC_IMPORT_FIRST = 400
AP_IMPORT_ELF_COUNT = 28
AP_ITEM_IMPORT_ACCESS_FIRST = 320
AP_IMPORT_COUNT = 16
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
AP_SLOT_OWN = 255
AP_LOC_FORM_FIRST = 383
AP_LOC_IMPORT_MINIBOSS_FIRST = 656
AP_IMPORT_MINIBOSS_COUNT = 18
AP_LOC_IMPORT_EXLIFE_FIRST = 674
AP_IMPORT_EXLIFE_COUNT = 21
AP_LOC_IMPORT_SUBTANK_FIRST = 695

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
CHECKED_LOCATIONS_COUNT = 88
SERVER_CHECKED = 0x0003EF02
SERVER_CHECKED_COUNT = 88
RANK_ELF_USED = 0x0003EF5A
DISKS_OWNED = 0x0003EF5C
DEATH_COUNT = 0x0003EF5E
KILL_REQUEST = 0x0003EF60
CAN_ACCEPT_ITEMS = 0x0003EF61
SHOP_SEEN = 0x0003EF62
SHOP_SEEN_COUNT = 6

# gStageRun.id: Current stage
STAGE_ID = 0x000301A0

# gSpawnManager.area: Individual area of the stage
STAGE_AREA = 0x000300E1

# gApShopPrices
SHOP_PRICES_ROM_OFFSET = 0x00103040
SHOP_PRICES_COUNT = 48
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems
SHOP_ITEMS_ROM_OFFSET = 0x001030A0
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
SEED_CONFIG_ROM_OFFSET = 0x00100638
SEED_CONFIG_SIZE = 36
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
    "attackMode": (14, 1),
    "randomEnemies": (15, 1),
    "doubleTapDash": (16, 1),
    "airSpinSlash": (17, 1),
    "slotImport": (18, 15),
    "requiredStages": (33, 1),
}

# Stage id: the ROM offset and byte size of each BG palette
STAGE_PALETTES = {
    1: [(0xD93A8C, 96), (0xD965EC, 128), (0xD9A0AC, 192), (0xD9CC2C, 192), (0xD9EDC0, 128)],
    2: [(0xDB1090, 192), (0xDB4D50, 192), (0xDB87D0, 192), (0xDBC810, 224), (0xDBE81C, 192), (0xDC07B0, 192), (0xDC1D74, 96)],
    3: [(0xDC4D10, 192), (0xDC6D30, 224), (0xDC95CC, 224), (0xDCB0B4, 160)],
    4: [(0xDD2CC0, 224), (0xDD6CA0, 128), (0xDDA360, 32), (0xDDE380, 192), (0xDE2440, 224)],
    5: [(0xDE53D0, 160), (0xDE7CE4, 192), (0xDEAA20, 160), (0xDECFD4, 96)],
    6: [(0xDEED34, 192), (0xDF0AE0, 192), (0xDF2238, 64), (0xDF38A8, 224), (0xDF4F8C, 224), (0xDF7B80, 192), (0xDF8EB4, 224)],
    7: [(0xDFB518, 224), (0xDFF2F8, 224), (0xE00218, 32), (0xE00CD0, 32)],
    8: [(0xE0365C, 224), (0xE0698C, 192), (0xE0845C, 224), (0xE0A298, 224)],
    9: [(0xE0BA44, 224), (0xE0E8D4, 224), (0xE10E98, 224), (0xE12A4C, 224), (0xE14D84, 192)],
    10: [(0xE17168, 192), (0xE18F08, 224), (0xE1B0F0, 160), (0xE1CCA4, 96)],
    11: [(0xE20D68, 224), (0xE242C8, 224), (0xE279E8, 192), (0xE2A568, 128), (0xE2E5E8, 224)],
    12: [(0xD93A8C, 96), (0xDA2E00, 96), (0xDA66E0, 64), (0xDAA320, 160), (0xDACFC4, 64)],
    13: [(0xDC6D30, 224), (0xDCCC70, 224), (0xDCE688, 224), (0xDD03F0, 224)],
    14: [(0xE30B90, 160), (0xE32E90, 96), (0xE359A0, 96), (0xE37D4C, 96), (0xE3AA20, 96)],
    15: [(0xE3CD04, 224), (0xE3EFA0, 160), (0xE40710, 128), (0xE42ED8, 224)],
    16: [(0xE45168, 224), (0xE47DE0, 192), (0xE48DDC, 160), (0xE4B698, 224), (0xE4F284, 192), (0xE526EC, 224)],
    17: [(0xE54048, 224), (0xE55C14, 224), (0xE59CF4, 224), (0xE5DDD4, 224), (0xE5FE94, 224), (0xE61228, 160)],
}
