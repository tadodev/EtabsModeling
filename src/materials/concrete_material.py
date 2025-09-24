from models.element_infor import Concrete


def define_concrete_material(sap_model, concrete: Concrete):
    MATERIAL_CONCRETE = 2

    # Define material only if not already present
    mat_names = sap_model.PropMaterial.GetNameList()[1]
    if concrete.name not in mat_names:
        sap_model.PropMaterial.SetMaterial(concrete.name, MATERIAL_CONCRETE)

    # Define isotropic properties
    sap_model.PropMaterial.SetMPIsotropic(
        concrete.name,
        concrete.Ec,
        concrete.nu if hasattr(concrete, "nu") else 0.2,
        concrete.alpha if hasattr(concrete, "alpha") else 0.0000055
    )

    # Define concrete stress-strain properties
    sap_model.PropMaterial.SetOConcrete_1(
        concrete.name,
        concrete.fc,
        False,  # lightweight
        0,  # fcs factor
        1, 2,  # stress-strain curve type
        0.0022,  # strain at f'c
        0.0052,  # crushing strain
        -0.1,  # tension stiffening
        0, 0  # other params
    )
