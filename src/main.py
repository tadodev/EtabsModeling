# Example CLI usage
# -----------------------
from connection.etabs_connection import connect_to_etabs
from materials.concrete_material import define_concrete_materials
from modeling.model_beams import define_beam_sections
from modeling.model_stories import define_stories
from models.element_infor import RectColumn, Concrete, CircColumn, Story
from sections.column_circle import define_circular_sections
from sections.column_rectangular import define_rectangular_sections
from sections.slab_shell import define_slab_sections
from sections.wall_shell import define_wall_sections
from utils.build_etabs_data import build_etabs_model_data
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
    sap_model.SetPresentUnits(lb_in_F)

    # Connected to Excel to read data
    path = r"data/Input Data_V02.xlsx"

    stories = read_story_table(path)

    concretes = read_concrete_table(path)

    rect_columns = read_rectangular_column_table(path)

    cir_columns = read_circular_column_table(path)

    walls = read_wall_table(path)

    coupling_beams = read_coupling_beam_table(path)

    slabs = read_slab_table(path)

    # Define properties in ETABS
    define_stories(sap_model, stories, -5.0)

    define_concrete_materials(sap_model, concretes)

    define_rectangular_sections(sap_model, rect_columns)
    define_circular_sections(sap_model, cir_columns)
    define_wall_sections(sap_model, walls)
    define_beam_sections(sap_model, coupling_beams)
    define_slab_sections(sap_model, slabs)

    sap_model.View.RefreshView()
    # assign isotropic mechanical properties to material
