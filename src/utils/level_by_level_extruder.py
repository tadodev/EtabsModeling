"""
Level-by-level extrusion module with unit system support.

This module processes each story individually using its own DXF file.
Each level is extruded from its floor elevation to the floor above.
Supports both US (lb-in-F) and Metric (N-mm-C) unit systems.
"""

from typing import List, Dict
from models.element_infor import Story, RectColumn, CircColumn, Wall, CouplingBeam, Slab
from models.geometry3d import ColumnGeom, WallGeom, SlabGeom, BeamGeom
from utils.dxf_processing import read_dxf_plan, get_points_by_layer, get_lines_by_layer, get_polylines_by_layer
from utils.unit_config import UnitConfig, convert_story_height
import os


def calculate_story_elevations(stories: List[Story], base_elevation: float,
                               unit_config: UnitConfig) -> Dict[str, float]:
    """
    Calculate elevation for each story level in story input units.

    Args:
        stories: List of Story objects (ordered from bottom to top)
        base_elevation: Base elevation in story input units (ft or m)
        unit_config: Unit configuration

    Returns:
        Dictionary mapping level name to bottom elevation (in story input units)
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
        unit_config: UnitConfig,
        layer_rect: str = "REC COLS",
        layer_circ: str = "CIR COLS"
) -> List[ColumnGeom]:
    """
    Extrude columns for a single level from its DXF file.

    Args:
        story: Story object containing DXF path
        z_bottom: Bottom elevation in model units (in or mm)
        z_top: Top elevation in model units (in or mm)
        rect_columns: List of rectangular column properties
        circ_columns: List of circular column properties
        unit_config: Unit configuration
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
            # Convert DXF coordinates (in story input units) to model units
            x_model = x * unit_config.length_to_model
            y_model = y * unit_config.length_to_model

            column_geom = ColumnGeom(
                start_point=(x_model, y_model, z_bottom),
                end_point=(x_model, y_model, z_top),
                prop_name=prop_name.name
            )
            column_geometries.append(column_geom)

    # Process circular columns
    circ_points = get_points_by_layer(doc, layer_circ)
    for x, y, _ in circ_points:
        prop_name = circ_props.get(story.level, None)
        if prop_name:
            x_model = x * unit_config.length_to_model
            y_model = y * unit_config.length_to_model

            column_geom = ColumnGeom(
                start_point=(x_model, y_model, z_bottom),
                end_point=(x_model, y_model, z_top),
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
        unit_config: UnitConfig,
        layer_x: str = "WALL",
        layer_y: str = "WALL Y"
) -> List[WallGeom]:
    """
    Extrude walls for a single level from its DXF file.

    Args:
        story: Story object containing DXF path
        z_bottom: Bottom elevation in model units (in or mm)
        z_top: Top elevation in model units (in or mm)
        walls: List of wall properties
        unit_config: Unit configuration
        layer_x: DXF layer name for X-direction walls
        layer_y: DXF layer name for Y-direction walls

    Returns:
        List of WallGeom objects
    """
    if not story.dxf_path or not os.path.exists(story.dxf_path):
        print(f"⚠️ Warning: DXF file not found for level {story.level}: {story.dxf_path}")
        return []

    doc = read_dxf_plan(story.dxf_path)

    # Filter wall properties for this story only
    wall_props = [w for w in walls if w.level == story.level]
    if not wall_props:
        print(f"⚠️ No wall properties found for level {story.level}")
        return []

    wall_geometries = []

    # Process X-direction walls
    wall_x_lines = get_lines_by_layer(doc, layer_x)
    for (x1, y1, _), (x2, y2, _) in wall_x_lines:
        for w in wall_props:
            if w.name:
                # Convert coordinates to model units
                x1_model = x1 * unit_config.length_to_model
                x2_model = x2 * unit_config.length_to_model
                y1_model = y1 * unit_config.length_to_model
                y2_model = y2 * unit_config.length_to_model

                wall_geom = WallGeom(
                    num_points=4,
                    x_coord=[x1_model, x2_model, x2_model, x1_model],
                    y_coord=[y1_model, y2_model, y2_model, y1_model],
                    z_coord=[z_bottom, z_bottom, z_top, z_top],
                    prop_name=w.name
                )
                wall_geometries.append(wall_geom)
                break

    # Process Y-direction walls
    wall_y_lines = get_lines_by_layer(doc, layer_y)
    for (x1, y1, _), (x2, y2, _) in wall_y_lines:
        for w in wall_props:
            if w.name:
                x1_model = x1 * unit_config.length_to_model
                x2_model = x2 * unit_config.length_to_model
                y1_model = y1 * unit_config.length_to_model
                y2_model = y2 * unit_config.length_to_model

                wall_geom = WallGeom(
                    num_points=4,
                    x_coord=[x1_model, x2_model, x2_model, x1_model],
                    y_coord=[y1_model, y2_model, y2_model, y1_model],
                    z_coord=[z_bottom, z_bottom, z_top, z_top],
                    prop_name=w.name
                )
                wall_geometries.append(wall_geom)
                break

    print(f"  ✓ Created {len(wall_geometries)} walls for {story.level}")
    return wall_geometries


def extrude_level_beams(
        story: Story,
        z_level: float,
        beams: List[CouplingBeam],
        unit_config: UnitConfig,
        layer_x: str = "CB X",
        layer_y: str = "CB Y"
) -> List[BeamGeom]:
    """
    Extrude beams for a single level from its DXF file.
    Beams are placed at the top of the story (floor level).

    Args:
        story: Story object containing DXF path
        z_level: Floor elevation in model units (in or mm)
        beams: List of beam properties
        unit_config: Unit configuration
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
            x1_model = x1 * unit_config.length_to_model
            x2_model = x2 * unit_config.length_to_model
            y1_model = y1 * unit_config.length_to_model
            y2_model = y2 * unit_config.length_to_model

            beam_geom = BeamGeom(
                start_point=(x1_model, y1_model, z_level),
                end_point=(x2_model, y2_model, z_level),
                prop_name=matching_beam.name
            )
            beam_geometries.append(beam_geom)

    print(f"  ✓ Created {len(beam_geometries)} beams for {story.level}")
    return beam_geometries


def extrude_level_slabs(
        story: Story,
        z_level: float,
        slabs: List[Slab],
        unit_config: UnitConfig,
        layer: str = "SLAB"
) -> List[SlabGeom]:
    """
    Extrude slabs for a single level from its DXF file.
    Slabs are placed at the top of the story (floor level).

    Args:
        story: Story object containing DXF path
        z_level: Floor elevation in model units (in or mm)
        slabs: List of slab properties
        unit_config: Unit configuration
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
        # Convert coordinates to model units
        x_coords = [pt[0] * unit_config.length_to_model for pt in polyline]
        y_coords = [pt[1] * unit_config.length_to_model for pt in polyline]
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
        slabs: List[Slab],
        unit_config: UnitConfig
) -> tuple:
    """
    Process all stories level-by-level, creating geometry from individual DXF files.

    This function processes from bottom to top, extruding each level by its story height.

    Args:
        stories: List of Story objects (ordered bottom to top)
        base_elevation: Base elevation in story input units (ft or m)
        rect_columns: All rectangular column properties
        circ_columns: All circular column properties
        walls: All wall properties
        beams: All beam properties
        slabs: All slab properties
        unit_config: Unit configuration

    Returns:
        Tuple of (all_columns, all_walls, all_beams, all_slabs)
    """
    print("\n" + "=" * 60)
    print("PROCESSING LEVELS FROM BOTTOM TO TOP")
    print("=" * 60)

    # Calculate elevations for all stories (in story input units)
    elevations = calculate_story_elevations(stories, base_elevation, unit_config)

    all_columns = []
    all_walls = []
    all_beams = []
    all_slabs = []

    # Process each story from bottom to top
    for idx, story in enumerate(stories):
        print(f"\n📐 Processing {story.level} (Story {idx + 1}/{len(stories)})")
        print(f"   DXF: {story.dxf_path}")

        # Convert elevations from story input units to model units
        z_bottom = convert_story_height(elevations[story.level], unit_config)
        z_top = convert_story_height(elevations[story.level] + story.height, unit_config)
        z_floor = z_top  # Slabs and beams at top of story

        print(
            f"   Elevation: {elevations[story.level]:.2f}{unit_config.story_input_unit} to {elevations[story.level] + story.height:.2f}{unit_config.story_input_unit}")
        print(f"   Model Units: {z_bottom:.2f}{unit_config.length_unit} to {z_top:.2f}{unit_config.length_unit}")

        # Process columns (from bottom to top of this story)
        level_columns = extrude_level_columns(
            story, z_bottom, z_top, rect_columns, circ_columns, unit_config
        )
        all_columns.extend(level_columns)

        # Process walls (from bottom to top of this story)
        level_walls = extrude_level_walls(
            story, z_bottom, z_top, walls, unit_config
        )
        all_walls.extend(level_walls)

        # Process beams (at top of this story)
        level_beams = extrude_level_beams(
            story, z_floor, beams, unit_config
        )
        all_beams.extend(level_beams)

        # Process slabs (at top of this story)
        level_slabs = extrude_level_slabs(
            story, z_floor, slabs, unit_config
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
