import sys
import comtypes.client
import comtypes.gen.ETABSv1

default_path = r"C:\Program Files\Computers and Structures\ETABS 22\ETABS.exe"


def connect_to_etabs(attach_to_instance=True, specify_path=False, program_path=default_path):

    helper = comtypes.client.CreateObject("ETABSv1.Helper")
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

    if attach_to_instance:
        try:
            etabs_object = helper.GetObject("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            print("No running instance of ETABS found or failed to attach.")
            sys.exit(-1)
    else:
        try:
            if specify_path:
                etabs_object = helper.CreateObject(program_path)
            else:
                etabs_object = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        except (OSError, comtypes.COMError):
            print("Cannot start ETABS.")
            sys.exit(-1)
        etabs_object.ApplicationStart()

    sap_model = etabs_object.SapModel

    return sap_model
