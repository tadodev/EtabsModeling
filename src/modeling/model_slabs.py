from typing import List

from models.geometry3d import SlabGeom


def create_slabs_in_etabs(sap_model, slab_geometries: List[SlabGeom],
                          sdl_name: str = "Dead", liveload_name: str = "Live"):
    """
    Create slab elements in ETABS using the AddByCoord method.

    Args:
        :param sap_model: ETABS model object
        :param slab_geometries: List of SlabGeom objects
        :param sdl_name: Name of the sdl load pattern
        :param liveload_name: Name of the live load pattern
    """
    created_count = 0

    for slab_geom in slab_geometries:
        try:
            # Create slab using ETABS API
            name = ""  # Will be assigned by ETABS
            returned = sap_model.AreaObj.AddByCoord(
                slab_geom.num_points,
                slab_geom.x_coord,
                slab_geom.y_coord,
                slab_geom.z_coord,
                name,  # Name (will be assigned by ETABS)
                slab_geom.prop_name,  # Section property name
                slab_geom.name,  # User name
                "Global"  # Coordinate system
            )
            etabs_name = returned[-2]  # ret[-2] is the ETABS-assigned name
            if returned[-1] != 0:  # ret[-1] is the error code
                print(f"⚠️ Warning: Failed to create slab {slab_geom.name}. Error code: {ret[1]}")
            else:
                created_count += 1

            # Assign SDL and Live Load
            Object = 0
            sdl_value = slab_geom.sdl  # in psf
            live_value = slab_geom.live  # in psf
            if live_value > 0:
                ret_live = sap_model.AreaObj.SetLoadUniform(
                    etabs_name,
                    liveload_name,
                    live_value/144,  # convert psf to psi
                    11,  # project gravity
                    True,
                    "Global",
                    Object
                )

            if sdl_value > 0:
                ret_sdl = sap_model.AreaObj.SetLoadUniform(
                    etabs_name,
                    sdl_name,
                    sdl_value/144,  # convert psf to psi
                    11,  # project gravity
                    True,
                    "Global",
                    Object
                )

        except Exception as e:
            print(f"❌ Error creating slab {slab_geom.name}: {e}")

    print(f"✅ Successfully created {created_count} slabs in ETABS.")
