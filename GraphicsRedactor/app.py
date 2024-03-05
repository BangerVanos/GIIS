import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates as img_coords
from PIL import Image as img
from src.app_enums import AppStates, Tools
from src.app_enums import (FirstOrderLineAlgorithms,
                           SecondOrderLineAlgorithms,
                           ParametricLinesAlgorithms)
from src.first_order_lines.first_order_lines import FirstOrderLine


class GraphicsRedactorView:
    
    def __init__(self) -> None:
        st.set_page_config('Graphics Redactor', layout='wide')
        if st.session_state.get('app_state') is None:
            st.session_state['app_state'] = AppStates.initial_render_state
        
        self._state_render_funcs = {
            AppStates.initial_render_state: self._render_initial,
            AppStates.canvas_render_state: self._render_canvas,
            AppStates.load_file_state: self._render_load,
            AppStates.save_file_state: self._render_save,
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
            st.button('Canvas test', key='new_canvas_btn',
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
                        Tools.first_order_line,
                        Tools.second_order_line,
                        Tools.parametric_line,
                        Tools.transforming
                    ],
                    format_func=self._tool_format_func,
                    key='tool_selector'
                )
                if tool_select:
                    self._render_tool_algorithms(tool_col)
            with canvas_col:                
                click_coords = img_coords(
                    st.session_state['canvas_image'],
                    key='img_coords'    
                )
                st.write(click_coords)
                new_img_col, save_img_col, debug_col, blank_col = st.columns([1, 1, 1, 10], gap='small')
                with new_img_col:
                    st.button(label='New image', use_container_width=True)
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
        self._switch_to_canvas()

    def _switch_to_canvas(self) -> None:
        st.session_state['app_state'] = AppStates.canvas_render_state

    def _switch_to_initial(self) -> None:
        st.session_state['app_state'] = AppStates.initial_render_state
    
    def _tool_format_func(self, option) -> str:
        format_dict = {
            Tools.first_order_line: 'First order line ―',
            Tools.second_order_line: 'Second order line ⌒',
            Tools.parametric_line: 'Parametric line ⟡',
            Tools.transforming: 'Transforming tool ⌗'
        }
        return format_dict[option]
    
    def _render_tool_algorithms(self, tool_col_placeholder) -> None:
        algorithms = {
            Tools.first_order_line: FirstOrderLineAlgorithms.to_list(),
            Tools.second_order_line: SecondOrderLineAlgorithms.to_list(),
            Tools.parametric_line: ParametricLinesAlgorithms.to_list(),
            Tools.transforming: ['Kiya!']
        }
        with tool_col_placeholder:
            algorithm_selector = st.selectbox(
                label='Type',
                key='tool_algorithm',
                options=algorithms[st.session_state.get('tool_selector')],
                index=0,
                format_func=self._tool_algorithm_format_func
            )
    
    def _tool_algorithm_format_func(self, option) -> str:
        format_dict = {
            FirstOrderLineAlgorithms.dda: 'Digital Differential Analyzer',
            FirstOrderLineAlgorithms.bresenham: 'Bresenham\'s algorithm',
            FirstOrderLineAlgorithms.wu: 'Wu\'s algorithm',
            FirstOrderLineAlgorithms.guptasproull: 'Gupta-Sproull algorithm',

            SecondOrderLineAlgorithms.circumference: 'Circumference',
            SecondOrderLineAlgorithms.ellipse: 'Ellipse',
            SecondOrderLineAlgorithms.hyperbola: 'Hyperbola',
            SecondOrderLineAlgorithms.parabola: 'Parabola',

            ParametricLinesAlgorithms.hermit: 'Hermite shape',
            ParametricLinesAlgorithms.bezier: 'Bezier\'s curve',
            ParametricLinesAlgorithms.bspline: 'B-Spline',
            
        }
        return format_dict.get(option, 'Kiya!')        


view = GraphicsRedactorView()
view.run()
