import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates as img_coords
from enum import StrEnum
from PIL import Image as img


class AppStates(StrEnum):
    initial_render_state: str = 'initial'
    canvas_render_state: str = 'canvas'
    load_file_state: str = 'load'
    save_file_state: str = 'save'


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
        st.button('Canvas test', key='switch_to_canvas_btn',
                  on_click=self._switch_to_canvas)

    def _render_canvas(self) -> None:
        if st.session_state.get('canvas_image') is None:
            st.session_state['canvas_image'] = img.new('RGB', (1280, 720), color='white')
        with self._placeholder.container(border=False):
            tool_col, canvas_col = st.columns([1, 9])
            with tool_col:
                st.write('DDA')
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
        pass

    def _switch_to_canvas(self) -> None:
        st.session_state['app_state'] = AppStates.canvas_render_state

    def _switch_to_initial(self) -> None:
        st.session_state['app_state'] = AppStates.initial_render_state


view = GraphicsRedactorView()
view.run()
