from models.element_infor import RectColumn


def define_rectangular_section(sap_model, column: RectColumn):
    """
    Define a rectangular frame section in ETABS from a RectColumn dataclass,
    and assign reinforcement using SetRebarColumn.
    """
    # 1. Define rectangle geometry
    ret = sap_model.PropFrame.SetRectangle(
        column.section_name,   # Section name
        column.material,   # Material (concrete) must exist in ETABS
        column.b,              # Depth (local 2-dir)
        column.h               # Width (local 3-dir)
    )

    if ret != 0:
        raise Exception(f"ETABS failed to define rectangular section {column.section_name}. Error code: {ret}")
    else:
        print(f"✅ Defined rectangular section {column.section_name} ({column.b}x{column.h}).")

    # 2. Assign reinforcement
    ret = sap_model.PropFrame.SetRebarColumn(
        column.section_name,          # Frame section name
        column.long_bar_mat,          # Longitudinal rebar material
        column.confine_mat,           # Confinement rebar material
        1,                            # Pattern = 1 (Rectangular)
        1,                            # ConfineType = ties (auto for rectangle)
        column.cover,                 # Clear cover
        0,                            # NumberCBars (only for circular)
        column.bars_3dir,             # Bars along local 3-axis
        column.bars_2dir,             # Bars along local 2-axis
        column.long_bar_size,         # Longitudinal bar size
        column.tie_bar_size,          # Tie bar size
        column.tie_spacing,           # Tie spacing
        column.tie_legs_2dir,         # Tie legs along 2-dir
        column.tie_legs_3dir,         # Tie legs along 3-dir
        False                         # ToBeDesigned = False (Check only)
    )

    if ret != 0:
        raise Exception(f"ETABS failed to assign rebar to {column.section_name}. Error code: {ret}")
    else:
        print(f"✅ Assigned rebar to {column.section_name}: "
              f"{column.bars_2dir}x{column.bars_3dir} {column.long_bar_size} with {column.tie_bar_size} ties.")