import sys
import comtypes
import ezdxf
from ezdxf.document import Drawing


# ---------- DXF I/O ----------
def read_dxf_plan(path: str) -> Drawing:
    try:
        doc = ezdxf.readfile(path)
        print(f"Reading DXF plan: {path}")
        return doc
    except (IOError, comtypes.COMError):
        sys.exit("Not a DXF file or a generic I/O error.")
    except ezdxf.DXFStructureError:
        sys.exit("Invalid or corrupt DXF file.")


def get_model_space(doc: Drawing):
    try:
        return doc.modelspace()
    except Exception:
        sys.exit("Could not find modelspace.")


# ---------- Base extractors ----------
def get_points_by_layer(doc: Drawing, layer: str):
    msp = get_model_space(doc)
    return [
        (pt.dxf.location.x, pt.dxf.location.y, pt.dxf.location.z)
        for pt in msp.query(f'POINT[layer=="{layer}"]')
    ]


def get_lines_by_layer(doc: Drawing, layer: str):
    msp = get_model_space(doc)
    return [
        ((e.dxf.start.x, e.dxf.start.y, e.dxf.start.z),
         (e.dxf.end.x, e.dxf.end.y, e.dxf.end.z))
        for e in msp.query("LINE") if e.dxf.layer == layer
    ]


def get_polylines_by_layer(doc: Drawing, layer: str, closed_only: bool = False):
    msp = doc.modelspace()
    polys = []

    for e in msp.query("LWPOLYLINE POLYLINE"):
        if e.dxf.layer != layer:
            continue
        if closed_only and not e.closed:
            continue

        if e.dxftype() == "LWPOLYLINE":
            pts = [(x, y, 0.0) for x, y, *_ in e.get_points()]  # (x, y, start_width, end_width, bulge)
        elif e.dxftype() == "POLYLINE":
            pts = [(v.dxf.location.x, v.dxf.location.y, v.dxf.location.z) for v in e.vertices]
        else:
            continue

        polys.append(pts)

    return polys
