import numpy as np
from math import factorial
from src.additional_math import Pixel, Point
from numbers import Number


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

    @classmethod
    def b_spline(cls, c_points: list[Point], color: str = '#000000',
                 alpha: int = 255, **kwargs) -> list[Pixel]:
        spline_order = kwargs['order']
        spline_degree = spline_order - 1
        steps = (250 * len(c_points) if not kwargs.get('steps') 
                 else kwargs.get('steps'))                   

        def de_boor(u: float, knots: list[Number], c_points: list[Point]):
            n = len(c_points) - 1  # Number of control points minus 1

            # Handle corner cases
            if u <= knots[spline_degree]:
                return c_points[0]
            elif u >= knots[n + spline_degree + 1]:
                return c_points[n]

            # Recursive de Boor's algorithm
            def de_boor_helper(i, j, u):
                if j == 1:                    
                    return c_points[i]
                else:
                    alpha = (u - knots[i]) / (knots[i + j] - knots[i])
                    return (de_boor_helper(i, j - 1, u).scalar_multiply(1 - alpha) +
                            de_boor_helper(i + 1, j - 1, u).scalar_multiply(alpha))

            return de_boor_helper(spline_degree, spline_degree + 1, u)        
        
        t = np.linspace(0, 1, len(c_points) + spline_order, endpoint=True)
        u_values = np.linspace(0, 1, steps) 

        px_list: list[Pixel] = [
            Pixel(de_boor(u, t, c_points), color, alpha)
            for u in u_values
        ]             
            
        return px_list            
