# Fields to be read from gAp and gApSeedConfig.
# EWRAM address minus 0x02000000

# gAp.ready reads AP_READY once the game has booted, and gAp.version reads AP_VERSION.
AP_READY = 0x335A5041      # Spells out 'APZ3' in little endian
AP_VERSION = 23

# Constants from ap.h
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

# gApShopPrices, ROM data: one u16 per shop slot
SHOP_PRICES_ROM_OFFSET = 0x0010247C
SHOP_PRICES_COUNT = 48
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems, ROM data: one fixed record a slot
SHOP_ITEMS_ROM_OFFSET = 0x001024DC
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
SEED_CONFIG_ROM_OFFSET = 0x000FFB74
SEED_CONFIG_SIZE = 12
SEED_CONFIG_FIELDS = {   # ap.h name: (offset, size)
    "requiredDisks": (0, 2),
    "startingWeapons": (2, 1),
    "easyExSkill": (3, 1),
    "itemsanity": (4, 1),
    "exLifeSanity": (5, 1),
    "selectButton": (6, 1),
    "damageUpgrades": (7, 1),
    "cyberElves": (8, 1),
    "diskNamePopup": (9, 1),
    "unused": (10, 1),
}

# Stage id: the ROM offset and byte size of each BG palette
STAGE_PALETTES = {
    1: [(0x759DA8, 96), (0x75C908, 128), (0x7603C8, 192), (0x762F48, 192), (0x7650DC, 128)],
    2: [(0x7773AC, 192), (0x77B06C, 192), (0x77EAEC, 192), (0x782B2C, 224), (0x784B38, 192), (0x786ACC, 192), (0x788090, 96)],
    3: [(0x78B02C, 192), (0x78D04C, 224), (0x78F8E8, 224), (0x7913D0, 160)],
    4: [(0x798FDC, 224), (0x79CFBC, 128), (0x7A067C, 32), (0x7A469C, 192), (0x7A875C, 224)],
    5: [(0x7AB6EC, 160), (0x7AE000, 192), (0x7B0D3C, 160), (0x7B32F0, 96)],
    6: [(0x7B5050, 192), (0x7B6DFC, 192), (0x7B8554, 64), (0x7B9BC4, 224), (0x7BB2A8, 224), (0x7BDE9C, 192), (0x7BF1D0, 224)],
    7: [(0x7C1834, 224), (0x7C5614, 224), (0x7C6534, 32), (0x7C6FEC, 32)],
    8: [(0x7C9978, 224), (0x7CCCA8, 192), (0x7CE778, 224), (0x7D05B4, 224)],
    9: [(0x7D1D60, 224), (0x7D4BF0, 224), (0x7D71B4, 224), (0x7D8D68, 224), (0x7DB0A0, 192)],
    10: [(0x7DD484, 192), (0x7DF224, 224), (0x7E140C, 160), (0x7E2FC0, 96)],
    11: [(0x7E7084, 224), (0x7EA5E4, 224), (0x7EDD04, 192), (0x7F0884, 128), (0x7F4904, 224)],
    12: [(0x759DA8, 96), (0x76911C, 96), (0x76C9FC, 64), (0x77063C, 160), (0x7732E0, 64)],
    13: [(0x78D04C, 224), (0x792F8C, 224), (0x7949A4, 224), (0x79670C, 224)],
    14: [(0x7F6EAC, 160), (0x7F91AC, 96), (0x7FBCBC, 96), (0x7FE068, 96), (0x800D3C, 96)],
    15: [(0x803020, 224), (0x8052BC, 160), (0x806A2C, 128), (0x8091F4, 224)],
    16: [(0x80B484, 224), (0x80E0FC, 192), (0x80F0F8, 160), (0x8119B4, 224), (0x8155A0, 192), (0x818A08, 224)],
    17: [(0x81A364, 224), (0x81BF30, 224), (0x820010, 224), (0x8240F0, 224), (0x8261B0, 224), (0x827544, 160)],
}
