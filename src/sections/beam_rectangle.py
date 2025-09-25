from models.element_infor import CouplingBeam


def define_beam_sections(sap_model, beams: list[CouplingBeam]):
    unique_beams = {}
    for beam in beams:
        if beam.name not in unique_beams:
            unique_beams[beam.name] = beam

    # Get the list of existing frame property names
    _, existing_names, ret = sap_model.PropFrame.GetNameList(0, [])
    if ret != 0:
        raise Exception(f"Failed to retrieve frame property names. Error code: {ret}")

    existing_set = set(existing_names)

    defined_count = 0
    for beam in unique_beams.values():
        if beam.name in existing_set:
            # Beam section already exists, skip creation
            continue

        # Define the rectangular geometry
        ret = sap_model.PropFrame.SetRectangle(
            beam.name,
            beam.material,
            beam.h,  # Depth (h)
            beam.b  # Width (b)
        )
        if ret != 0:
            raise Exception(f"Failed to define beam section geometry for {beam.name}. Error code: {ret}")

        # Assign rebar data
        ret = sap_model.PropFrame.SetRebarBeam(
            beam.name,
            beam.long_bar_mat,
            beam.tie_bar_mat,
            beam.cover_top,
            beam.cover_bot,
            beam.top_left_area,
            beam.top_right_area,
            beam.bot_left_area,
            beam.bot_right_area
        )
        if ret != 0:
            raise Exception(f"Failed to assign rebar to beam section {beam.name}. Error code: {ret}")

        defined_count += 1

    print(f"Successfully defined {defined_count} new unique beam sections (total unique: {len(unique_beams)}).")