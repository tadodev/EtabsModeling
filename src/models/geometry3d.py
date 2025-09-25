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
    end_point: Point3D
    prop_name: str
    name: str = ""


@dataclass
class WallGeom:
    num_points: int
    x_coord: List[float]
    y_coord: List[float]
    z_coord: List[float]
    prop_name: str
    name: str = ""


@dataclass
class SlabGeom:
    num_points: int
    x_coord: List[float]
    y_coord: List[float]
    z_coord: List[float]
    prop_name: str
    name: str = ""
