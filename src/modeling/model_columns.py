from typing import List

from models.geometry3d import ColumnGeom


def create_columns_in_etabs(sap_model, column_geometries: List[ColumnGeom]):
    """
    Create column elements in ETABS using the AddByCoord method.

    Args:
        sap_model: ETABS model object
        column_geometries: List of ColumnGeom objects
    """
    created_count = 0

    for col_geom in column_geometries:
        try:
            # Extract coordinates
            xi, yi, zi = col_geom.start_point
            xj, yj, zj = col_geom.end_point

            # Create column using ETABS API
            name = ""  # Will be assigned by ETABS
            ret = sap_model.FrameObj.AddByCoord(
                xi, yi, zi,  # I-End coordinates
                xj, yj, zj,  # J-End coordinates
                name,  # Name (will be assigned by ETABS)
                col_geom.prop_name,  # Section property name
                col_geom.name,  # User name
                "Global"  # Coordinate system
            )

            if ret[1] != 0:  # ret[1] is the error code
                print(f"⚠️ Warning: Failed to create column {col_geom.name}. Error code: {ret[1]}")
            else:
                created_count += 1

        except Exception as e:
            print(f"❌ Error creating column {col_geom.name}: {e}")

    print(f"✅ Successfully created {created_count} columns in ETABS.")
