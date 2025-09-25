from typing import List, Tuple

from models.element_infor import Story
from src.models.geometry3d import Point2DGeom, Line2DGeom, Polygon2DGeom

Point3D = Tuple[float, float, float]


def extrude_point(point: Point2DGeom, stories: list[Story]) -> List[Point3D]:
    """Extrude a single point vertically through story heights."""
    z = 0.0
    pts = []
    for h in stories:
        z += h
        pts.append((point.p[0], point.p[1], z))
    return pts


def extrude_line(line: Line2DGeom, story_heights: List[float]) -> List[Tuple[Point3D, Point3D]]:
    """Extrude a line into vertical wall segments."""
    z = 0.0
    walls = []
    for h in story_heights:
        z_next = z + h
        walls.append((
            (line.start[0], line.start[1], z), (line.end[0], line.end[1], z),
            (line.start[0], line.start[1], z_next), (line.end[0], line.end[1], z_next)
        ))
        z = z_next
    return walls


def extrude_polygon(poly: Polygon2DGeom, story_heights: List[float]) -> List[List[Point3D]]:
    """Extrude polygon into slabs at each story level."""
    z = 0.0
    slabs = []
    for h in story_heights:
        z += h
        elevated = [(x, y, z) for (x, y) in poly.vertices]
        slabs.append(elevated)
    return slabs
