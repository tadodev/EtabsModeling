# Example CLI usage
# -----------------------
from connection.etabs_connection import connect_to_etabs
from materials.concrete_material import define_concrete_materials
from modeling.model_stories import define_stories
from sections.beam_rectangle import define_beam_sections
from sections.column_circle import define_circular_sections
from sections.column_rectangular import define_rectangular_sections
from sections.slab_shell import define_slab_sections
from sections.wall_shell import define_wall_sections
from utils.dxf_processing import get_points_by_layer, read_dxf_plan, get_lines_by_layer
from utils.excel_processing import read_story_table, read_concrete_table, read_rectangular_column_table, \
    read_circular_column_table, read_wall_table, read_slab_table, read_coupling_beam_table

if __name__ == "__main__":
    # import pprint
    # excel = r"data/Input Data_V02.xlsx"
    # dxf = r"data/PLan View_V02.dxf"
    #
    # data = build_etabs_model_data(excel, dxf, column_layer="REC COLS", wall_layer="WALL", slab_layer="SLAB")
    #
    # print("Stories (top-down from excel):")
    # pprint.pprint(data["stories"])
    #
    # print("\nHeights (bottom-up):", data["heights_list"])
    # print("\nBase map (elev -> level):")
    # pprint.pprint(data["base_map"])
    #
    # print("\nSample merged column segment (first 6):")
    # for c in data["columns"][:6]:
    #     pprint.pprint(c)
    #
    # print("\nSample merged wall panel (first 6):")
    # for w in data["walls"][:6]:
    #     pprint.pprint(w)
    #
    # print("\nSample merged slab (first 6):")
    # for s in data["slabs"][:6]:
    #     pprint.pprint(s)
    sap_model = connect_to_etabs()
    lb_in_F = 1
    base_elevation = 0.0
    sap_model.SetPresentUnits(lb_in_F)

    # Connected to Excel to read data
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

    sap_model.View.RefreshView()

    # Connected to Dxf to read data
    dxf_path = r"data/PLan View_V02.dxf"
    doc = read_dxf_plan(dxf_path)

    cir_column_locations = get_points_by_layer(doc, "CIR COLS")

    rect_column_locations = get_points_by_layer(doc, "REC COLS")

    wall_x_locations = get_lines_by_layer(doc, " WALL X")
    wall_y_locations = get_lines_by_layer(doc, " WALL Y")

    coupling_beams_y_locations = get_points_by_layer(doc, "CB Y")

    slabs_locations = get_lines_by_layer(doc, "SLAB")
    # assign isotropic mechanical properties to material
