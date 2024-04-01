from PIL import Image as img
from PIL import ImageColor
from .additional_math import Point, Pixel
from .first_order_lines.first_order_lines import FirstOrderLine
from .second_order_lines.second_order_lines import SecondOrderLine
from .parametric_lines.parametric_lines import ParametricLines
from .polygons.polygons import Polygon
from . app_enums import (ToolsEnum,
                         FirstOrderLineAlgorithmsEnum,
                         SecondOrderLineAlgorithmsEnum,
                         ParametricLinesAlgorithmsEnum,
                         PolygonAlgorithmsEnum)


class Drawer:

    def __init__(self, canvas: img.Image) -> None:
        self._canvas: img.Image = canvas
    
    def draw_point(self, point: Point, color: str, alpha: int = 255) -> None:
        pil_color = list(ImageColor.getrgb(color))
        if len(pil_color) < 4:
            pil_color.append(alpha)
        pil_color = tuple(pil_color)
        try:
            self._canvas.putpixel((int(point.x), int(point.y)), pil_color)
        except IndexError as err:
            print(f'{err}. Tried to put pixel with coords {(point.x, point.y)} '
                  f'on image of size {self._canvas.size}')
    
    def draw_pixel(self, pixel: Pixel) -> None:
        self.draw_point(pixel.point, pixel.color, pixel.alpha)

    def draw_pixels(self, pixels: list[Pixel] | tuple[Pixel]):
        for pixel in pixels:
            self.draw_pixel(pixel)
    
    def set_canvas(self, canvas: img.Image) -> None:
        self._canvas = canvas


class ShapeDrawer:

    def __init__(self, canvas: img.Image) -> None:
        self._drawer = Drawer(canvas)

        self._shapes_algorithms = {
            ToolsEnum.first_order_line: {
                FirstOrderLineAlgorithmsEnum.dda: FirstOrderLine.dda,
                FirstOrderLineAlgorithmsEnum.bresenham: FirstOrderLine.bresenham,
                FirstOrderLineAlgorithmsEnum.wu: FirstOrderLine.wu,
                FirstOrderLineAlgorithmsEnum.guptasproull: FirstOrderLine.gupta_sproull
            },

            ToolsEnum.second_order_line: {
                SecondOrderLineAlgorithmsEnum.circumference: SecondOrderLine.circumference,
                SecondOrderLineAlgorithmsEnum.ellipse: SecondOrderLine.ellipse,
                SecondOrderLineAlgorithmsEnum.hyperbola: SecondOrderLine.hyperbola,
                SecondOrderLineAlgorithmsEnum.parabola: SecondOrderLine.parabola
            },

            ToolsEnum.parametric_line: {
                ParametricLinesAlgorithmsEnum.bezier: ParametricLines.bezier,
                ParametricLinesAlgorithmsEnum.bspline: ParametricLines.b_spline,
                ParametricLinesAlgorithmsEnum.hermite: ParametricLines.hermite
            },

            ToolsEnum.polygon: {
                PolygonAlgorithmsEnum.simple: Polygon.simple_polygon,
                PolygonAlgorithmsEnum.graham: Polygon.graham,
                PolygonAlgorithmsEnum.jarvis: Polygon.jarvis
            }
        }

    def draw_shape(self, tool: str, algorithm: str, points: list[Point],
                   color: str = '#000000', alpha: int = 255, **kwargs) -> None:
        if tool == ToolsEnum.first_order_line:
            self._draw_first_order_line(algorithm, points[0], points[1],
                                        color, alpha)
        elif tool == ToolsEnum.second_order_line:
            self._draw_second_order_line(algorithm, points,
                                         color, alpha)
        elif tool == ToolsEnum.parametric_line:            
            self._draw_parametric_line(algorithm, points,
                                       color, alpha, **kwargs)
        elif tool == ToolsEnum.polygon:
            self._draw_polygon(algorithm, points,
                               color, alpha, **kwargs)       
    
    def _draw_first_order_line(self, algorithm: str, start: Point, end: Point,
                               color: str = '#000000', alpha: int = 255) -> None:
        self._drawer.draw_pixels(
            self._shapes_algorithms[ToolsEnum.first_order_line][algorithm](
                start, end, color, alpha
            )
        )
    
    def _draw_second_order_line(self, algorithm: str, points: list[Point],
                                color: str = '#000000', alpha: int = 255) -> None:
        self._drawer.draw_pixels(
            self._shapes_algorithms[ToolsEnum.second_order_line][algorithm](
                *points, color, alpha
            )
        )
    
    def _draw_parametric_line(self, algorithm: str, points: list[Point],
                              color: str = '#000000', alpha: int = 255,
                              **kwargs) -> None:
        self._drawer.draw_pixels(
            self._shapes_algorithms[ToolsEnum.parametric_line][algorithm](
                points, color, alpha, **kwargs
            )
        )
    
    def _draw_polygon(self, algorithm: str, points: list[Point],
                      color: str = '#000000', alpha: int = 255,
                      **kwargs) -> None:
        self._drawer.draw_pixels(
            self._shapes_algorithms[ToolsEnum.polygon][algorithm](
                points, color, alpha, **kwargs
            )
        )
    
    def set_canvas(self, canvas: img.Image) -> None:
        self._drawer.set_canvas(canvas)
