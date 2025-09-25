from typing import List

from models.geometry3d import SlabGeom


def create_slabs_in_etabs(sap_model, slab_geometries: List[SlabGeom]):
    """
    Create slab elements in ETABS using the AddByCoord method.

    Args:
        sap_model: ETABS model object
        slab_geometries: List of SlabGeom objects
    """
    created_count = 0

    for slab_geom in slab_geometries:
        try:
            # Create slab using ETABS API
            name = ""  # Will be assigned by ETABS
            ret = sap_model.AreaObj.AddByCoord(
                slab_geom.num_points,
                slab_geom.x_coord,
                slab_geom.y_coord,
                slab_geom.z_coord,
                name,  # Name (will be assigned by ETABS)
                slab_geom.prop_name,  # Section property name
                slab_geom.name,  # User name
                "Global"  # Coordinate system
            )

            if ret[1] != 0:  # ret[1] is the error code
                print(f"⚠️ Warning: Failed to create slab {slab_geom.name}. Error code: {ret[1]}")
            else:
                created_count += 1

        except Exception as e:
            print(f"❌ Error creating slab {slab_geom.name}: {e}")

    print(f"✅ Successfully created {created_count} slabs in ETABS.")