import numpy as np
from math import factorial
from src.additional_math import Pixel, Point


class ParametricLines:

    @classmethod
    def bezier(cls, c_points: list[Point], color: str = '#000000',
               alpha: int = 255, **kwargs) -> None:
        CPOINTSAMOUNT = len(c_points)
        n = CPOINTSAMOUNT - 1
        i = 0
        steps = 100*CPOINTSAMOUNT if not kwargs.get('steps') else kwargs.get('steps')        
        t = np.linspace(0, 1, steps)        

        # binomial coeffs
        def n_i(n, i):
            return factorial(n) / (factorial(i) * factorial(n - i))
        
        # Berstein basis polynominal
        def basis_func(n, i, t):
            j = np.array(n_i(n, i) * t**i * (1 - t) ** (n - i))
            return j
        
        xBezier = np.zeros((steps, ))
        yBezier = np.zeros((steps,))
        
        for k in range(0, CPOINTSAMOUNT):
            xBezier = basis_func(n, i, t) * c_points[k].x + xBezier
            yBezier = basis_func(n, i, t) * c_points[k].y + yBezier
            i += 1
        
        px_list: list[Pixel] = [
            Pixel(Point(px[0], px[1]), color, alpha)
            for px in np.c_[xBezier, yBezier]
        ]
        return px_list

