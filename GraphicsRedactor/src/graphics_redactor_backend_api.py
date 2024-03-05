from PIL import Image as img
from PIL import ImageColor
from .additional_math import Point, Pixel
from .first_order_lines.first_order_lines import FirstOrderLine
from . app_enums import ToolsEnum, FirstOrderLineAlgorithmsEnum


class Drawer:

    def __init__(self, canvas: img.Image) -> None:
        self._canvas: img.Image = canvas
    
    def draw_point(self, point: Point, color: str, alpha: int = 255) -> None:
        pil_color = list(ImageColor.getrgb(color))
        if len(pil_color) < 4:
            pil_color.append(alpha)
        pil_color = tuple(pil_color)
        self._canvas.putpixel((int(point.x), int(point.y)), pil_color)
    
    def draw_pixel(self, pixel: Pixel) -> None:
        self.draw_point(pixel.point, pixel.color, pixel.alpha)

    def draw_pixels(self, pixels: list[Pixel] | tuple[Pixel]):
        for pixel in pixels:
            self.draw_pixel(pixel)


class ShapeDrawer:

    def __init__(self, canvas: img.Image) -> None:
        self._drawer = Drawer(canvas)

        self._shapes_algorithms = {
            ToolsEnum.first_order_line: {
                FirstOrderLineAlgorithmsEnum.dda: FirstOrderLine.dda,
                FirstOrderLineAlgorithmsEnum.bresenham: FirstOrderLine.bresenham,
                FirstOrderLineAlgorithmsEnum.wu: FirstOrderLine.wu,
                FirstOrderLineAlgorithmsEnum.guptasproull: FirstOrderLine.gupta_sproull
            }
        }

    def draw_shape(self, tool: str, algorithm: str, points: list[Point],
                   color: str = '#000000', alpha: int = 255) -> None:
        if tool == ToolsEnum.first_order_line:
            self._draw_first_order_line(algorithm, points[0], points[1],
                                        color, alpha)        
    
    def _draw_first_order_line(self, algorithm: str, start: Point, end: Point,
                               color: str = '#000000', alpha: int = 255) -> None:
        self._drawer.draw_pixels(
            self._shapes_algorithms[ToolsEnum.first_order_line][algorithm](
                start, end, color, alpha
            )
        )
