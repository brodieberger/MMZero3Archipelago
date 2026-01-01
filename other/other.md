# Mega Man Zero 3 – Ghidra Analysis XML

This folder contains my Ghidra analysis exports for Mega Man Zero 3.  
The XML files restore my function names, labels, comments when imported into Ghidra.  
No ROM data is included.

There are two analyses:

- **Japanese ROM**  
  Used as a reference alongside an existing decompilation.  
  Decomp project: https://github.com/mmzret/rmz3/

- **USA ROM**  
  The primary ROM being modified and documented.  
  Contains notes related to custom logic, hooks, and Archipelago integration.


## How to Use

1. Open Ghidra and create a new project
2. Import the `.gba` file
3. Use processor:
   - ARMv4T
   - Little Endian
   - Default Compiler
4. Let Ghidra finish analysis
5. With the program open, go to:
   - `File → Import → XML`
6. Import the matching XML file

After importing, all documented functions, labels, and comments will appear automatically.

Check out this document if you want to learn more about reverse engineering: https://www.starcubelabs.com/reverse-engineering-gba