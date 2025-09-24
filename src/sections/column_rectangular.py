from typing import List

from models.element_infor import RectColumn


# Make sure RectColumn dataclass is imported
# from models.element_infor import RectColumn

def define_rectangular_sections(sap_model, columns: List[RectColumn]):
    """
    Defines multiple rectangular frame sections in the model from a list of RectColumn objects.
    """
    for column in columns:
        try:
            # 1. Define rectangle geometry
            ret = sap_model.PropFrame.SetRectangle(
                column.name,  # Section name
                column.material,  # Concrete material name
                column.b,  # Depth
                column.h  # Width
            )
            if ret != 0:
                raise Exception(f"Failed to define section geometry (Error code: {ret})")

            print(f"✅ Defined section: {column.name} ({column.b}x{column.h})")

            # 2. Assign reinforcement
            ret = sap_model.PropFrame.SetRebarColumn(
                column.name,
                column.long_bar_mat,
                column.tie_bar_mat,
                1,  # Pattern = 1 (Rectangular)
                1,  # ConfineType = Ties
                column.cover,
                0,  # num_C_bars (not for rectangles)
                column.bars_3dir,  # Bars along local 3-axis
                column.bars_2dir,  # Bars along local 2-axis
                column.long_bar_size,
                column.tie_bar_size,
                column.tie_spacing,
                column.tie_legs_2dir,
                column.tie_legs_3dir,
                False  # ToBeDesigned = False
            )
            if ret != 0:
                raise Exception(f"Failed to assign rebar (Error code: {ret})")

            print(f"   ... Assigned rebar to {column.name}.")

        except Exception as e:
            print(f"❌ ERROR defining rectangular section '{column.name}': {e}")