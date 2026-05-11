# ExportBytesToPython.py  # flake8: noqa
# Exports the current Ghidra listing selection as a Python patch snippet for Archipelago.
# Each row corresponds to one instruction or one defined data item, with assembly/value as a comment.
# ROM file offsets are calculated by subtracting the GBA ROM base (0x08000000).
#
# Usage:
#   1. Select the bytes you want to export in Ghidra's Listing view.
#   2. Run this script (Script Manager or keybind).
#   3. The snippet is printed to the console AND copied to your clipboard.
#
# Install: copy this file into your Ghidra user scripts folder, then add that
#          folder in Script Manager (Manage Script Dirs).
#
# @category GBA
# @menupath Tools.GBA.Export Bytes as Python
# @runtime Jython

import java.awt.Toolkit as Toolkit
import java.awt.datatransfer.StringSelection as StringSelection
from ghidra.program.model.listing import CodeUnit

GBA_ROM_BASE = 0x08000000

selection = currentSelection
if selection is None or selection.isEmpty():
    popup("No bytes selected. Highlight a range in the Listing view first.")
    exit()

memory = currentProgram.getMemory()
listing = currentProgram.getListing()
symbol_table = currentProgram.getSymbolTable()
start = selection.getMinAddress()
end = selection.getMaxAddress()
num_bytes = int(selection.getNumAddresses())

def get_label(addr):
    """Return the primary symbol name at addr, or None."""
    symbols = symbol_table.getSymbols(addr)
    for sym in symbols:
        if not sym.isExternal():
            return sym.getName()
    return None

def get_comment(code_unit):
    """Return EOL or pre-comment from a CodeUnit, or None."""
    eol = code_unit.getComment(CodeUnit.EOL_COMMENT)
    if eol:
        return eol
    return code_unit.getComment(CodeUnit.PRE_COMMENT)

def read_bytes(addr, length):
    return [memory.getByte(addr.add(i)) & 0xFF for i in range(length)]

def format_hex(byte_list):
    return ", ".join("0x{:02X}".format(b) for b in byte_list)

# Build rows: (hex_string, comment_string_or_None)
rows = []
addr = start
while addr is not None and addr <= end:
    instr = listing.getInstructionAt(addr)
    if instr is not None:
        instr_bytes = read_bytes(addr, instr.getLength())
        rows.append((format_hex(instr_bytes), str(instr)))
        addr = addr.add(instr.getLength())
    else:
        data = listing.getDataAt(addr)
        if data is not None and data.getLength() > 0:
            data_bytes = read_bytes(addr, data.getLength())
            # Build a comment: prefer Ghidra comment, then label + value, then just value
            comment = get_comment(data)
            if not comment:
                label = get_label(addr)
                value = data.getDefaultValueRepresentation()
                if label and value:
                    comment = "{}: {}".format(label, value)
                elif label:
                    comment = label
                elif value:
                    comment = value
            rows.append((format_hex(data_bytes), comment))
            addr = addr.add(data.getLength())
        else:
            b = memory.getByte(addr) & 0xFF
            rows.append(("0x{:02X}".format(b), None))
            addr = addr.next()

    if addr is not None and addr > end:
        break

start_offset = start.getOffset() - GBA_ROM_BASE
end_offset = end.getOffset() - GBA_ROM_BASE
if start_offset < 0:
    start_offset = start.getOffset()
    end_offset = end.getOffset()

# Rows whose hex part exceeds this character width get their comment on a separate line above.
# ~5 bytes worth of hex; keeps 2- and 4-byte instruction/pointer rows inline.
LONG_ROW_THRESHOLD = 30

short_hex_lengths = [len(hex_part) for hex_part, _ in rows if len(hex_part) <= LONG_ROW_THRESHOLD]
max_short_len = max(short_hex_lengths) if short_hex_lengths else LONG_ROW_THRESHOLD
comment_col = max_short_len + 3  # hex + comma + 2 spaces minimum before "#"

byte_lines = []
for hex_part, comment in rows:
    if len(hex_part) > LONG_ROW_THRESHOLD:
        if comment is not None:
            byte_lines.append("        # {}".format(comment))
        byte_lines.append("        {},".format(hex_part))
    else:
        spaces = " " * (comment_col - len(hex_part) - 1)
        if comment is not None:
            byte_lines.append("        {},{}# {}".format(hex_part, spaces, comment))
        else:
            byte_lines.append("        {},".format(hex_part))

snippet = (
    "# 0x{start:X} - 0x{end:X} ({n} bytes)\n"
    "patch.write_token(\n"
    "    APTokenTypes.WRITE,\n"
    "    0x{start:X},\n"
    "    bytes([\n"
    "{rows}\n"
    "    ]),\n"
    ")"
).format(
    start=start_offset,
    end=end_offset,
    n=num_bytes,
    rows="\n".join(byte_lines),
)

print("=" * 60)
print(snippet)
print("=" * 60)

clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
clipboard.setContents(StringSelection(snippet), None)
popup("Copied {} bytes from 0x{:X} to clipboard.".format(num_bytes, start_offset))
