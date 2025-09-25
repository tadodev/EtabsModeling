from typing import List

from models.element_infor import CircColumn

def define_circular_sections(sap_model, columns: List[CircColumn]):
    """
    Defines multiple circular frame sections in the model from a list of CircColumn objects.
    """
    for column in columns:
        try:
            # 1. Define circular geometry
            # Note: Corrected to use the concrete material `column.material`
            ret = sap_model.PropFrame.SetCircle(
                column.name,
                column.material, # This should be the concrete material
                column.dia
            )
            if ret != 0:
                raise Exception(f"Failed to define section geometry (Error code: {ret})")

            print(f"✅ Defined section: {column.name} (Ø {column.dia})")

            # 2. Assign reinforcement
            ret = sap_model.PropFrame.SetRebarColumn(
                column.name,
                column.long_bar_mat,
                column.tie_bar_mat,
                2,                     # Pattern = 2 (Circular)
                1,                     # ConfineType: 1=Ties, 2=Spiral
                column.cover,
                column.num_C_bars,     # Total number of longitudinal bars
                0,                     # Bars along 3-axis (not for circular)
                0,                     # Bars along 2-axis (not for circular)
                column.long_bar_size,
                column.tie_bar_size,
                column.tie_spacing,
                0,                     # Tie legs 2-dir (not for circular)
                0,                     # Tie legs 3-dir (not for circular)
                False                  # ToBeDesigned = False
            )
            if ret != 0:
                raise Exception(f"Failed to assign rebar (Error code: {ret})")

            print(f"   ... Assigned rebar to {column.name}.")

        except Exception as e:
            print(f"❌ ERROR defining circular section '{column.name}': {e}")