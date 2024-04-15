from src.polygons.polygons import PolygonProperty, Polygon
from src.additional_math import Point, Pixel
from scipy.spatial import Delaunay, Voronoi
import numpy as np
from random import randint


def rrgb() -> str:
    return f'#{randint(0, 0xFFFFFF):06x}'


class DelanayTriangulation:

    @classmethod
    def triangulate(cls, c_points: list[Point], color: str = '#000000',
                    alpha: int = 255, **kwargs) -> list[Pixel]:
        if len(c_points) < 2:
            return []
        
        triangles = cls._handle_triangulation(c_points)
        px_list: list[Pixel] = []
        for tr in triangles:
            px_list.extend(Polygon.simple_polygon(
                tr, color, alpha, fill=True,
                fill_color=rrgb(),
                fill_algorithm='scan_line'
            ))
        return px_list
    
    @classmethod
    def _handle_triangulation(cls, c_points: list[Point]) -> list[list[Point]]:
        raw_points = np.array([(p.x, p.y) for p in c_points])
        triangles = Delaunay(raw_points)
        raw_tri_points = raw_points[triangles.simplices].tolist()
        return [[Point(p[0], p[1]) for p in tr]
                 for tr in raw_tri_points]


class VoronoiDiagram:

    @classmethod
    def diagram(cls, c_points: list[Point], color: str = '#000000',
                alpha: int = 255, **kwargs):
        raw_points = np.array([(p.x, p.y) for p in c_points])
        vor = Voronoi(raw_points)

        px_list: list[Pixel] = []
        regions = [[Point(p[0], p[1]) for p in raw_points[reg]]
                    for reg in vor.regions if len(reg) > 0]
        for region in regions:
            px_list.extend(
                Polygon.simple_polygon(region, color, alpha,
                                       fill=True,
                                       fill_color=rrgb(),
                                       fill_algorithm='scan_line')
            ) 
        return px_list        
