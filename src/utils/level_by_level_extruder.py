"""
Level-by-level extrusion module.

This module processes each story individually using its own DXF file.
Each level is extruded from its floor elevation to the floor above.
"""

from typing import List, Dict
from models.element_infor import Story, RectColumn, CircColumn, Wall, CouplingBeam, Slab
from models.geometry3d import ColumnGeom, WallGeom, SlabGeom, BeamGeom
from utils.dxf_processing import read_dxf_plan, get_points_by_layer, get_lines_by_layer, get_polylines_by_layer
import os


def calculate_story_elevations(stories: List[Story], base_elevation: float = 0.0) -> Dict[str, float]:
    """
    Calculate elevation for each story level.

    Args:
        stories: List of Story objects (ordered from bottom to top)
        base_elevation: Base elevation in meters

    Returns:
        Dictionary mapping level name to bottom elevation (in meters)
    """
    elevations = {}
    current_elev = base_elevation

    for story in stories:
        elevations[story.level] = current_elev
        current_elev += story.height

    return elevations


def extrude_level_columns(
        story: Story,
        z_bottom: float,
        z_top: float,
        rect_columns: List[RectColumn],
        circ_columns: List[CircColumn],
        layer_rect: str = "REC COLS",
        layer_circ: str = "CIR COLS"
) -> List[ColumnGeom]:
    """
    Extrude columns for a single level from its DXF file.

    Args:
        story: Story object containing DXF path
        z_bottom: Bottom elevation in mm
        z_top: Top elevation in mm
        rect_columns: List of rectangular column properties
        circ_columns: List of circular column properties
        layer_rect: DXF layer name for rectangular columns
        layer_circ: DXF layer name for circular columns

    Returns:
        List of ColumnGeom objects
    """
    if not story.dxf_path or not os.path.exists(story.dxf_path):
        print(f"⚠️ Warning: DXF file not found for level {story.level}: {story.dxf_path}")
        return []

    doc = read_dxf_plan(story.dxf_path)

    # Create lookup dictionaries
    rect_props = {col.level: col for col in rect_columns if col.level == story.level}
    circ_props = {col.level: col for col in circ_columns if col.level == story.level}

    column_geometries = []

    # Process rectangular columns
    rect_points = get_points_by_layer(doc, layer_rect)
    for x, y, _ in rect_points:
        prop_name = rect_props.get(story.level, None)
        if prop_name:
            column_geom = ColumnGeom(
                start_point=(x, y, z_bottom),
                end_point=(x, y, z_top),
                prop_name=prop_name.name
            )
            column_geometries.append(column_geom)

    # Process circular columns
    circ_points = get_points_by_layer(doc, layer_circ)
    for x, y, _ in circ_points:
        prop_name = circ_props.get(story.level, None)
        if prop_name:
            column_geom = ColumnGeom(
                start_point=(x, y, z_bottom),
                end_point=(x, y, z_top),
                prop_name=prop_name.name
            )
            column_geometries.append(column_geom)

    print(f"  ✓ Created {len(column_geometries)} columns for {story.level}")
    return column_geometries


def extrude_level_walls(
        story: Story,
        z_bottom: float,
        z_top: float,
        walls: List[Wall],
        layer_x: str = "WALL X",
        layer_y: str = "WALL"
) -> List[WallGeom]:
    """
    Extrude walls for a single level from its DXF file.

    Args:
        story: Story object containing DXF path
        z_bottom: Bottom elevation in mm
        z_top: Top elevation in mm
        walls: List of wall properties
        layer_x: DXF layer name for X-direction walls
        layer_y: DXF layer name for Y-direction walls

    Returns:
        List of WallGeom objects
    """
    if not story.dxf_path or not os.path.exists(story.dxf_path):
        print(f"⚠️ Warning: DXF file not found for level {story.level}: {story.dxf_path}")
        return []

    doc = read_dxf_plan(story.dxf_path)

    # Create lookup dictionary
    wall_props = {wall.level: wall for wall in walls if wall.level == story.level}

    wall_geometries = []

    # Process X-direction walls
    wall_x_lines = get_lines_by_layer(doc, layer_x)
    for (x1, y1, _), (x2, y2, _) in wall_x_lines:
        # Find matching wall property (you may need better logic here)
        matching_wall = None
        for wall in wall_props.values():
            if "X" in wall.name.upper():
                matching_wall = wall
                break

        if matching_wall:
            wall_geom = WallGeom(
                num_points=4,
                x_coord=[x1, x2, x2, x1],
                y_coord=[y1, y2, y2, y1],
                z_coord=[z_bottom, z_bottom, z_top, z_top],
                prop_name=matching_wall.name
            )
            wall_geometries.append(wall_geom)

    # Process Y-direction walls
    wall_y_lines = get_lines_by_layer(doc, layer_y)
    for (x1, y1, _), (x2, y2, _) in wall_y_lines:
        # Find matching wall property
        matching_wall = None
        for wall in wall_props.values():
            if "Y" in wall.name.upper():
                matching_wall = wall
                break

        if matching_wall:
            wall_geom = WallGeom(
                num_points=4,
                x_coord=[x1, x2, x2, x1],
                y_coord=[y1, y2, y2, y1],
                z_coord=[z_bottom, z_bottom, z_top, z_top],
                prop_name=matching_wall.name
            )
            wall_geometries.append(wall_geom)

    print(f"  ✓ Created {len(wall_geometries)} walls for {story.level}")
    return wall_geometries


def extrude_level_beams(
        story: Story,
        z_level: float,
        beams: List[CouplingBeam],
        layer_x: str = "CB X",
        layer_y: str = "CB Y"
) -> List[BeamGeom]:
    """
    Extrude beams for a single level from its DXF file.
    Beams are placed at the top of the story (floor level).

    Args:
        story: Story object containing DXF path
        z_level: Floor elevation in mm
        beams: List of beam properties
        layer_x: DXF layer name for X-direction beams
        layer_y: DXF layer name for Y-direction beams

    Returns:
        List of BeamGeom objects
    """
    if not story.dxf_path or not os.path.exists(story.dxf_path):
        print(f"⚠️ Warning: DXF file not found for level {story.level}: {story.dxf_path}")
        return []

    doc = read_dxf_plan(story.dxf_path)

    # Create lookup dictionary
    beam_props = {beam.level: beam for beam in beams if beam.level == story.level}

    beam_geometries = []

    # Process X-direction beams
    beam_x_lines = get_lines_by_layer(doc, layer_x)
    for (x1, y1, _), (x2, y2, _) in beam_x_lines:
        matching_beam = None
        for beam in beam_props.values():
            if "X" in beam.name.upper():
                matching_beam = beam
                break

        if matching_beam:
            beam_geom = BeamGeom(
                start_point=(x1, y1, z_level),
                end_point=(x2, y2, z_level),
                prop_name=matching_beam.name
            )
            beam_geometries.append(beam_geom)

    # Process Y-direction beams
    beam_y_lines = get_lines_by_layer(doc, layer_y)
    for (x1, y1, _), (x2, y2, _) in beam_y_lines:
        matching_beam = None
        for beam in beam_props.values():
            if "Y" in beam.name.upper():
                matching_beam = beam
                break

        if matching_beam:
            beam_geom = BeamGeom(
                start_point=(x1, y1, z_level),
                end_point=(x2, y2, z_level),
                prop_name=matching_beam.name
            )
            beam_geometries.append(beam_geom)

    print(f"  ✓ Created {len(beam_geometries)} beams for {story.level}")
    return beam_geometries


def extrude_level_slabs(
        story: Story,
        z_level: float,
        slabs: List[Slab],
        layer: str = "SLAB"
) -> List[SlabGeom]:
    """
    Extrude slabs for a single level from its DXF file.
    Slabs are placed at the top of the story (floor level).

    Args:
        story: Story object containing DXF path
        z_level: Floor elevation in mm
        slabs: List of slab properties
        layer: DXF layer name for slabs

    Returns:
        List of SlabGeom objects
    """
    if not story.dxf_path or not os.path.exists(story.dxf_path):
        print(f"⚠️ Warning: DXF file not found for level {story.level}: {story.dxf_path}")
        return []

    doc = read_dxf_plan(story.dxf_path)

    # Get slab properties for this level
    level_slab = None
    for slab in slabs:
        if slab.level == story.level:
            level_slab = slab
            break

    if not level_slab:
        print(f"⚠️ Warning: No slab properties found for level {story.level}")
        return []

    slab_geometries = []

    # Process slab polylines
    slab_polylines = get_polylines_by_layer(doc, layer)
    for poly_idx, polyline in enumerate(slab_polylines):
        x_coords = [pt[0] for pt in polyline]
        y_coords = [pt[1] for pt in polyline]
        z_coords = [z_level] * len(polyline)

        slab_geom = SlabGeom(
            num_points=len(polyline),
            x_coord=x_coords,
            y_coord=y_coords,
            z_coord=z_coords,
            prop_name=level_slab.name,
            name=f"S{poly_idx + 1}_{story.level}",
            sdl=level_slab.sdl,
            live=level_slab.live
        )
        slab_geometries.append(slab_geom)

    print(f"  ✓ Created {len(slab_geometries)} slabs for {story.level}")
    return slab_geometries


def process_all_levels(
        stories: List[Story],
        base_elevation: float,
        rect_columns: List[RectColumn],
        circ_columns: List[CircColumn],
        walls: List[Wall],
        beams: List[CouplingBeam],
        slabs: List[Slab]
) -> tuple:
    """
    Process all stories level-by-level, creating geometry from individual DXF files.

    This function processes from bottom to top, extruding each level by its story height.

    Args:
        stories: List of Story objects (ordered bottom to top)
        base_elevation: Base elevation in meters
        rect_columns: All rectangular column properties
        circ_columns: All circular column properties
        walls: All wall properties
        beams: All beam properties
        slabs: All slab properties

    Returns:
        Tuple of (all_columns, all_walls, all_beams, all_slabs)
    """
    print("\n" + "=" * 60)
    print("PROCESSING LEVELS FROM BOTTOM TO TOP")
    print("=" * 60)

    # Calculate elevations for all stories
    elevations = calculate_story_elevations(stories, base_elevation)

    all_columns = []
    all_walls = []
    all_beams = []
    all_slabs = []

    # Process each story from bottom to top
    for idx, story in enumerate(stories):
        print(f"\n📐 Processing {story.level} (Story {idx + 1}/{len(stories)})")
        print(f"   DXF: {story.dxf_path}")

        z_bottom = elevations[story.level] * 1000  # Convert m to mm
        z_top = (elevations[story.level] + story.height) * 1000  # Convert m to mm
        z_floor = z_top  # Slabs and beams at top of story

        print(f"   Elevation: {elevations[story.level]:.2f}m to {elevations[story.level] + story.height:.2f}m")

        # Process columns (from bottom to top of this story)
        level_columns = extrude_level_columns(
            story, z_bottom, z_top, rect_columns, circ_columns
        )
        all_columns.extend(level_columns)

        # Process walls (from bottom to top of this story)
        level_walls = extrude_level_walls(
            story, z_bottom, z_top, walls
        )
        all_walls.extend(level_walls)

        # Process beams (at top of this story)
        level_beams = extrude_level_beams(
            story, z_floor, beams
        )
        all_beams.extend(level_beams)

        # Process slabs (at top of this story)
        level_slabs = extrude_level_slabs(
            story, z_floor, slabs
        )
        all_slabs.extend(level_slabs)

    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total Columns: {len(all_columns)}")
    print(f"Total Walls: {len(all_walls)}")
    print(f"Total Beams: {len(all_beams)}")
    print(f"Total Slabs: {len(all_slabs)}")

    return all_columns, all_walls, all_beams, all_slabs