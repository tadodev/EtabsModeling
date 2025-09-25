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
from utils.build_etabs_data import etabs_model_builder
from utils.dxf_processing import get_points_by_layer, read_dxf_plan, get_lines_by_layer
from utils.excel_processing import read_story_table, read_concrete_table, read_rectangular_column_table, \
    read_circular_column_table, read_wall_table, read_slab_table, read_coupling_beam_table

if __name__ == "__main__":
    etabs_model_builder()

