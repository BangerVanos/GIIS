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
