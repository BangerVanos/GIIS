import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates as img_coords
from PIL import Image as img
from src.app_enums import AppStatesEnum, ToolsEnum
from src.app_enums import (FirstOrderLineAlgorithmsEnum,
                           SecondOrderLineAlgorithmsEnum,
                           ParametricLinesAlgorithmsEnum)
from src.graphics_redactor_backend_api import ShapeDrawer
from src.additional_math import Point


class GraphicsRedactorView:
    
    def __init__(self) -> None:
        st.set_page_config('Graphics Redactor', layout='wide')
        if st.session_state.get('app_state') is None:
            st.session_state['app_state'] = AppStatesEnum.initial_render_state
        
        self._state_render_funcs = {
            AppStatesEnum.initial_render_state: self._render_initial,
            AppStatesEnum.canvas_render_state: self._render_canvas,
            AppStatesEnum.load_file_state: self._render_load,
            AppStatesEnum.save_file_state: self._render_save,
            None: self._render_initial
        }

        self._placeholder = st.empty()        
    
    def run(self) -> None:        
        self._render()

    def _render(self) -> None:                       
        self._state_render_funcs[st.session_state.get('app_state')]()        
    
    def _render_initial(self) -> None:
        st.write('### Simple graphics redactor')
        new_tab, load_tab, info_tab = st.tabs(['New image', 'Load image', 'App info'])
        with new_tab:
            st.header('New image')
            width_input = st.number_input(
                label='Image width',
                min_value=10,
                key='image_width_input',
                value=1280
            )
            height_input = st.number_input(
                label='Image height',
                min_value=10,
                key='image_height_input',
                value=720   
            )        
            st.button('New canvas', key='new_canvas_btn',
                      on_click=self._new_canvas)

    def _render_canvas(self) -> None:               
        with self._placeholder.container(border=False):
            tool_col, canvas_col = st.columns([2, 9])
            with tool_col:
                color_select = st.color_picker(
                    label='Select pixel color',
                    key='color_select',
                    help='Select color of your shapes'
                )                
                tool_select = st.radio(
                    label='Select tool',
                    options=[
                        ToolsEnum.first_order_line,
                        ToolsEnum.second_order_line,
                        ToolsEnum.parametric_line,
                        ToolsEnum.transforming
                    ],
                    format_func=self._tool_format_func,
                    key='tool_selector'
                )
                if tool_select:
                    self._render_tool_algorithms(tool_col)                
            with canvas_col:                
                click_coords = img_coords(
                    st.session_state['canvas_image'],
                    key='canvas_click_coords'    
                )
                if click_coords:
                    self._handle_canvas_click(click_coords)                    
                new_img_col, save_img_col, debug_col, blank_col = st.columns([2, 2, 2, 10], gap='small')
                with new_img_col:
                    st.button(label='Clear canvas', use_container_width=True,
                              on_click=self._clear_canvas)
                with save_img_col:
                    st.button(label='Save image', use_container_width=True)
                with debug_col:
                    st.checkbox(label='Debug?',
                                key='debug_enabled',
                                help='Check this to enable debug option')              

    def _render_load(self) -> None:
        pass

    def _render_save(self) -> None:
        pass

    def _new_canvas(self) -> None:
        width = st.session_state.get('image_width_input')
        height = st.session_state.get('image_height_input')
        st.session_state['canvas_image'] = img.new('RGB', (width, height), color='white')
        st.session_state['canvas_figures'] = dict()
        st.session_state['drawer'] = ShapeDrawer(st.session_state['canvas_image'])
        st.session_state['points_list'] = None
        self._switch_to_canvas()

    def _clear_canvas(self) -> None:
        size = st.session_state['canvas_image'].size
        st.session_state['points_list'] = None
        st.session_state['canvas_image'] = img.new('RGB', size, color='white')
        st.session_state['canvas_figures'] = dict()
        st.session_state['drawer'].set_canvas(st.session_state['canvas_image'])    

    def _switch_to_canvas(self) -> None:
        st.session_state['app_state'] = AppStatesEnum.canvas_render_state

    def _switch_to_initial(self) -> None:
        st.session_state['app_state'] = AppStatesEnum.initial_render_state
    
    def _tool_format_func(self, option) -> str:
        format_dict = {
            ToolsEnum.first_order_line: 'First order line ―',
            ToolsEnum.second_order_line: 'Second order line ⌒',
            ToolsEnum.parametric_line: 'Parametric line ⟡',
            ToolsEnum.transforming: 'Transforming tool ⌗'
        }
        return format_dict[option]
    
    def _render_tool_algorithms(self, tool_col_placeholder) -> None:
        algorithms = {
            ToolsEnum.first_order_line: FirstOrderLineAlgorithmsEnum.to_list(),
            ToolsEnum.second_order_line: SecondOrderLineAlgorithmsEnum.to_list(),
            ToolsEnum.parametric_line: ParametricLinesAlgorithmsEnum.to_list(),
            ToolsEnum.transforming: ['Kiya!']
        }
        with tool_col_placeholder:
            algorithm_selector = st.selectbox(
                label='Type',
                key='tool_algorithm',
                options=algorithms[st.session_state.get('tool_selector')],
                index=0,
                format_func=self._tool_algorithm_format_func
            )

            if st.session_state.get('tool_selector') == ToolsEnum.parametric_line:
                st.number_input(label='Choose number of control points',
                                min_value=4,
                                key='cpoints_amount_selector')
    
    def _tool_algorithm_format_func(self, option) -> str:
        format_dict = {
            FirstOrderLineAlgorithmsEnum.dda: 'Digital Differential Analyzer',
            FirstOrderLineAlgorithmsEnum.bresenham: 'Bresenham\'s algorithm',
            FirstOrderLineAlgorithmsEnum.wu: 'Wu\'s algorithm',
            FirstOrderLineAlgorithmsEnum.guptasproull: 'Gupta-Sproull algorithm',

            SecondOrderLineAlgorithmsEnum.circumference: 'Circumference',
            SecondOrderLineAlgorithmsEnum.ellipse: 'Ellipse',
            SecondOrderLineAlgorithmsEnum.hyperbola: 'Hyperbola',
            SecondOrderLineAlgorithmsEnum.parabola: 'Parabola',

            ParametricLinesAlgorithmsEnum.hermit: 'Hermite shape',
            ParametricLinesAlgorithmsEnum.bezier: 'Bezier\'s curve',
            ParametricLinesAlgorithmsEnum.bspline: 'B-Spline',
            
        }
        return format_dict.get(option, 'Kiya!')

    def _handle_canvas_click(self, coords) -> None:
        if st.session_state.get('points_list') is None:
            st.session_state['points_list'] = []
            return                
        st.session_state['points_list'].append(Point(
            coords['x'], coords['y']
        ))
        self._handle_shape_drawing()                        
    
    def _handle_shape_drawing(self) -> None:
        # Handling only first and second order lines        
        enough_point_to_draw = {
            ToolsEnum.first_order_line: {
                FirstOrderLineAlgorithmsEnum.dda: 2,
                FirstOrderLineAlgorithmsEnum.bresenham: 2,
                FirstOrderLineAlgorithmsEnum.wu: 2,
                FirstOrderLineAlgorithmsEnum.guptasproull: 2
            },

            ToolsEnum.second_order_line: {
                SecondOrderLineAlgorithmsEnum.circumference: 2,
                SecondOrderLineAlgorithmsEnum.ellipse: 2,
                SecondOrderLineAlgorithmsEnum.hyperbola: 3,
                SecondOrderLineAlgorithmsEnum.parabola: 2
            } 
        }
        # If parametric line tool is chosen, this block will work
        if st.session_state.get('cpoints_amount_selector'):
            parametric_curve_cpoints = st.session_state.get('cpoints_amount_selector')
            enough_point_to_draw[ToolsEnum.parametric_line] = {
                ParametricLinesAlgorithmsEnum.bezier: parametric_curve_cpoints
            }
        
        tool = st.session_state.get('tool_selector')
        algorithm = st.session_state.get('tool_algorithm')        
        if (len(st.session_state.get('points_list')) ==
            enough_point_to_draw[tool][algorithm]):
            points = st.session_state['points_list']            
            st.session_state['drawer'].draw_shape(
                tool=tool,
                algorithm=algorithm,
                points=points,
                color=st.session_state.get('color_selector', '#000000'),
                alpha=255
            )
            st.session_state['points_list'] = None                        
            st.rerun()                 


view = GraphicsRedactorView()
view.run()
