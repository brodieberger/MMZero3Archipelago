from dataclasses import dataclass
import os
import Utils
from worlds.Files import APProcedurePatch

from settings import get_settings
import settings

class MMZero3ProcedurePatch(APProcedurePatch):
    game = "Mega Man Zero 3"
    hash = "aa1d5eeffcd5e4577db9ee6d9b1100f9"
    patch_file_ending = ".apmmzero3"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["mmz3-ap.bsdiff4"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        file_name = get_settings().MMZero3_settings["rom_file"]
        if not os.path.exists(file_name):
          file_name = Utils.user_path(file_name)
        with open(file_name, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes

class MMZero3Settings(settings.Group):
    class MMZero3RomFile(settings.UserFilePath):
        """File name of your Mega Man Zero 3 (USA) """
        required = True
        description = "Mega Man Zero 3 (USA) ROM File"
        copy_to = "Mega Man Zero 3 (USA).gba"
        md5s = [MMZero3ProcedurePatch.hash]


    rom_file: MMZero3RomFile = MMZero3RomFile(MMZero3RomFile.copy_to)