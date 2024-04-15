from enum import StrEnum


class AppStatesEnum(StrEnum):
    initial_render_state: str = 'initial'
    canvas_render_state: str = 'canvas'
    load_file_state: str = 'load'
    save_file_state: str = 'save'


class ToolsEnum(StrEnum):
    first_order_line: str = 'fst_ord_line'
    second_order_line: str = 'scnd_ord_line'
    parametric_line: str = 'param_line'
    polygon: str = 'polygon'
    transforming: str = 'transforming'
    delanay_voronoi: str = 'delanay-voronoi'

    @classmethod
    def to_list(cls) -> list:
        return [
            cls.first_order_line,
            cls.second_order_line,
            cls.parametric_line,
            cls.polygon,
            cls.transforming,
            cls.delanay_voronoi
        ]


class FirstOrderLineAlgorithmsEnum(StrEnum):
    dda: str = 'dda'
    bresenham: str = 'bresenham'
    wu: str = 'wu'
    guptasproull: str = 'gupta-sproull'

    @classmethod
    def to_list(cls) -> list:
        return [
            cls.dda,
            cls.bresenham,
            cls.wu,
            cls.guptasproull
        ]


class SecondOrderLineAlgorithmsEnum(StrEnum):
    circumference: str = 'circumference'
    ellipse: str = 'ellipse'
    hyperbola: str = 'hyperbola'
    parabola: str = 'parabols'

    @classmethod
    def to_list(cls) -> list:
        return [
            cls.circumference,
            cls.ellipse,
            cls.hyperbola,
            cls.parabola
        ]


class ParametricLinesAlgorithmsEnum(StrEnum):
    hermite: str = 'hermit'
    bezier: str = 'bezier'
    bspline: str = 'bspline'

    @classmethod
    def to_list(cls) -> list:
        return [
            cls.hermite,
            cls.bezier,
            cls.bspline
        ]


class TransformingAlgorithmsEnum(StrEnum):
    move: str = 'move'
    reflect: str = 'reflect'
    rotate: str = 'rotate'
    scale: str = 'scale'
    
    @classmethod
    def to_list(cls) -> list:
        return [
            cls.move,
            cls.reflect,
            cls.rotate,
            cls.scale
        ]


class PolygonAlgorithmsEnum(StrEnum):
    simple: str = 'simple'
    graham: str = 'graham'
    jarvis: str = 'jarvis'

    @classmethod
    def to_list(cls) -> list:
        return [
            cls.simple,
            cls.graham,
            cls.jarvis
        ]


class PolygonFillAlgorithmsEnum(StrEnum):
    scan_line_simple: str = 'scan_line_simple'
    scan_line: str = 'scan_line'
    simple_floodfill: str = 'floodfill_simple'
    scan_floodfill: str = 'floodfill_scan'

    @classmethod
    def to_list(cls) -> list:
        return [
            cls.scan_line_simple,
            cls.scan_line,
            cls.simple_floodfill,
            cls.scan_floodfill
        ]
    

class DelanayVoronoiAlgorithmsEnum(StrEnum):
    delanay: str = 'delanay'
    voronoi: str = 'voronoi'

    @classmethod
    def to_list(cls) -> list:
        return [
            cls.delanay,
            cls.voronoi
        ]
