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
SHOP_PRICES_ROM_OFFSET = 0x00802D9C
SHOP_PRICES_COUNT = 48
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems, ROM data: one fixed record a slot
SHOP_ITEMS_ROM_OFFSET = 0x00802DFC
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
SEED_CONFIG_ROM_OFFSET = 0x00801638
SEED_CONFIG_SIZE = 8
SEED_CONFIG_FIELDS = {   # ap.h name: (offset, size)
    "requiredDisks": (0, 2),
    "startingWeapons": (2, 1),
    "easyExSkill": (3, 1),
    "itemsanity": (4, 1),
    "exLifeSanity": (5, 1),
    "unused": (6, 1),
}

# Stage id: the ROM offset and byte size of each BG palette
STAGE_PALETTES = {
    1: [(0x7081F0, 96), (0x70AD50, 128), (0x70E810, 192), (0x711390, 192), (0x713524, 128)],
    2: [(0x7257F4, 192), (0x7294B4, 192), (0x72CF34, 192), (0x730F74, 224), (0x732F80, 192), (0x734F14, 192), (0x7364D8, 96)],
    3: [(0x739474, 192), (0x73B494, 224), (0x73DD30, 224), (0x73F818, 160)],
    4: [(0x747424, 224), (0x74B404, 128), (0x74EAC4, 32), (0x752AE4, 192), (0x756BA4, 224)],
    5: [(0x759B34, 160), (0x75C448, 192), (0x75F184, 160), (0x761738, 96)],
    6: [(0x763498, 192), (0x765244, 192), (0x76699C, 64), (0x76800C, 224), (0x7696F0, 224), (0x76C2E4, 192), (0x76D618, 224)],
    7: [(0x76FC7C, 224), (0x773A5C, 224), (0x77497C, 32), (0x775434, 32)],
    8: [(0x777DC0, 224), (0x77B0F0, 192), (0x77CBC0, 224), (0x77E9FC, 224)],
    9: [(0x7801A8, 224), (0x783038, 224), (0x7855FC, 224), (0x7871B0, 224), (0x7894E8, 192)],
    10: [(0x78B8CC, 192), (0x78D66C, 224), (0x78F854, 160), (0x791408, 96)],
    11: [(0x7954CC, 224), (0x798A2C, 224), (0x79C14C, 192), (0x79ECCC, 128), (0x7A2D4C, 224)],
    12: [(0x7081F0, 96), (0x717564, 96), (0x71AE44, 64), (0x71EA84, 160), (0x721728, 64)],
    13: [(0x73B494, 224), (0x7413D4, 224), (0x742DEC, 224), (0x744B54, 224)],
    14: [(0x7A52F4, 160), (0x7A75F4, 96), (0x7AA104, 96), (0x7AC4B0, 96), (0x7AF184, 96)],
    15: [(0x7B1468, 224), (0x7B3704, 160), (0x7B4E74, 128), (0x7B763C, 224)],
    16: [(0x7B98CC, 224), (0x7BC544, 192), (0x7BD540, 160), (0x7BFDFC, 224), (0x7C39E8, 192), (0x7C6E50, 224)],
    17: [(0x7C87AC, 224), (0x7CA378, 224), (0x7CE458, 224), (0x7D2538, 224), (0x7D45F8, 224), (0x7D598C, 160)],
}
