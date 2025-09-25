from typing import List

from models.geometry3d import BeamGeom


def create_beams_in_etabs(sap_model, beam_geometries: List[BeamGeom]):
    """
    Create coupling beam elements in ETABS using the AddByCoord method.

    Args:
        sap_model: ETABS model object
        beam_geometries: List of BeamGeom objects
    """
    created_count = 0

    for beam_geom in beam_geometries:
        try:
            # Extract coordinates
            xi, yi, zi = beam_geom.start_point
            xj, yj, zj = beam_geom.end_point

            # Create beam using ETABS API
            name = ""  # Will be assigned by ETABS
            ret = sap_model.FrameObj.AddByCoord(
                xi, yi, zi,  # I-End coordinates
                xj, yj, zj,  # J-End coordinates
                name,  # Name (will be assigned by ETABS)
                beam_geom.prop_name,  # Section property name
                beam_geom.name,  # User name
                "Global"  # Coordinate system
            )

            if ret[1] != 0:  # ret[1] is the error code
                print(f"⚠️ Warning: Failed to create coupling beam {beam_geom.name}. Error code: {ret[1]}")
            else:
                created_count += 1

        except Exception as e:
            print(f"❌ Error creating coupling beam {beam_geom.name}: {e}")

    print(f"✅ Successfully created {created_count} coupling beams in ETABS.")