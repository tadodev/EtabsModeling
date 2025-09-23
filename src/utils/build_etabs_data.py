from typing import List, Tuple, Dict, Any
import math

# adjust imports to your project layout
from utils.dxf_processing import read_dxf_plan
from utils.get_elements import get_columns, get_walls, get_slabs
from utils.excel_processing import (
    read_story_table,
    read_column_table,
    read_wall_table,
    read_coupling_beam_table,
    read_slab_table,
)
from models.element_infor import Story, Column, Wall, CouplingBeam, Slab

# -----------------------
# Utilities
# -----------------------
EPS = 1e-3


def _round_key(x: float) -> float:
    """Round elevation key to avoid tiny float differences."""
    return round(float(x), 6)


def build_story_mappings(stories: List[Story]):
    """
    Build:
      - heights_list (bottom-up) for extrusion
      - base_map: base_elevation -> level_name (bottom elevation)
      - top_map: top_elevation -> level_name (top elevation)
    Assumes `stories` are in top-down order (e.g. L44, L43, ...).
    """
    # Ensure we interpret 'stories' as top-down, convert to bottom-up order
    bottom_up = list(reversed(stories))

    heights = [float(s.height) for s in bottom_up]  # bottom-up heights
    base_map: Dict[float, str] = {}
    top_map: Dict[float, str] = {}

    z = 0.0
    for s in bottom_up:
        base_map[_round_key(z)] = s.level
        z_next = z + float(s.height)
        top_map[_round_key(z_next)] = s.level
        z = z_next

    return heights, base_map, top_map


def find_level_by_base_elev(base_map: Dict[float, str], z_value: float) -> str | None:
    """Find the story level whose base_elevation is closest to z_value (within EPS)."""
    z_key = _round_key(z_value)
    if z_key in base_map:
        return base_map[z_key]
    # fallback: nearest
    nearest = min(base_map.keys(), key=lambda k: abs(k - z_value))
    if abs(nearest - z_value) <= EPS:
        return base_map[nearest]
    # not found
    return None


def find_level_by_top_elev(top_map: Dict[float, str], z_value: float) -> str | None:
    z_key = _round_key(z_value)
    if z_key in top_map:
        return top_map[z_key]
    nearest = min(top_map.keys(), key=lambda k: abs(k - z_value))
    if abs(nearest - z_value) <= EPS:
        return top_map[nearest]
    return None


def nearest_level_for_z(base_map: Dict[float, str], top_map: Dict[float, str], z_value: float) -> str:
    """Try base_map then top_map, else nearest base name."""
    l = find_level_by_base_elev(base_map, z_value)
    if l:
        return l
    l = find_level_by_top_elev(top_map, z_value)
    if l:
        return l
    # fallback: nearest base
    nearest = min(base_map.keys(), key=lambda k: abs(k - z_value))
    return base_map[nearest]


# -----------------------
# Merge functions
# -----------------------
def _to_pyfloat_triplet(pt):
    """Convert possible np.float64 to plain python floats (x,y,z)."""
    x, y, z = pt
    return float(x), float(y), float(z)


def merge_columns(
        columns_geo: List[List[Tuple[float, float, float]]],
        story_base_map: Dict[float, str],
        excel_columns: List[Column],
) -> List[Dict[str, Any]]:
    """
    columns_geo: list of stacks; each stack is a list of top points (z = cumulative top) in bottom-up story order.
                 e.g. [(x,y,top1),(x,y,top2),...]
    Returns list of dicts:
        {
          "level": "L44",    # level name for this story segment
          "prop": Column(...),  # matching excel Column by level
          "geom": ((x,y,z_bot),(x,y,z_top))
        }
    """
    merged = []
    # Create quick index of excel column props by level name
    prop_by_level = {c.level: c for c in excel_columns}

    for stack in columns_geo:
        # ensure floats
        pts = [_to_pyfloat_triplet(p) for p in stack]
        # build segments between bottoms and tops
        prev_z = 0.0
        x, y, _ = pts[0]  # plan coords
        for top_pt in pts:
            tx, ty, tz = top_pt
            # bottom = prev_z, top = tz
            level_name = find_level_by_base_elev(story_base_map, prev_z)
            prop = prop_by_level.get(level_name)
            merged.append({
                "level": level_name,
                "prop": prop,  # may be None if not present in excel
                "geom": ((float(x), float(y), float(prev_z)), (float(tx), float(ty), float(tz)))
            })
            prev_z = tz
    return merged


def merge_walls(
        walls_geo: List[List[Tuple[Tuple[float, float, float], ...]]],
        story_base_map: Dict[float, str],
        excel_walls: List[Wall],
) -> List[Dict[str, Any]]:
    """
    walls_geo: list (one entry per plan wall) each entry is a list of quads per story:
        [ ( (x1,y1,z_bot),(x2,y2,z_bot),(x2,y2,z_top),(x1,y1,z_top) ), ... ]
    Returns list of dicts:
        { "level": level, "prop": Wall(...), "geom": [ (x1,y1,z1), ...] }  # quad coordinates
    """
    merged = []
    # index excel walls by level (there may be one per level; use list if multiple)
    props_by_level = {}
    for w in excel_walls:
        props_by_level.setdefault(w.level, []).append(w)

    for wall_entry in walls_geo:
        # wall_entry is list of quads per level (bottom-up order)
        for quad in wall_entry:
            # convert quad to python floats
            quad_pts = [_to_pyfloat_triplet(p) for p in quad]
            # bottom z is first point's z
            z_bot = quad_pts[0][2]
            level_name = find_level_by_base_elev(story_base_map, z_bot)
            # pick first matching prop for that level (if multiple, you may choose rules)
            props = props_by_level.get(level_name, [])
            prop = props[0] if props else None
            merged.append({
                "level": level_name,
                "prop": prop,
                "geom": quad_pts
            })
    return merged


def merge_slabs(
        slabs_geo: List[List[List[Tuple[float, float, float]]]],
        story_top_map: Dict[float, str],
        excel_slabs: List[Slab],
) -> List[Dict[str, Any]]:
    """
    slabs_geo: list (one entry per plan slab) each entry is a list of polygons per story (each polygon is vertex list)
    Returns list of dicts:
        { "level": level, "prop": Slab(...), "geom": [ (x,y,z), ... ] }
    """
    merged = []
    props_by_level = {s.level: s for s in excel_slabs}

    for slab_entry in slabs_geo:
        # slab_entry: polygons per story (each polygon at top elevation of that story)
        for poly in slab_entry:
            poly_pts = [_to_pyfloat_triplet(p) for p in poly]
            # slab top elevation: poly_pts[0][2]
            top_z = poly_pts[0][2]
            level_name = find_level_by_top_elev(story_top_map, top_z)
            prop = props_by_level.get(level_name)
            merged.append({
                "level": level_name,
                "prop": prop,
                "geom": poly_pts
            })
    return merged


# -----------------------
# Main builder function
# -----------------------
def build_etabs_model_data(
        excel_path: str,
        dxf_path: str,
        column_layer: str = "REC COLS",
        wall_layer: str = "WALL",
        slab_layer: str = "SLAB",
):
    """
    High-level pipeline:
      1. Read Excel (stories + element tables)
      2. Build story mappings (heights, base/top maps)
      3. Read DXF and extrude geometry using heights
      4. Merge geometry with Excel props
    Returns:
      {
         "stories": List[Story],
         "columns": List[ { level, prop(Column|None), geom: ((x,y,z_bot),(x,y,z_top)) } ],
         "walls": List[ { level, prop(Wall|None), geom: [ (x,y,z)... ] } ],
         "slabs": List[ { level, prop(Slab|None), geom: [ (x,y,z)... ] } ],
         "raw_geo": { "columns_geo": ..., "walls_geo": ..., "slabs_geo": ... }
      }
    """
    # --- excel ---
    stories = read_story_table(excel_path)
    excel_columns = read_column_table(excel_path)
    excel_walls = read_wall_table(excel_path)
    excel_beams = read_coupling_beam_table(excel_path)
    excel_slabs = read_slab_table(excel_path)

    if len(stories) == 0:
        raise RuntimeError("No stories found in Excel")

    # --- build mappings ---
    heights_list, base_map, top_map = build_story_mappings(stories)
    # heights_list is bottom-up list of floats, ready to pass to extruder
    # base_map: base_elev -> level, top_map: top_elev -> level

    # --- read dxf and extrude ---
    doc = read_dxf_plan(dxf_path)

    # these functions are expected to accept (doc, layer, story_heights)
    columns_geo = get_columns(doc, column_layer, heights_list)
    walls_geo = get_walls(doc, wall_layer, heights_list)
    slabs_geo = get_slabs(doc, slab_layer, heights_list)

    # --- merge geometry with properties ---
    merged_columns = merge_columns(columns_geo, base_map, excel_columns)
    merged_walls = merge_walls(walls_geo, base_map, excel_walls)
    merged_slabs = merge_slabs(slabs_geo, top_map, excel_slabs)

    result = {
        "stories": stories,
        "heights_list": heights_list,
        "base_map": base_map,
        "top_map": top_map,
        "raw_geo": {
            "columns_geo": columns_geo,
            "walls_geo": walls_geo,
            "slabs_geo": slabs_geo,
        },
        "columns": merged_columns,
        "walls": merged_walls,
        "slabs": merged_slabs,
        "beams_table": excel_beams,
    }
    return result
