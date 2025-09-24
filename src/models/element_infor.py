from dataclasses import dataclass


@dataclass
class Story:
    level: str
    height: float  # in ft for now
    is_master: bool = False
    similar_to: str = "None"
    splice_above: bool = False
    splice_height: float = 0.0
    color: int = 0


@dataclass
class Concrete:
    name: str
    fc: float
    Ec: float


@dataclass
class RectColumn:
    level: str
    section_name: str
    material: str
    b: float
    h: float
    long_bar_mat: str
    confine_mat: str
    cover: float
    bars_2dir: int
    bars_3dir: int
    long_bar_size: str
    tie_bar_size: str
    tie_spacing: float
    tie_legs_2dir: int
    tie_legs_3dir: int


@dataclass
class CircColumn:
    level: str
    section_name: str
    material: str
    dia: float
    long_bar_mat: str
    confine_mat: str
    cover: float
    num_bars: int
    long_bar_size: str
    tie_bar_size: str
    tie_spacing: float


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
