from PIL import Image as img
import numpy as np
from typing import Literal
from numbers import Number


class ImageTransformer:
    
    def __init__(self, canvas: img.Image, view):
        self._canvas = canvas
        self._view = view
    
    def set_canvas(self, canvas: img.Image):
        self._canvas = canvas
    
    def move(self, axis: Literal['x', 'y'], amount: int):
        matrix = np.array(
            [
                [1, 0, (axis == 'x') * amount],
                [0, 1, (axis == 'y') * amount],
                [0, 0, 1]
            ]
        )
        self._transform(matrix)
    
    def rotate(self, degree: int):
        degree = np.deg2rad(degree)        
        matrix = np.array(
            [
                [np.cos(degree), -np.sin(degree), 0],
                [np.sin(degree), np.cos(degree), 0],
                [0, 0, 1]
            ]
        )
        self._transform(matrix)
    
    def scale(self, scale_x: Number, scale_y: Number):
        matrix = np.array(
            [
                [scale_x, 0, 0],
                [0, scale_y, 0],
                [0, 0, 1]
            ]
        )
        self._transform(matrix)
    
    def reflect(self, axis: Literal['x', 'y']):
        matrix = np.array(
            [
                [1 if axis == 'x' else -1, 0, 0],
                [0, 1 if axis == 'y' else -1, 0],
                [0, 0, 1]
            ]
        )
        self._transform(matrix)
    
    def _transform(self, matrix):
        transformed_canvas = self._canvas.transform(self._canvas.size, img.AFFINE,
                                                    data=np.linalg.inv(matrix).flatten()[:6],
                                                    resample=img.BICUBIC,
                                                    fillcolor=(255, 255, 255))
        self._view.set_canvas(transformed_canvas)
