# Example CLI usage
# -----------------------
from connection.etabs_connection import connect_to_etabs
from utils.build_etabs_data import build_etabs_model_data

if __name__ == "__main__":
    # import pprint
    # excel = r"data/Input Data_V02.xlsx"
    # dxf = r"data/PLan View_V02.dxf"
    #
    # data = build_etabs_model_data(excel, dxf, column_layer="REC COLS", wall_layer="WALL", slab_layer="SLAB")
    #
    # print("Stories (top-down from excel):")
    # pprint.pprint(data["stories"])
    #
    # print("\nHeights (bottom-up):", data["heights_list"])
    # print("\nBase map (elev -> level):")
    # pprint.pprint(data["base_map"])
    #
    # print("\nSample merged column segment (first 6):")
    # for c in data["columns"][:6]:
    #     pprint.pprint(c)
    #
    # print("\nSample merged wall panel (first 6):")
    # for w in data["walls"][:6]:
    #     pprint.pprint(w)
    #
    # print("\nSample merged slab (first 6):")
    # for s in data["slabs"][:6]:
    #     pprint.pprint(s)
    sap_model = connect_to_etabs()
    ret = sap_model.PropMaterial.SetMaterial("Concrete", 2)

    ret = sap_model.PropMaterial.SetOConcrete_1("Concrete", 6, False, 0, 1, 2, 0.0022, 0.0052, -0.1, 0, 0)

    ret = sap_model.PropMaterial.SetMaterial('6000psi', 2)

    # assign isotropic mechanical properties to material


