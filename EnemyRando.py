"""Enemy randomization. Only done when the option for it is enabled.

This file here does several things.
  1. Swap the sprite sheets. The enemies that have replaced the fewest so far this seed are tried first, 
     so the same few smaller enemies are not placed everywhere.
  2. Merge palette slots so that enemies can share them.
  3. Account for Extra enemies and load them into stages that didn't usually have them.
  4. Check per spawn location and decide what should go there.

You should probably read through EnemyData.py to understand a lot of this. It uses variable names pulled from the
decomp that I tend to rename myself if I find them too strange. Sorry that can cause confusion in a lot of areas.

The stage's table is organized by rows. Each row contains information saying to load a sprite sheet into tiles in video memory,
load a color palette for those tiles, in specific level areas, and in specific modes (normal, mettaur, cyber, and mettaur+cyber)

These stage rows will be changed along with the spawn points, since they are needed to actually render the enemies.

I also use these names interchangably by mistake, but for the enemy spawning:
   
    spawn point: The one single location where vanilla places an enemy. Used as a base for the randomizer spawn spots.
    
    spawn spot: Multiple of these per spawn point. Can be placed on the ground, a little in the air,
    embedded in the ground, on a nearby wall, or nearby ceiling, or a hand placed spot in specific enemies. 
    These are where the randomizer actually puts enemies. Each enemy uses one specific spawn spot based on its spawn requirements.
"""

from typing import Dict, List, Set, Tuple

from . import EnemyData as D

ENTITY_ENEMY = 3
HEAVY = D.HEAVY_CANNON["id"]
PLACEABLE = {"FLOOR", "CEILING", "WALL_LEFT", "WALL_RIGHT", "AIR", "EMBEDDED"}
MODES = {"normal": (1, 1), "mettaur": (2, 1), "cyber": (1, 2), "mettaur_cyber": (2, 2)}

BURNABLE_WOOD = 34   # level geometry and not an actual enemy
ICE_BLOCK = 63       # the Ice Base ice block, a platform

# Hammers must be in their vanilla spots, snakecords can be moved though not sure why that is here???
SNAKECORD, HAMMER = 20, 21

# how many points back a point looks to avoid repeating an enemy.
NEIGHBORS = 4       

# Stuff for Packs. 
# Makes each spawn point spawn more than one enemy, based on the "difficulty" of the enemy that is being replaced.
# A pack's other enemies are new spawn points, known as a COMPANION
# The density cap prevents too many enemies from appearing, which is based on the vanilla game's most crowded screen.
PACK_MAX = 3            
COMPANION = 0x40
DENSITY_WINDOW, DENSITY_CAP = 15, 10
UNKILLABLE_TOUGHNESS = 6 # Rating for unkillable enemies.

MARK_SHIFT = 2
NO_ENEMY = 0xFFFF
SPAWNED = {variant[0] for variant in D.VARIANTS}


def motion(enemy_id: int) -> int:
    return D.SPECIES[enemy_id]["motion"]


def spot_free(enemy_id: int, counted: Set[int]) -> bool:
    """Whether an enemy spawn point can be replaced by a different enemy."""
    species = D.SPECIES[enemy_id]
    makes_others = set(species["makes"]) - {enemy_id}
    return (species["motion"] is not None
            and enemy_id not in (BURNABLE_WOOD, ICE_BLOCK, SNAKECORD, HAMMER)
            and not makes_others & counted)


def movable(enemy_id: int) -> bool:
    """Whether an enemy can be moved to another spawn point."""
    species = D.SPECIES[enemy_id]
    return (enemy_id in SPAWNED and species["motion"] is not None and species["hurt"] != "?"
            and set(species["makes"]) <= {enemy_id}
            and enemy_id not in (BURNABLE_WOOD, ICE_BLOCK))


def sheets_of(enemy_id: int) -> tuple:
    """Returns the enemy's own sheet first, then any others."""
    return (motion(enemy_id),) + tuple(D.SPECIES[enemy_id]["sheets"])


# a sprite sheet's cyberColor byte.
CYBER = {}
for _stage in D.STAGES.values():
    for _row in _stage["preload_rows"]:
        CYBER[_row[0]] = max(CYBER.get(_row[0], 0), _row[6])


def killable(enemy_id: int) -> bool:
    """Whether an enemy can be killed, and its kill counts for a disk, meaning it can be in a disk marked spot."""
    return D.SPECIES[enemy_id]["hurt"] == "yes" and D.SPECIES[enemy_id]["counts_kills"]


def is_candidate(enemy_id: int) -> bool:
    """Whether an enemy can be placed at another enemy's spawn point:"""
    if not movable(enemy_id):
        return False
    for variant, (spawn_requirement, _below, _above) in D.VARIANTS.items():
        if variant[0] == enemy_id and spawn_requirement in PLACEABLE:
            return True
    return False


CANDIDATES = sorted(enemy_id for enemy_id in D.SPECIES if is_candidate(enemy_id))
if D.HEAVY_CANNON_AT:
    CANDIDATES.append(HEAVY)


def toughness(variant) -> int:
    """Hit points of an enemy's strongest section."""
    enemy_id, _work0, _work1 = variant
    species = D.SPECIES[enemy_id]
    if species["hurt"] != "yes" or species["hp"] is None:
        return UNKILLABLE_TOUGHNESS
    return species["hp"]


def entity(variant) -> tuple:
    """The template fields (kind, id, work0, work1) for a variant. 
    Heavy Cannons are actually handled in game as a solid.."""
    enemy_id, work0, work1 = variant
    if enemy_id == HEAVY:
        return D.HEAVY_CANNON["kind"], D.HEAVY_CANNON["solid"], work0, work1
    return ENTITY_ENEMY, enemy_id, work0, work1


def drop_enemy(drop) -> int:
    """The enemy a disk drop row counts kills of, or None if no spawn point places it."""
    _stage, _stage2, _zako, kind, enemy_id = drop[:5]
    if kind == ENTITY_ENEMY:
        return enemy_id
    if (kind, enemy_id) == (D.HEAVY_CANNON["kind"], D.HEAVY_CANNON["solid"]):
        return HEAVY
    return None


def headroom(enemy_id: int, spawn_requirement: str, vanilla_above: int) -> int:
    """Tiles that the enemy needs above it in order to spawn."""
    if spawn_requirement == "FLOOR":
        return min(vanilla_above, D.SPECIES[enemy_id]["reach_above"])
    return vanilla_above


def palette_group(sheet: int):
    """The shared palette that sheet draws with (EnemyData.MERGED), or None for its own sheet."""
    merged = D.MERGED.get(sheet)
    return None if merged is None else merged[0]


def by_cell(table: dict) -> dict:
    """EnemyData.py's CLAIMS / PALETTE_CLAIMS for one stage."""
    return {(area, mode): value[mode] if isinstance(value, dict) else value
            for area, value in table.items() for mode in MODES}


def loaded(rows, sheet: int) -> Set[Tuple[int, str]]:
    """Every cell a row loads in."""
    cells = set()
    for row_sheet, area_mask, _tile, _palette, bits_05, bits_06, _cyber in rows:
        if row_sheet != sheet:
            continue
        for area in range(8):
            if not area_mask >> area & 1:
                continue
            for mode, (need_05, need_06) in MODES.items():
                if bits_05 & need_05 and bits_06 & need_06:
                    cells.add((area, mode))
    return cells


def stage_points(stage_id: int) -> list:
    """
    Returns a list of spawn points for a stage.
    mark: disk drop row
    Contains information from EnemyData.py as well as:
    kept: Enemies or spots that are never changed (currently empty and unused)
    free: is in spot_free
    pillar_room: an area that has room for the pillar art, which determines if a pillar cannon can spawn there.
    """
    stage = D.STAGES[stage_id]
    templates = stage["enemy_templates"]
    vanilla_rows = stage["preload_rows"]
    counted_here = {drop_enemy(drop) for drop in D.DROPS if drop[0] == stage_id} - {None}
    points = []
    for index, template, x, y, spots, pack in stage["enemy_spawn_points"]:
        enemy_id, work0, work1 = templates[template][1:4]
        seen_in = {area for area, _mode in loaded(vanilla_rows, motion(enemy_id))
                   & by_cell(D.CLAIMS[stage_id]).keys()}   # areas reachable in gameplay
        points.append(dict(index=index, template=template, enemy_id=enemy_id, work0=work0,
                           work1=work1, x=x, y=y, spots=spots, pack=pack,
                           kept=(stage_id, index) in D.NEVER_CHANGES,
                           free=(spot_free(enemy_id, counted_here)
                                 and (stage_id, index) not in D.NEVER_CHANGES),
                           # Checks if room is there for the new pillar art
                           pillar_room=all((stage_id, area) in D.PILLAR["areas"]
                                           for area in seen_in)))

    drop_groups = {}     # drop row: (vanilla enemy, the spawn points whose kills count for it)
    for row_index, drop in enumerate(D.DROPS):
        drop_stage, work0, enemy_id = drop[0], drop[5], drop_enemy(drop)
        if drop_stage == stage_id and enemy_id is not None:
            drop_groups[row_index] = (enemy_id, {
                point["index"] for point in points
                if point["enemy_id"] == enemy_id and (work0 == 0xFFFF or point["work0"] == work0)})
    # disk spawn points get the AP logo and count kills by the spawn spot instead of by enemy type
    mark_of = {}
    for row_index, (_enemy_id, group) in drop_groups.items():
        if group and all(point["free"] or point["kept"]
                         for point in points if point["index"] in group):
            mark_of.update((index, row_index + 1) for index in group)
    for point in points:
        point["mark"] = mark_of.get(point["index"], 0)
    return points


def needs_pillar(point, offset):
    """Whether a Pillar Cannon needs new pillar art, or is a vanilla spawn."""
    return point["enemy_id"] != D.PILLAR["enemy"] or offset != (0, 0)


def placements(stage_id: int, candidate: int, point: dict, spots=None) -> list:
    """Whether or not an enemy can spawn on a chosen stage and point."""
    fits = []
    if not killable(candidate) and point["mark"]:
        return fits
    # Heavy cannons had to be manually placed due to their uniqueness.
    height = D.HEAVY_CANNON_AT.get((stage_id, point["index"]))
    if candidate == HEAVY and point["enemy_id"] != HEAVY and height is None:
        return fits
    swimmer = candidate in D.SWIMMERS
    if swimmer and point["enemy_id"] not in D.SWIMMERS:
        return fits
    for dx, dy, standable_as, room_below, room_above in spots or point["spots"]:
        if swimmer and (dx, dy) != (0, 0):
            continue
        if (candidate == D.PILLAR["enemy"] and needs_pillar(point, (dx, dy))
                and (room_below > D.PILLAR["floor"] or not point["pillar_room"])):
            continue
        if candidate in D.ON_SLOPES and "SLOPE" in standable_as:
            standable_as = standable_as + ("FLOOR",)
        for variant, (spawn_requirement, need_below, need_above) in D.VARIANTS.items():
            if candidate == HEAVY and height is not None and variant[1] != height:
                continue
            if (variant[0] == candidate and spawn_requirement in standable_as
                    and room_below >= need_below
                    and room_above >= headroom(candidate, spawn_requirement, need_above)):
                fits.append((variant, (dx, dy)))
    return fits


def randomize_stage(stage_id: int, rng, used: Dict[int, int], difficulty: float) -> dict:
    """Randomize one stage's enemies."""
    stage = D.STAGES[stage_id]
    templates = stage["enemy_templates"]
    vanilla_rows = stage["preload_rows"]
    made_here = set(stage["made_here"])
    points = stage_points(stage_id)
    marked = sorted({point["mark"] - 1 for point in points if point["mark"]})

    placed_here = {point["enemy_id"] for point in points}
    # the sprite sheets from the vanilla game, normal modes only so that mettaur and virus mode enemis can spawn
    sheets_here = {row[0] for row in vanilla_rows
                   if any(mode == "normal" for _area, mode in loaded([row], row[0]))}
    palette_claims = by_cell(D.PALETTE_CLAIMS[stage_id])
    claimed_tiles = {cell: {tile for first, end in runs for tile in range(first, end)}
                     for cell, runs in by_cell(D.CLAIMS[stage_id]).items()}

    def room_for(old_enemy, new_enemy, replacement_for):
        """Whether the new enemy's sprite sheet fits where the old one was loaded.
        It can only be bigger if the extra tiles aren't used by anything else."""
        old_size = D.MOTIONS[motion(old_enemy)][0]
        new_size = D.MOTIONS[motion(new_enemy)][0]
        if new_size <= old_size:
            return True
        size_of = {row[0]: D.MOTIONS[row[0]][0] for row in vanilla_rows}
        for swapped_out, swapped_in in replacement_for.items():
            size_of[motion(swapped_out)] = D.MOTIONS[motion(swapped_in)][0]
        for row in vanilla_rows:
            if row[0] != motion(old_enemy):
                continue
            first_tile = row[2]
            grown = set(range(first_tile + old_size, first_tile + new_size))
            if first_tile + new_size > 1024:
                return False
            for cell in loaded([row], row[0]) & claimed_tiles.keys():
                if grown & claimed_tiles[cell]:
                    return False
                for other in vanilla_rows:
                    if other[0] != motion(old_enemy) and cell in loaded([other], other[0]) \
                            and grown & set(range(other[2], other[2] + size_of[other[0]])):
                        return False
        return True

    # 1. swap the sprite sheets, try the enemies that have replaced the fewest so far first
    replacement_for: Dict[int, int] = {}
    for old_enemy in sorted(placed_here - made_here):
        if old_enemy == HEAVY:
            continue        # since swapping its sheet away would leave no Heavy Cannon for the stage
        own_points = [point for point in points if point["enemy_id"] == old_enemy]
        if not all(point["free"] for point in own_points):
            continue
        old_palettes = D.MOTIONS[motion(old_enemy)][1]
        options = []
        for candidate in CANDIDATES:
            if (motion(candidate) not in sheets_here
                    and not loaded(vanilla_rows, motion(candidate))
                    & loaded(vanilla_rows, motion(old_enemy))
                    and candidate not in replacement_for.values()
                    and not D.SPECIES[candidate]["sheets"]   # excludes enemies needing a second sheet
                    and D.MOTIONS[motion(candidate)][1] <= old_palettes
                    and all(placements(stage_id, candidate, point) for point in own_points)
                    and room_for(old_enemy, candidate, replacement_for)):
                options.append(candidate)
        if options:
            fewest = min(used.get(candidate, 0) for candidate in options)
            chosen = rng.choice([candidate for candidate in options
                                 if used.get(candidate, 0) == fewest])
            replacement_for[old_enemy] = chosen
            used[chosen] = used.get(chosen, 0) + 1

    replacement_sheet = {motion(old): motion(new) for old, new in replacement_for.items()}
    rows = [(replacement_sheet.get(row[0], row[0]), *row[1:]) for row in vanilla_rows]


    # 2. Palette slot merging: 
    def taken(cell, leaving=None):
        """Gets tiles and palettes that are used in the given cell."""
        tiles = set(claimed_tiles.get(cell, ()))
        palettes = dict.fromkeys(palette_claims.get(cell, ()))
        for index, row in enumerate(rows):
            if index == leaving or cell not in loaded([row], row[0]):
                continue
            tile_count, palette_count = D.MOTIONS[row[0]]
            tiles |= set(range(row[2], row[2] + tile_count))
            group = palette_group(row[0])
            for slot in range(row[3], row[3] + palette_count):
                palettes[slot] = group if palettes.get(slot, group) == group else None
        return tiles, palettes

    def palette_slot(sheet, cells, leaving=None):
        """Returns the palette slot that the sheet can load into."""
        group = palette_group(sheet)
        count = D.MOTIONS[sheet][1]
        held = [taken(cell, leaving)[1] for cell in cells]

        def fits(first):
            return all(slot not in palettes or (group is not None and palettes[slot] == group)
                       for palettes in held for slot in range(first, first + count))

        def shared(first):
            return sum(group is not None and palettes.get(first) == group for palettes in held)

        options = [first for first in range(16 - count + 1) if fits(first)]
        return max(options, key=lambda first: (shared(first), -first), default=None)

    for index, row in enumerate(rows):
        if palette_group(row[0]) is None:
            continue
        cells = loaded([row], row[0]) & claimed_tiles.keys()
        held = [taken(cell, index)[1] for cell in cells]
        if any(palettes.get(row[3], palette_group(row[0])) != palette_group(row[0])
               for palettes in held):
            continue
        slot = palette_slot(row[0], cells, index)
        staying = sum(palettes.get(row[3]) == palette_group(row[0]) for palettes in held)
        moving = sum(palettes.get(slot) == palette_group(row[0]) for palettes in held)
        if moving > staying:
            rows[index] = (*row[:3], slot, *row[4:])


    # 3. add extra enemies into the stage that did not previously have them
    def choices(point):
        """What each of a spawn point's spawn locations can hold."""
        needed_cells = loaded(vanilla_rows, motion(point["enemy_id"]))
        out = {candidate for candidate in CANDIDATES
               if candidate not in made_here
               and all(needed_cells <= loaded(rows, sheet) for sheet in sheets_of(candidate))
               and placements(stage_id, candidate, point)}
        if all(needed_cells <= loaded(rows, sheet) for sheet in sheets_of(point["enemy_id"])):
            out.add(point["enemy_id"])
        return out

    free_points = [point for point in points if point["free"]]
    while len(rows) + 1 < stage["preload"][1]:
        weight = {point["index"]: 1 / (1 + len(choices(point))) for point in free_points}
        loading = {row[0] for row in rows
                   if any(mode == "normal" for _area, mode in loaded([row], row[0]))}
        best = None
        for candidate in CANDIDATES:
            if motion(candidate) in loading or candidate in made_here:
                continue
            served_by_cells = {}
            for point in free_points:
                if placements(stage_id, candidate, point):
                    cells = frozenset(loaded(vanilla_rows, motion(point["enemy_id"])))
                    served_by_cells.setdefault(cells, []).append(point)
            for cells, served in served_by_cells.items():
                area_mask = bits_05 = bits_06 = 0
                for area, mode in cells:
                    area_mask |= 1 << area
                    bits_05 |= MODES[mode][0]
                    bits_06 |= MODES[mode][1]
                row_cells = loaded([(0, area_mask, 0, 0, bits_05, bits_06, 0)], 0)
                if loaded(rows, motion(candidate)) & row_cells:
                    continue                    
                reachable = row_cells & claimed_tiles.keys()
                fitted, added = [], 0
                try:
                    for sheet in sheets_of(candidate):
                        have = loaded(rows, sheet) & row_cells
                        if have == row_cells and sheet != motion(candidate):
                            continue
                        if have:
                            fitted = None
                            break
                        busy_tiles = set()
                        for cell in reachable:
                            busy_tiles |= taken(cell)[0]
                        tile, free_run = None, 0 
                        for first in range(1023, 511, -1):
                            free_run = 0 if first in busy_tiles else free_run + 1
                            if free_run == D.MOTIONS[sheet][0]:
                                tile = first
                                break
                        palette = palette_slot(sheet, reachable)
                        if tile is None or palette is None:
                            fitted = None
                            break
                        fitted.append((sheet, area_mask, tile, palette, bits_05, bits_06,
                                       CYBER.get(sheet, 0)))
                        rows.append(fitted[-1])
                        added += 1
                finally:
                    del rows[len(rows) - added:]
                if not fitted:
                    continue
                score = (candidate == HEAVY, sum(weight[point["index"]] for point in served),
                         -used.get(candidate, 0), rng.random())
                if best is None or score > best[0]:
                    best = (score, fitted, candidate)
        if best is None:
            break
        _score, fitted, candidate = best
        rows.extend(fitted)
        used[candidate] = used.get(candidate, 0) + 1

    # 4. Go through the stage from left to right and pick which enemy and position to spawn them at for each spawn point.
    choice_at = {}       
    recent = []          

    def budget(point):
        return toughness((point["enemy_id"], point["work0"], point["work1"])) * difficulty

    def most(enemy, point):
        """Gets the max toughness that an enemy can bring to a specific point."""
        places = {offset for _variant, offset in placements(stage_id, enemy, point, point["pack"])}
        tough = max((toughness(variant) for variant, _offset in placements(stage_id, enemy, point)),
                    default=toughness((enemy, point["work0"], point["work1"])))
        return tough * (1 + (min(len(places), PACK_MAX - 1) if enemy != HEAVY else 0))

    for point in sorted(points, key=lambda point: point["x"]):
        own = point["enemy_id"]
        options = choices(point) if point["free"] else set()
        if not options:
            recent.append(own)                      # stay vanilla
            continue
        if HEAVY in options and (stage_id, point["index"]) in D.HEAVY_CANNON_AT:
            options = {HEAVY}               
        reach = {enemy: most(enemy, point) for enemy in options}
        enough = {enemy for enemy in options if reach[enemy] >= budget(point) or enemy == own}
        options = enough or {enemy for enemy in options if reach[enemy] == max(reach.values())}
        nearby = recent[-NEIGHBORS:]
        fewest = min(nearby.count(enemy) for enemy in options)
        options = sorted(enemy for enemy in options if nearby.count(enemy) == fewest)
        if len(options) > 1 and own in options:
            options.remove(own)
        enemy = rng.choices(options, [1 / (1 + used.get(e, 0)) for e in options])[0]
        used[enemy] = used.get(enemy, 0) + 1
        recent.append(enemy)
        if enemy != own:
            choice_at[point["index"]] = rng.choice(placements(stage_id, enemy, point))

    # packs: If an enemy is replacing another enemy that previously had more health than it,
    # spawn duplicates of that new enemy to match the old enemies health value (or get close to it).
    # Multiplied based on difficulty, though this might get removed later.
    # The multiplier can place more enemies into a vanilla spot too. ^
    placed = []          # (x, y, enemy)
    for point in points:
        variant, (dx, dy) = choice_at.get(point["index"], ((point["enemy_id"],), (0, 0)))
        placed.append((point["x"] + dx, point["y"] + dy, variant[0]))
    companions = []      # (x, y, variant, the spawn point it belongs to)

    def crowded(x):
        xs = [p[0] for p in placed]
        return any(sum(w <= other < w + DENSITY_WINDOW for other in xs) + 1 > DENSITY_CAP
                   for w in range(x - DENSITY_WINDOW + 1, x + 1))

    def overlaps(x, y, enemy):
        return any(abs(py - y) <= 1 and abs(px - x) < max(D.SPECIES[enemy]["wide"],
                                                          D.SPECIES[other]["wide"])
                   for px, py, other in placed)

    for point in sorted(points, key=lambda point: point["x"]):
        if not point["free"]:
            continue
        variant, (dx, dy) = choice_at.get(
            point["index"], ((point["enemy_id"], point["work0"], point["work1"]), (0, 0)))
        if variant[0] == HEAVY:
            continue
        have = toughness(variant)
        members, side = [(dx, dy)], 1
        spacing = D.SPECIES[variant[0]]["wide"] + 1
        fits = placements(stage_id, variant[0], point, point["pack"])
        rng.shuffle(fits)
        while have < budget(point) and len(members) < PACK_MAX:
            room = [(extra, (px, py)) for extra, (px, py) in fits
                    if all(abs(px - mx) >= spacing for mx, _my in members)
                    and not crowded(point["x"] + px)
                    and not overlaps(point["x"] + px, point["y"] + py, extra[0])]
            if not room:
                break
            extra, (px, py) = min(room, key=lambda f: (abs(f[1][0] - dx), (f[1][0] - dx) * side < 0,
                                                       abs(f[1][1] - dy)))
            side = -1 if px > dx else 1             # the next goes on the other side of the base enemy
            members.append((px, py))
            x, y = point["x"] + px, point["y"] + py
            companions.append((x, y, extra, point))
            placed.append((x, y, extra[0]))
            have += toughness(extra)

    # Extra rows that were never used can be dropped.
    held_sheets = {sheet for enemy in recent for sheet in sheets_of(enemy)}
    rows = rows[:len(vanilla_rows)] + [row for row in rows[len(vanilla_rows):]
                                       if row[0] in held_sheets]

    # templates: for enemies that changed, or are marked with the AP logo graphic.
    first_new_template = stage["templates"][1]
    new_templates, template_index, repoint, moves = [], {}, {}, {}
    for point in points:
        own = (point["enemy_id"], point["work0"], point["work1"])
        variant, (dx, dy) = choice_at.get(point["index"], (own, (0, 0)))
        mark = point["mark"]
        if (dx, dy) != (0, 0):
            moves[point["index"]] = (point["x"] + dx, point["y"] + dy)
        if variant == own and not mark:
            continue
        flag, _enemy, _work0, _work1, attr, mettaur_id, virus_id = templates[point["template"]]
        if variant[0] == D.PILLAR["enemy"] and needs_pillar(point, (dx, dy)):
            flag |= D.PILLAR["flag"]
        template = (flag, *entity(variant), attr | mark << MARK_SHIFT, mettaur_id, virus_id)
        if template not in template_index:
            template_index[template] = first_new_template + len(new_templates)
            new_templates.append(template)
        repoint[point["index"]] = template_index[template]

    pack_points = []
    for x, y, variant, point in companions:
        flag, _enemy, _work0, _work1, attr, mettaur_id, virus_id = templates[point["template"]]
        flag |= COMPANION
        if variant[0] == D.PILLAR["enemy"]:
            flag |= D.PILLAR["flag"]
        template = (flag, *entity(variant), attr & ((1 << MARK_SHIFT) - 1), mettaur_id, virus_id)
        if template not in template_index:
            template_index[template] = first_new_template + len(new_templates)
            new_templates.append(template)
        pack_points.append((x, y, template_index[template], point["index"]))
    return dict(templates=new_templates, repoint=repoint, moves=moves, rows=rows,
                marked=marked, pack=pack_points)


def randomize(rng, difficulty: float = 1.0) -> dict:
    """
    Randomize each level in order of ID (TODO could be randomized if thats better). 
    Keeps the used variable so that other stages can prioritize unused enemies.
    """
    used: Dict[int, int] = {}
    return {stage_id: randomize_stage(stage_id, rng, used, difficulty)
            for stage_id in sorted(D.STAGES)}


def writes(result: dict) -> List[Tuple[int, bytes]]:
    """ROM offset and bytes to be written into the ROM during patch time."""
    out = []
    for stage_id, stage_result in result.items():
        stage = D.STAGES[stage_id]
        templates_offset, vanilla_count, capacity = stage["templates"]
        assert vanilla_count + len(stage_result["templates"]) <= capacity, stage_id
        if stage_result["templates"]:
            out.append((templates_offset + vanilla_count * 8,
                        b"".join(bytes(template) for template in stage_result["templates"])))
        table = []
        for index, (x, y, template) in enumerate(stage["all_spawn_points"]):
            x, y = stage_result["moves"].get(index, (x, y))
            table.append((x, y, stage_result["repoint"].get(index, template)))
        for x, y, template, _spot in sorted(stage_result["pack"]):
            at = next((i for i, row in enumerate(table) if i and row[0] > x), len(table))
            table.insert(at, (x, y, template))
        table.append((0x7FFFFFFF, 32767, 0)) 
        assert len(table) <= stage["spawn_point_capacity"], stage_id
        out.append((stage["spawn_points"], b"".join(
            x.to_bytes(4, "little", signed=True) + y.to_bytes(2, "little", signed=True)
            + template.to_bytes(2, "little") for x, y, template in table)))
        table = bytearray()
        for sheet, area_mask, tile, palette, bits_05, bits_06, cyber in stage_result["rows"]:
            table += (bytes([sheet, area_mask]) + tile.to_bytes(2, "little")
                      + bytes([palette, bits_05, bits_06, cyber]))
        table += bytes([0xFF]) + bytes(7)           # FF is terminator
        out.append((stage["preload"][0], bytes(table)))

    marked = {row_index for stage_result in result.values() for row_index in stage_result["marked"]}
    drops = bytearray()
    for row_index, row in enumerate(D.DROPS):
        row = list(row)
        if row_index in marked:
            row[4] = NO_ENEMY                      
        for field in row:
            drops += field.to_bytes(2, "little")
    out.append((D.DROPS_OFFSET, bytes(drops)))
    return out


def recolor(rom: bytearray) -> None:
    """Redraw every sprite sheet in EnemyData.MERGED to share color palettes."""
    def remap_tiles(tiles, size, remap):
        rom[tiles:tiles + size] = bytes(remap[byte & 15] | remap[byte >> 4] << 4
                                        for byte in rom[tiles:tiles + size])

    for group, tiles, size, palette, remap in D.MERGED.values():
        remap_tiles(tiles, size, remap)
        rom[palette:palette + 32] = b"".join(color.to_bytes(2, "little")
                                             for color in D.PALETTE_GROUPS[group])
    # Pillar cannon new art
    cannon = D.MERGED.get(motion(D.PILLAR["enemy"]))
    if cannon is not None:
        remap_tiles(D.PILLAR["tiles"], D.PILLAR["size"], cannon[4])
