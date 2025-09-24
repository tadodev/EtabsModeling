from models.element_infor import CircColumn


def define_circular_section(sap_model, column: CircColumn):
    """
    Define a circular frame section in ETABS from a CircColumn dataclass,
    and assign reinforcement using SetRebarColumn.
    """
    # 1. Define circular geometry
    ret = sap_model.PropFrame.SetCircle(
        column.section_name,   # Section name
        column.long_bar_mat,   # Material (concrete) must exist in ETABS
        column.dia        # Diameter of circular column
    )

    if ret != 0:
        raise Exception(f"ETABS failed to define circular section {column.section_name}. Error code: {ret}")
    else:
        print(f"✅ Defined circular section {column.section_name} (Ø {column.dia}).")

    # 2. Assign reinforcement
    ret = sap_model.PropFrame.SetRebarColumn(
        column.section_name,          # Frame section name
        column.long_bar_mat,          # Longitudinal rebar material
        column.confine_mat,           # Confinement rebar material
        2,                            # Pattern = 2 (Circular)
        1,  # ConfineType: 1=Ties, 2=Spiral
        column.cover,                 # Clear cover
        column.num_bars,         # Total longitudinal bars (for circular)
        0,                            # NumberR3Bars (not used in circular)
        0,                            # NumberR2Bars (not used in circular)
        column.long_bar_size,         # Longitudinal bar size
        column.tie_bar_size,          # Tie/spiral bar size
        column.tie_spacing,           # Spacing of ties/spirals
        0,                            # Tie legs 2-dir (not used in circular)
        0,                            # Tie legs 3-dir (not used in circular)
        False                         # ToBeDesigned = False (Check only)
    )

    if ret != 0:
        raise Exception(f"ETABS failed to assign rebar to {column.section_name}. Error code: {ret}")
    else:
        print(f"✅ Assigned rebar to {column.section_name}: "
              f"{column.num_bars} {column.long_bar_size} with {column.tie_bar_size} "
              f"{'ties'} @ {column.tie_spacing}.")