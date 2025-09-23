from models.geometry2d import Point2DGeom, Line2DGeom, Polygon2DGeom
from utils.extruder import extrude_point, extrude_line, extrude_polygon
from utils.dxf_processing import _get_lines_by_layer, _get_polylines_by_layer, _get_points_by_layer


def get_columns(doc, layer, story_heights):
    base_points = _get_points_by_layer(doc, layer)
    return [extrude_point(Point2DGeom((x, y)), story_heights) for x, y, _ in base_points]


def get_walls(doc, layer, story_heights):
    base_lines = _get_lines_by_layer(doc, layer)
    return [extrude_line(Line2DGeom((x1, y1), (x2, y2)), story_heights) for (x1, y1, _), (x2, y2, _) in base_lines]


def get_slabs(doc, layer, story_heights):
    base_polys = _get_polylines_by_layer(doc, layer, closed_only=True)
    return [extrude_polygon(Polygon2DGeom([(x, y) for x, y, _ in pts]), story_heights) for pts in base_polys]
