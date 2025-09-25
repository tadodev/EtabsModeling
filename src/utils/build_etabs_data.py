from connection.etabs_connection import connect_to_etabs
from materials.concrete_material import define_concrete_materials
from modeling.model_beams import create_beams_in_etabs
from modeling.model_columns import create_columns_in_etabs
from modeling.model_slabs import create_slabs_in_etabs
from modeling.model_stories import define_stories
from modeling.model_walls import create_walls_in_etabs
from sections.beam_rectangle import define_beam_sections
from sections.column_circle import define_circular_sections
from sections.column_rectangular import define_rectangular_sections
from sections.slab_shell import define_slab_sections
from sections.wall_shell import define_wall_sections
from utils.dxf_processing import read_dxf_plan, get_points_by_layer, get_lines_by_layer, get_polylines_by_layer
from utils.excel_processing import read_story_table, read_concrete_table, read_rectangular_column_table, \
    read_circular_column_table, read_wall_table, read_coupling_beam_table, read_slab_table
from utils.extruder import extrude_points_to_columns, extrude_lines_to_walls, extrude_polylines_to_slabs, \
    extrude_lines_to_beams


def etabs_model_builder():
    """
    Complete workflow example showing how to use all the functions together.
    """
    # Connect to ETABS
    sap_model = connect_to_etabs()
    sap_model.SetPresentUnits(1)  # lb_in_F units
    base_elevation = -5.0  # Base elevation in feet

    # Read data from Excel
    excel_path = r"data/Input Data_V02.xlsx"
    stories = read_story_table(excel_path)
    concretes = read_concrete_table(excel_path)
    rect_columns = read_rectangular_column_table(excel_path)
    cir_columns = read_circular_column_table(excel_path)
    walls = read_wall_table(excel_path)
    coupling_beams = read_coupling_beam_table(excel_path)
    slabs = read_slab_table(excel_path)

    # Define properties in ETABS
    define_stories(sap_model, stories, base_elevation)
    define_concrete_materials(sap_model, concretes)
    define_rectangular_sections(sap_model, rect_columns)
    define_circular_sections(sap_model, cir_columns)
    define_wall_sections(sap_model, walls)
    define_beam_sections(sap_model, coupling_beams)
    define_slab_sections(sap_model, slabs)

    # Read geometry from DXF
    dxf_path = r"data/PLan View_V02.dxf"
    doc = read_dxf_plan(dxf_path)

    # Get 2D geometry data
    cir_column_locations = get_points_by_layer(doc, "CIR COLS")
    rect_column_locations = get_points_by_layer(doc, "REC COLS")
    coupling_beam_y_location = get_lines_by_layer(doc, "CB Y")
    wall_x_locations = get_lines_by_layer(doc, "WALL X")
    wall_y_locations = get_lines_by_layer(doc, "WALL Y")
    slab_polylines = get_polylines_by_layer(doc, "SLAB")  # Assuming these are polylines

    # Extrude geometry to 3D with section assignments
    rect_column_geoms = extrude_points_to_columns(
        rect_column_locations, stories, rect_columns, [], base_elevation
    )

    circ_column_geoms = extrude_points_to_columns(
        cir_column_locations, stories, [], cir_columns, base_elevation
    )

    wall_x_geoms = extrude_lines_to_walls(
        wall_x_locations, stories, walls, base_elevation
    )

    wall_y_geoms = extrude_lines_to_walls(
        wall_y_locations, stories, walls, base_elevation
    )

    coupling_beam_geoms = extrude_lines_to_beams(
        coupling_beam_y_location, stories, coupling_beams, base_elevation
    )

    # For slabs, you'd need polylines from DXF instead of lines
    slab_geoms = extrude_polylines_to_slabs(
         slab_polylines, stories, slabs, base_elevation)

    # Create elements in ETABS
    create_columns_in_etabs(sap_model, rect_column_geoms + circ_column_geoms)
    create_walls_in_etabs(sap_model, wall_x_geoms + wall_y_geoms)
    create_beams_in_etabs(sap_model, coupling_beam_geoms)
    create_slabs_in_etabs(sap_model, slab_geoms)

    # Refresh the view
    sap_model.View.RefreshView()
    print("✅ Complete ETABS model created successfully!")