import numpy as np
from math import factorial
from src.additional_math import Pixel, Point
from numbers import Number
from scipy.interpolate import BSpline
from scipy.interpolate import splrep


class ParametricLines:

    @classmethod
    def bezier(cls, c_points: list[Point], color: str = '#000000',
               alpha: int = 255, **kwargs) -> None:
        
        # Check whether curve is enclosed
        if kwargs.get('enclosed'):
            c_points.append(c_points[0])

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

    # @classmethod
    # def b_spline(cls, c_points: list[Point], color: str = '#000000',
    #              alpha: int = 255, **kwargs) -> list[Pixel]:                
        
    #     segments = [c_points[i:i+2] for i in range(len(c_points) - 1)]
    #     cp_x_arr = np.array([point.x for point in c_points])
    #     srt_cp_x_arr_indx = np.argsort(cp_x_arr)
    #     cp_y_arr = np.array([point.y for point in c_points])
    #     tck = splrep(cp_x_arr[srt_cp_x_arr_indx],
    #                  cp_y_arr[srt_cp_x_arr_indx], s=0, k=3)
    #     px_list: list[Pixel] = []        
    #     b_spline = BSpline(*tck)
    #     for segment in segments:
    #         steps = int(segment[0].distance(segment[-1]))
    #         x_coords = list(np.linspace(segment[0].x, segment[-1].x, steps))            
    #         px_list.extend([
    #             Pixel(Point(x, y), color, alpha)
    #             for x, y in zip(x_coords, b_spline(x_coords))
    #         ])      
            
    #     return px_list

    @classmethod
    def b_spline(cls, c_points: list[Point], color: str = '#000000',
                 alpha: int = 255, **kwargs) -> list[Pixel]:
        
        # Check whether curve is enclosed
        if kwargs.get('enclosed'):
            c_points.append(c_points[0])

        points_amount = len(c_points)
        c_points.insert(0, c_points[0])
        c_points.append(c_points[-1])

        seg_steps = 100 if not kwargs.get('steps') else kwargs['steps']

        px_list: list[Pixel] = []

        def find_segment(i):
            par_list = np.linspace(0, 1, seg_steps)
            for t in par_list:
                point = ((1/6) * np.array([t**3, t**2, t, 1]) @ np.array([[-1, 3, -3, 1],
                                                                         [3, -6, 3, 0],
                                                                         [-3, 0, 3, 0],
                                                                         [1, 4, 1, 0]])
                        @ np.array([[c_points[i - 1].x, c_points[i - 1].y],
                                    [c_points[i].x, c_points[i].y],
                                    [c_points[i + 1].x, c_points[i + 1].y],
                                    [c_points[i + 2].x, c_points[i + 2].y]]))
                px_list.append(
                    Pixel(Point(point[0], point[1]), color, alpha)
                )
        
        for i in range(1, points_amount):
            find_segment(i)
        
        return px_list

    @classmethod
    def hermite(cls, c_points: list[Point], color: str = '#000000',
                alpha: int = 255, **kwargs) -> list[Pixel]:
        def t(x: Number, xk: Number, xk1: Number):
            return (x - xk) / (xk1 - xk)

        def deriv(pk0: Point, pk1: Point, pk2: Point,
                  xk0: Number, xk1: Number, xk2: Number):
            
            if xk1 == xk0:
                xk0 = 0
            if xk2 == xk1:
                xk1 = 0

            return (((pk1 - pk0) / (2 * (xk1 - xk0)))
                    + ((pk2 - pk1) / (2 * (xk2 - xk1))))
        
        def p(t, pk, pk1, mk, mk1, xk, xk1):
            return (pk * (2 * t**3 - 3 * t**2 + 1) +
                    mk * (xk1 - xk) * (t**3 - 2 * t**2 + t) +
                    pk1 * (-2 * t**3 + 3 * t**2) +
                    mk1 * (t**3 - t**2) * (xk1 - xk))
        
        px_list: list[Pixel] = []
        steps = 200 if not kwargs.get('steps') else kwargs.get('steps')

        # Check whether curve is enclosed
        if kwargs.get('enclosed'):
            c_points.append(c_points[0])

        # Creating boundary points
        c_points.insert(0, c_points[0])
        c_points.append(c_points[-1])

        px_list: list[Pixel] = []
        
        for i in range(1, len(c_points) - 2):
            steps = (int(c_points[i].distance(c_points[i + 1])) * 10
                     if not kwargs.get('steps') else kwargs.get('steps'))            
            x_coords = np.linspace(c_points[i].x, c_points[i + 1].x,
                                   steps)
            
            mk = deriv(pk0=c_points[i - 1], pk1=c_points[i],
                       pk2=c_points[i + 1], xk0=c_points[i - 1].x,
                       xk1=c_points[i].x, xk2=c_points[i + 1].x)
            mk1 = deriv(pk0=c_points[i], pk1=c_points[i + 1],
                        pk2=c_points[i + 2], xk0=c_points[i].x,
                        xk1=c_points[i + 1].x, xk2=c_points[i + 2].x)
            px_list.extend(
                [
                    Pixel(p(t(x, c_points[i].x, c_points[i + 1].x),
                            c_points[i], c_points[i + 1],
                            mk, mk1, c_points[i].x, c_points[i + 1].x),
                            color, alpha)
                    for x in x_coords
                ]
            )

        return px_list

