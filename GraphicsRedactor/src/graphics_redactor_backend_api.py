from PIL import Image as img
from additional_math import Point, Pixel


class Drawer:

    def __init__(self, canvas: img.Image) -> None:
        self._canvas: img.Image = canvas
    
    def draw_point(self, point: Point, color: str) -> None:
        pass
