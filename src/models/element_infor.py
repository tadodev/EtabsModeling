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
    fc: float  # Compressive strength (f'c), e.g., in MPa
    Ec: float  # Modulus of Elasticity, e.g., in MPa

    # Optional mechanical properties with sensible defaults
    nu: float = 0.2  # Poisson's ratio
    alpha: float = 9.9e-6  # Co eff. of thermal expansion, per degree Celsius

    # Optional nonlinear properties with sensible defaults
    is_lightweight: bool = False
    strain_at_fc: float = 0.0022  # Strain at maximum compressive stress
    ultimate_strain: float = 0.005  # Ultimate crushing strain for concrete


@dataclass
class RectColumn:
    level: str
    name: str
    material: str
    b: float
    h: float
    long_bar_mat: str
    tie_bar_mat: str
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
    name: str
    material: str
    dia: float
    long_bar_mat: str
    tie_bar_mat: str
    cover: float
    num_C_bars: int
    long_bar_size: str
    tie_bar_size: str
    tie_spacing: float


@dataclass
class Wall:
    level: str
    name: str
    material: str
    wall_thk: float
    wall_prop: int = 1  # 1 = specified
    shell_type: int = 1  # 1= shellThin


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
