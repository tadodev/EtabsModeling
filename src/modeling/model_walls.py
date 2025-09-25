from typing import List

from models.geometry3d import WallGeom


def create_walls_in_etabs(sap_model, wall_geometries: List[WallGeom]):
    """
    Create wall elements in ETABS using the AddByCoord method.

    Args:
        sap_model: ETABS model object
        wall_geometries: List of WallGeom objects
    """
    created_count = 0

    for wall_geom in wall_geometries:
        try:
            # Create wall using ETABS API
            name = ""  # Will be assigned by ETABS
            ret = sap_model.AreaObj.AddByCoord(
                wall_geom.num_points,
                wall_geom.x_coord,
                wall_geom.y_coord,
                wall_geom.z_coord,
                name,  # Name (will be assigned by ETABS)
                wall_geom.prop_name,  # Section property name
                wall_geom.name,  # User name
                "Global"  # Coordinate system
            )

            if ret[1] != 0:  # ret[1] is the error code
                print(f"⚠️ Warning: Failed to create wall {wall_geom.name}. Error code: {ret[1]}")
            else:
                created_count += 1

        except Exception as e:
            print(f"❌ Error creating wall {wall_geom.name}: {e}")

    print(f"✅ Successfully created {created_count} walls in ETABS.")