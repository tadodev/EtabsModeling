from models.element_infor import Wall


def define_wall_sections(sap_model, walls: list[Wall]):
    unique_walls = {}
    for wall in walls:
        if wall.name not in unique_walls:
            unique_walls[wall.name] = wall

    # Get the list of existing shell property names
    _, existing_names, ret = sap_model.PropArea.GetNameList(0, [], 1)
    if ret != 0:
        raise Exception(f"Failed to retrieve shell property names. Error code: {ret}")

    existing_set = set(existing_names)

    defined_count = 0
    for wall in unique_walls.values():
        if wall.name in existing_set:
            # Wall section already exists, skip creation
            continue

        # Define the wall section
        ret = sap_model.PropArea.SetWall(
            wall.name,
            wall.wall_prop,
            wall.shell_type,
            wall.material,
            wall.wall_thk,
        )
        if ret != 0:
            raise Exception(f"Failed to define wall section {wall.name}. Error code: {ret}")
        defined_count += 1

    print(f"Successfully defined {defined_count} new unique wall sections (total unique: {len(unique_walls)}).")