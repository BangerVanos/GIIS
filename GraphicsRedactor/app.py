import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates as img_coords
from PIL import Image as img
from src.app_enums import AppStates, Tools


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
                value=640
            )
            height_input = st.number_input(
                label='Image height',
                min_value=10,
                key='image_height_input',
                value=480   
            )        
            st.button('Canvas test', key='new_canvas_btn',
                    on_click=self._new_canvas)

    def _render_canvas(self) -> None:               
        with self._placeholder.container(border=False):
            tool_col, canvas_col = st.columns([2, 9])
            with tool_col:
                tool_select = st.radio(
                    label='Select tool',
                    options=[
                        Tools.first_order_line,
                        Tools.second_order_line,
                        Tools.parametric_line,
                        Tools.transforming
                    ],
                    format_func=self._tool_format_func
                )
            with canvas_col:                
                click_coords = img_coords(
                    st.session_state['canvas_image'],
                    key='img_coords'    
                )
                st.write(click_coords)               

    def _render_load(self) -> None:
        pass

    def _render_save(self) -> None:
        pass

    def _new_canvas(self) -> None:
        width = st.session_state.get('image_width_input')
        height = st.session_state.get('image_height_input')
        st.session_state['canvas_image'] = img.new('RGB', (width, height), color='white')
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


view = GraphicsRedactorView()
view.run()
