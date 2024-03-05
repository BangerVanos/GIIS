from enum import StrEnum


class AppStates(StrEnum):
    initial_render_state: str = 'initial'
    canvas_render_state: str = 'canvas'
    load_file_state: str = 'load'
    save_file_state: str = 'save'


class Tools(StrEnum):
    first_order_line: str = 'fst_ord_line'
    second_order_line: str = 'scnd_ord_line'
    parametric_line: str = 'param_line'
    transforming: str = 'transforming'


class FirstOrderLineAlgorithms(StrEnum):
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


class SecondOrderLineAlgorithms(StrEnum):
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


class ParametricLinesAlgorithms(StrEnum):
    hermit: str = 'hermit'
    bezier: str = 'bezier'
    bspline: str = 'bspline'

    @classmethod
    def to_list(cls) -> list:
        return [
            cls.hermit,
            cls.bezier,
            cls.bspline
        ]
