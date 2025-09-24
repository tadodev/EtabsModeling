from models.element_infor import Concrete


def define_concrete_materials(sap_model, materials: list[Concrete]):
    """
    Defines one or more concrete materials in a SAP2000 model.

    This function checks if a material already exists before defining it.
    It sets the material's isotropic properties and its nonlinear
    stress-strain behavior using the Mander model.

    Args:
        sap_model: The active SAP2000 model object from the OAPI.
        materials: A list of `Concrete` dataclass objects to be defined.
    """
    MATERIAL_CONCRETE = 2  # SAP2000 API code for concrete material type

    try:
        # Get all existing material names once to avoid repeated API calls
        existing_mats = sap_model.PropMaterial.GetNameList()[1]

        for mat in materials:
            # --- Skip if material with the same name already exists ---
            if mat.name in existing_mats:
                print(f"Info: Material '{mat.name}' already exists. Skipping definition.")
                continue

            print(f"Defining material: '{mat.name}'...")

            # --- 1. Set the base material type to Concrete ---
            sap_model.PropMaterial.SetMaterial(mat.name, MATERIAL_CONCRETE)

            # --- 2. Define basic isotropic mechanical properties ---
            sap_model.PropMaterial.SetMPIsotropic(
                mat.name,
                mat.Ec,
                mat.nu,
                mat.alpha
            )

            # --- 3. Define nonlinear stress-strain properties (Mander model) ---
            # Note: StressStrainCurveType = 2 corresponds to the Mander model.
            # The 'fcs_factor' is ignored when using this model.
            sap_model.PropMaterial.SetOConcrete_1(
                mat.name,
                mat.fc,
                mat.is_lightweight,
                0,     # fcs_factor (ignored for Mander)
                1,     # ssc_type (stress-strain curve type) -> 1=Points
                2,     # ssh_type (hysteresis type) -> 2=Mander
                mat.strain_at_fc,
                mat.ultimate_strain,
                -0.1,  # Tension stiffening slope (use -0.1 for default behavior)
                0, 0   # Parameters for user-defined curves (not used here)
            )

    except Exception as e:
        print(f"Error: An exception occurred while defining concrete materials. Details: {e}")