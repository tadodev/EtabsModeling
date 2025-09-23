def define_concrete_materials(sap_model):
    MATERIAL_CONCRETE = 2
    sap_model.PropMaterial.SetMaterial("CONC", MATERIAL_CONCRETE)
    sap_model.PropMaterial.SetMPIsotropic("CONC", 3600, 0.2, 0.0000055)
