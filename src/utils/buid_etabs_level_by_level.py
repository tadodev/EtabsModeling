"""
ETABS Model Builder - Level-by-Level Approach

This workflow processes each story individually using its own DXF file.
Each level's DXF path is specified in the Excel Story table.
"""

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
from utils.excel_processing import (read_story_table, read_concrete_table,
                                    read_rectangular_column_table,
                                    read_circular_column_table, read_wall_table,
                                    read_coupling_beam_table, read_slab_table)
from utils.level_by_level_extruder import process_all_levels


def etabs_model_builder_level_by_level():
    """
    Complete workflow for building ETABS model using level-by-level approach.

    Each story has its own DXF file specified in the Excel Story sheet.
    The model is built from bottom to top, extruding each level by its story height.
    """
    print("=" * 70)
    print(" ETABS MODEL BUILDER - LEVEL BY LEVEL APPROACH")
    print("=" * 70)

    # ============================================
    # STEP 1: Connect to ETABS
    # ============================================
    print("\n🔌 Connecting to ETABS...")
    sap_model = connect_to_etabs()
    sap_model.SetPresentUnits(9)  # N_mm_C units
    base_elevation = -18  # Base elevation in meters
    print("✅ Connected to ETABS")

    # ============================================
    # STEP 2: Read Excel Data
    # ============================================
    print("\n📊 Reading Excel data...")
    excel_path = r"C:\Work\Code\EtabsModeling\src\data\Input Data_V02_metric.xlsx"

    stories = read_story_table(excel_path)
    concretes = read_concrete_table(excel_path)
    rect_columns = read_rectangular_column_table(excel_path)
    cir_columns = read_circular_column_table(excel_path)
    walls = read_wall_table(excel_path)
    coupling_beams = read_coupling_beam_table(excel_path)
    slabs = read_slab_table(excel_path)

    print(f"✅ Read data for {len(stories)} stories")

    # ============================================
    # STEP 3: Define Stories and Properties
    # ============================================
    print("\n🏗️ Defining stories and material properties in ETABS...")
    define_stories(sap_model, stories, base_elevation)
    define_concrete_materials(sap_model, concretes)
    define_rectangular_sections(sap_model, rect_columns)
    define_circular_sections(sap_model, cir_columns)
    define_wall_sections(sap_model, walls)
    define_beam_sections(sap_model, coupling_beams)
    define_slab_sections(sap_model, slabs)
    print("✅ Stories and properties defined")

    # ============================================
    # STEP 4: Process DXF Files Level-by-Level
    # ============================================
    print("\n📐 Processing DXF files for each level...")

    all_columns, all_walls, all_beams, all_slabs = process_all_levels(
        stories=stories,
        base_elevation=base_elevation,
        rect_columns=rect_columns,
        circ_columns=cir_columns,
        walls=walls,
        beams=coupling_beams,
        slabs=slabs
    )

    # ============================================
    # STEP 5: Create Elements in ETABS
    # ============================================
    print("\n🔨 Creating elements in ETABS...")

    if all_columns:
        create_columns_in_etabs(sap_model, all_columns)
    else:
        print("⚠️ No columns to create")

    if all_walls:
        create_walls_in_etabs(sap_model, all_walls)
    else:
        print("⚠️ No walls to create")

    if all_beams:
        create_beams_in_etabs(sap_model, all_beams)
    else:
        print("⚠️ No beams to create")

    if all_slabs:
        create_slabs_in_etabs(sap_model, all_slabs, "Dead", "Live")
    else:
        print("⚠️ No slabs to create")

    # ============================================
    # STEP 6: Finalize
    # ============================================
    print("\n🎨 Refreshing view...")
    sap_model.View.RefreshView()

    print("\n" + "=" * 70)
    print("✅ COMPLETE! ETABS model created successfully!")
    print("=" * 70)
    print(f"   📍 Base Elevation: {base_elevation} m")
    print(f"   📊 Total Stories: {len(stories)}")
    print(f"   🏛️ Total Columns: {len(all_columns)}")
    print(f"   🧱 Total Walls: {len(all_walls)}")
    print(f"   🌉 Total Beams: {len(all_beams)}")
    print(f"   🏢 Total Slabs: {len(all_slabs)}")
    print("=" * 70)


