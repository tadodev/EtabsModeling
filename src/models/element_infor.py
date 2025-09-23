from dataclasses import dataclass


@dataclass
class Story:
    level: str
    height: float  # in ft for now


@dataclass
class Column:
    level: str
    material: str
    fc: float
    name: str
    d_or_b: float
    h: float


@dataclass
class Wall:
    level: str
    material: str
    fc: int
    name_x: str
    wall_x_thk: int
    name_y: str
    wall_y_thk: int


@dataclass
class CouplingBeam:
    level: str
    material: str
    fc: int
    name_x: str
    b_x: int
    h_x: int
    name_y: str
    b_y: int
    h_y: int


@dataclass
class Slab:
    level: str
    material: str
    fc: int
    name: str
    thickness: float
    sdl: float
    live: float
