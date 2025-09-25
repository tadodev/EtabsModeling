from models.element_infor import Slab


def define_slab_sections(sap_model, slabs: list[Slab]):
    unique_slabs = {}
    for slab in slabs:
        if slab.name not in unique_slabs:
            unique_slabs[slab.name] = slab

    # Get the list of existing shell property names
    _, existing_names, ret = sap_model.PropArea.GetNameList(0, [], 1)
    if ret != 0:
        raise Exception(f"Failed to retrieve shell property names. Error code: {ret}")

    existing_set = set(existing_names)

    defined_count = 0
    for slab in unique_slabs.values():
        if slab.name in existing_set:
            # Slab section already exists, skip creation
            continue

        # Define the slab section
        ret = sap_model.PropArea.SetSlab(
            slab.name,
            slab.slab_prop,
            slab.shell_type,
            slab.material,
            slab.slab_thk,

        )
        if ret != 0:
            raise Exception(f"Failed to define slab section {slab.name}. Error code: {ret}")
        defined_count += 1

    print(f"Successfully defined {defined_count} new unique slab sections (total unique: {len(unique_slabs)}).")