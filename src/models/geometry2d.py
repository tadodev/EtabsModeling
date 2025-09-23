from dataclasses import dataclass
from typing import List, Tuple

Point2D = Tuple[float, float]


@dataclass
class Point2DGeom:
    p: Point2D


@dataclass
class Line2DGeom:
    start: Point2D
    end: Point2D


@dataclass
class Polygon2DGeom:
    vertices: List[Point2D]  # closed polyline
