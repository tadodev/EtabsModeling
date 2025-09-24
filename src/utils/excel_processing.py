# excel_processing.py

from typing import List
from openpyxl import load_workbook
from models.element_infor import Story, Column, Wall, CouplingBeam, Slab, Concrete


# ---------- STORY ----------
def read_story_table(path: str, sheet: str = "Story") -> List[Story]:
    wb = load_workbook(path, data_only=True)
    ws = wb[sheet]

    stories: List[Story] = []
    for row in ws.iter_rows(min_row=3, values_only=True):  # skip header
        if not row[0]:
            continue
        stories.append(Story(
            level=row[0],
            height=float(row[1])
        ))
    return stories


# ---------- STORY ----------
def read_concrete_table(path: str, sheet_name: str = "Material") -> List[Concrete]:
    """
    Reads the Concrete material table from Excel.

    Expected format in the sheet:
        Concrete   f'c (psi)   E (lb/in2)
        5750 psi   5750        4322239.003
        ...

    :param path: Path to Excel file
    :param sheet_name: Name of sheet containing material table
    :return: List of Concrete dataclass objects
    """
    wb = load_workbook(path, data_only=True)
    ws = wb[sheet_name]

    concretes: List[Concrete] = []

    # Skip header rows (assume first 2 rows are headers)
    for row in ws.iter_rows(min_row=3, values_only=True):
        if row[0] is None:
            continue
        name = str(row[0]).strip()
        fc = float(row[1])
        Ec = float(row[2])
        concretes.append(Concrete(name=name, fc=fc, Ec=Ec))

    return concretes


# ---------- COLUMN ----------
def read_column_table(path: str, sheet: str = "Rectangular column") -> List[Column]:
    wb = load_workbook(path, data_only=True)
    ws = wb[sheet]

    columns: List[Column] = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        if not row[0]:
            continue
        columns.append(Column(
            level=row[0],
            material=row[1],
            fc=float(row[2]),
            name=row[3],
            d_or_b=float(row[4]),
            h=float(row[5])
        ))
    return columns


# ---------- WALL ----------
def read_wall_table(path: str, sheet: str = "Wall") -> List[Wall]:
    wb = load_workbook(path, data_only=True)
    ws = wb[sheet]

    walls: List[Wall] = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        if not row[0]:
            continue
        walls.append(Wall(
            level=row[0],
            material=row[1],
            fc=int(row[2]),
            name_x=row[3],
            wall_x_thk=int(row[4]),
            name_y=row[5],
            wall_y_thk=int(row[6])
        ))
    return walls


# ---------- COUPLING BEAM ----------
def read_coupling_beam_table(path: str, sheet: str = "Coupling Beam") -> List[CouplingBeam]:
    wb = load_workbook(path, data_only=True)
    ws = wb[sheet]

    beams: List[CouplingBeam] = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        if not row[0]:
            continue
        beams.append(CouplingBeam(
            level=row[0],
            material=row[1],
            fc=int(row[2]),
            name_x=row[3],
            b_x=int(row[4]),
            h_x=int(row[5]),
            name_y=row[6],
            b_y=int(row[7]),
            h_y=int(row[8])
        ))
    return beams


# ---------- SLAB ----------
def read_slab_table(path: str, sheet: str = "Slab") -> List[Slab]:
    wb = load_workbook(path, data_only=True)
    ws = wb[sheet]

    slabs: List[Slab] = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        if not row[0]:
            continue
        slabs.append(Slab(
            level=row[0],
            material=row[1],
            fc=int(row[2]),
            name=row[3],
            thickness=float(row[4]),
            sdl=float(row[5]),
            live=float(row[6])
        ))
    return slabs
