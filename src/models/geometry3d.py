from dataclasses import dataclass
from typing import List, Tuple

Point3D = Tuple[float, float, float]


@dataclass
class ColumnGeom:
    start_point: Point3D
    end_point: Point3D
    prop_name: str
    name: str = ""


@dataclass
class BeamGeom:
    start_point: Point3D
    start_point: Point3D
    prop_name: str
    name: str = ""


@dataclass
class WallGeom:
    num_points: int
    x_coord: List[Point3D]
    y_coord: List[Point3D]
    z_coord: List[Point3D]
    prop_name: str
    name: str = ""


class SlabGeom:
    num_points: int
    x_coord: List[Point3D]
    y_coord: List[Point3D]
    z_coord: List[Point3D]
    prop_name: str
    name: str
