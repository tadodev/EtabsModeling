from typing import List, Tuple, Dict
from models.element_infor import Story, RectColumn, CircColumn, Wall, CouplingBeam, Slab
from models.geometry3d import ColumnGeom, WallGeom, SlabGeom, Point3D, BeamGeom


def calculate_story_elevations(stories: List[Story], base_elevation: float = 0.0) -> List[float]:
    """
    Calculate cumulative elevations for each story level.

    Args:
        stories: List of Story objects (ordered from bottom to top)
        base_elevation: Base elevation in feet

    Returns:
        List of elevations for each story level
    """
    elevations = [base_elevation]
    current_elev = base_elevation

    for story in stories:
        current_elev += story.height
        elevations.append(current_elev)

    return elevations


def extrude_points_to_columns(
        dxf_points: List[Tuple[float, float, float]],
        stories: List[Story],
        rect_columns: List[RectColumn],
        circ_columns: List[CircColumn],
        base_elevation: float = 0.0
) -> List[ColumnGeom]:
    """
    Extrude 2D points into 3D column geometry with proper section assignments.

    Args:
        dxf_points: List of (x, y, z) points from DXF
        stories: List of Story objects (bottom to top)
        rect_columns: Rectangular column properties by level
        circ_columns: Circular column properties by level
        base_elevation: Base elevation

    Returns:
        List of ColumnGeom objects
    """
    elevations = calculate_story_elevations(stories, base_elevation)

    # Create lookup dictionaries for column properties by level
    rect_props = {col.level: col for col in rect_columns}
    circ_props = {col.level: col for col in circ_columns}

    column_geometries = []

    for point_idx, (x, y, _) in enumerate(dxf_points):
        for story_idx, story in enumerate(stories):
            z_bottom = elevations[story_idx] * 12  # Convert to inches
            z_top = elevations[story_idx + 1] * 12  # Convert to inches

            # Determine section name based on available column data
            prop_name = "Default"
            if story.level in rect_props:
                prop_name = rect_props[story.level].name
            elif story.level in circ_props:
                prop_name = circ_props[story.level].name

            column_geom = ColumnGeom(
                start_point=(x, y, z_bottom),  # Convert to inches with z only
                end_point=(x, y, z_top),
                prop_name=prop_name,
                # name=f"C{point_idx + 1}_{story.level}"
            )
            column_geometries.append(column_geom)

    return column_geometries


def extrude_lines_to_walls(
        dxf_lines: List[Tuple[Tuple[float, float, float], Tuple[float, float, float]]],
        stories: List[Story],
        walls: List[Wall],
        base_elevation: float = 0.0
) -> List[WallGeom]:
    """
    Extrude 2D lines into 3D wall geometry with proper section assignments.

    Args:
        dxf_lines: List of line segments from DXF
        stories: List of Story objects (bottom to top)
        walls: Wall properties by level
        base_elevation: Base elevation

    Returns:
        List of WallGeom objects
    """
    elevations = calculate_story_elevations(stories, base_elevation)

    # Create lookup dictionary for wall properties by level
    wall_props = {wall.level: wall for wall in walls}

    wall_geometries = []

    for line_idx, ((x1, y1, _), (x2, y2, _)) in enumerate(dxf_lines):
        for story_idx, story in enumerate(stories):
            z_bottom = elevations[story_idx] * 12  # Convert to inches
            z_top = elevations[story_idx + 1] * 12  # Convert to inches

            # Get wall section name
            prop_name = "Default"
            if story.level in wall_props:
                prop_name = wall_props[story.level].name

            # Create 4-point wall geometry (rectangular wall panel)
            x_coords = [x1, x2, x2, x1]  # Convert to inches
            y_coords = [y1, y2, y2, y1]
            z_coords = [z_bottom, z_bottom, z_top, z_top]

            wall_geom = WallGeom(
                num_points=4,
                x_coord=x_coords,
                y_coord=y_coords,
                z_coord=z_coords,
                prop_name=prop_name,
                # name=f"W{line_idx + 1}_{story.level}"
            )
            wall_geometries.append(wall_geom)

    return wall_geometries


def extrude_polylines_to_slabs(
        dxf_polylines: List[List[Tuple[float, float, float]]],
        stories: List[Story],
        slabs: List[Slab],
        base_elevation: float = 0.0
) -> List[SlabGeom]:
    """
    Extrude 2D polylines into 3D slab geometry with proper section assignments.

    Args:
        dxf_polylines: List of polyline point lists from DXF
        stories: List of Story objects (bottom to top)
        slabs: Slab properties by level
        base_elevation: Base elevation

    Returns:
        List of SlabGeom objects
    """
    elevations = calculate_story_elevations(stories, base_elevation)

    # Create lookup dictionary for slab properties by level
    slab_props = {slab.level: slab for slab in slabs}

    slab_geometries = []

    for poly_idx, polyline in enumerate(dxf_polylines):
        for story_idx, story in enumerate(stories):
            z_level = elevations[story_idx + 1] * 12  # Slab at top of story, convert to inches
            # Get slab section name and loads
            level_slab = slab_props.get(story.level)
            prop_name = level_slab.name if level_slab else "Default"
            sdl = level_slab.sdl if level_slab else 0.0
            live = level_slab.live if level_slab else 0.0

            # Extract coordinates and convert to inches
            x_coords = [pt[0] for pt in polyline]
            y_coords = [pt[1] for pt in polyline]
            z_coords = [z_level] * len(polyline)

            slab_geom = SlabGeom(
                num_points=len(polyline),
                x_coord=x_coords,
                y_coord=y_coords,
                z_coord=z_coords,
                prop_name=prop_name,
                name=f"S{poly_idx + 1}_{story.level}",
                sdl=sdl,
                live=live
            )
            slab_geometries.append(slab_geom)

    return slab_geometries


def extrude_lines_to_beams(
        dxf_lines: List[Tuple[Tuple[float, float, float], Tuple[float, float, float]]],
        stories: List[Story],
        coupling_beams: List[CouplingBeam],
        base_elevation: float = 0.0
) -> List[BeamGeom]:
    """
    Extrude 2D line segments into 3D coupling beam geometry.

    This is used when your DXF already defines the beam start/end points as lines
    rather than center points that need to be extended.

    Args:
        dxf_lines: List of line segments from DXF
        stories: List of Story objects (bottom to top)
        coupling_beams: Coupling beam properties by level
        base_elevation: Base elevation in feet

    Returns:
        List of BeamGeom objects
    """
    # Calculate story elevations
    elevations = calculate_story_elevations(stories, base_elevation)

    # Create lookup dictionary for beam properties by level
    beam_props = {beam.level: beam for beam in coupling_beams}

    beam_geometries = []

    for line_idx, ((x1, y1, _), (x2, y2, _)) in enumerate(dxf_lines):
        for story_idx, story in enumerate(stories):
            # Beams are placed at the floor level (top of each story)
            z_level = elevations[story_idx + 1] * 12  # Convert to inches

            # Create beam geometry using line endpoints
            start_point = (x1, y1, z_level)
            end_point = (x2, y2, z_level)

            # Get beam section name for this level
            prop_name = "Default"
            if story.level in beam_props:
                # For lines, we might need logic to determine X vs Y beam
                # Based on line orientation or use a default
                prop_name = beam_props[story.level].name

            beam_geom = BeamGeom(
                start_point=start_point,
                end_point=end_point,
                prop_name=prop_name,
                # name=f"CB{line_idx + 1}_L_{story.level}"
            )
            beam_geometries.append(beam_geom)

    return beam_geometries
