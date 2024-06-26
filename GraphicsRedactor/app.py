import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates as img_coords
from PIL import Image as img
from src.app_enums import AppStatesEnum, ToolsEnum
from src.app_enums import (FirstOrderLineAlgorithmsEnum,
                           SecondOrderLineAlgorithmsEnum,
                           ParametricLinesAlgorithmsEnum,
                           TransformingAlgorithmsEnum,
                           PolygonAlgorithmsEnum,
                           PolygonFillAlgorithmsEnum,
                           DelanayVoronoiAlgorithmsEnum,
                           ClippingAlgorithmsEnum)
from src.graphics_redactor_backend_api import ShapeDrawer
from src.transforming import ImageTransformer
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
                    value='#000000',
                    help='Select color of your shapes'
                )                
                tool_select = st.radio(
                    label='Select tool',
                    options=ToolsEnum.to_list(),
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

                # Only drawing tools could accept canvas clicks
                if click_coords and tool_select != ToolsEnum.transforming:
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
        st.session_state['canvas_shapes'] = dict()
        st.session_state['drawer'] = ShapeDrawer(st.session_state['canvas_image'])
        st.session_state['transformer'] = ImageTransformer(st.session_state['canvas_image'],
                                                           self)
        st.session_state['points_list'] = None
        self._switch_to_canvas()

    def _clear_canvas(self) -> None:
        size = st.session_state['canvas_image'].size
        st.session_state['points_list'] = None
        st.session_state['canvas_image'] = img.new('RGB', size, color='white')
        st.session_state['canvas_shapes'] = dict()
        st.session_state['drawer'].set_canvas(st.session_state['canvas_image'])  
        st.session_state['transformer'].set_canvas(st.session_state['canvas_image'])

    def set_canvas(self, canvas: img.Image) -> None: 
        st.session_state['canvas_image'] = canvas
        st.session_state['drawer'].set_canvas(st.session_state['canvas_image'])  
        st.session_state['transformer'].set_canvas(st.session_state['canvas_image'])

    def _switch_to_canvas(self) -> None:
        st.session_state['app_state'] = AppStatesEnum.canvas_render_state

    def _switch_to_initial(self) -> None:
        st.session_state['app_state'] = AppStatesEnum.initial_render_state
    
    def _tool_format_func(self, option) -> str:
        format_dict = {
            ToolsEnum.first_order_line: 'First order line ―',
            ToolsEnum.second_order_line: 'Second order line ⌒',
            ToolsEnum.parametric_line: 'Parametric line ⟡',
            ToolsEnum.polygon: 'Polygon tool 🛑',
            ToolsEnum.transforming: 'Transforming tool ⌗',
            ToolsEnum.delanay_voronoi: 'Delanay & Voronoi',
            ToolsEnum.clipping: '2D Line Clipping'
        }
        return format_dict[option]
    
    def _render_tool_algorithms(self, tool_col_placeholder) -> None:
        algorithms = {
            ToolsEnum.first_order_line: FirstOrderLineAlgorithmsEnum.to_list(),
            ToolsEnum.second_order_line: SecondOrderLineAlgorithmsEnum.to_list(),
            ToolsEnum.parametric_line: ParametricLinesAlgorithmsEnum.to_list(),
            ToolsEnum.transforming: TransformingAlgorithmsEnum.to_list(),
            ToolsEnum.polygon: PolygonAlgorithmsEnum.to_list(),
            ToolsEnum.delanay_voronoi: DelanayVoronoiAlgorithmsEnum.to_list(),
            ToolsEnum.clipping: ClippingAlgorithmsEnum.to_list()
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
                self._render_parametric_line_parameters()
            elif (st.session_state.get('tool_selector') == ToolsEnum.transforming
                  and algorithm_selector):
                self._render_transforming_parameters(algorithm_selector)
            elif st.session_state.get('tool_selector') == ToolsEnum.polygon:
                self._render_polygon_parameters()
            elif st.session_state.get('tool_selector') == ToolsEnum.delanay_voronoi:
                self._render_delanay_voronoi_parameters()
            elif st.session_state.get('tool_selector') == ToolsEnum.clipping:
                self._render_clipping_parameters()
    
    def _render_parametric_line_parameters(self) -> None:
        st.number_input(label='Choose number of control points',
                                min_value=4,
                                key='cpoints_amount_selector')
        st.checkbox(label='Enclosed?',
                    key='parametric_enclosed')

    def _render_transforming_parameters(self, algorithm):
        if algorithm == TransformingAlgorithmsEnum.move:
            st.radio(label='Axis',
                     options=['x', 'y'],
                     key='move_axis',
                     horizontal=True)
            st.number_input(label='Pixels amount',
                            value=0,
                            key='move_amount')
        elif algorithm == TransformingAlgorithmsEnum.reflect:
            st.radio(label='Axis',
                     options=['x', 'y'],
                     key='reflect_axis',
                     horizontal=True)
        elif algorithm == TransformingAlgorithmsEnum.rotate:
            st.number_input(label='Degree',
                            value=0,
                            key='rotate_degree')
        elif algorithm == TransformingAlgorithmsEnum.scale:
            st.number_input(label='X Scale',
                            min_value=0.0,
                            value=1.0,
                            key='scale_x',
                            step=0.1)
            st.number_input(label='Y Scale',
                            min_value=0.0,
                            value=1.0,
                            key='scale_y',
                            step=0.1)
        st.button(label='Apply transform',
                  on_click=lambda: self._handle_transforming(algorithm))

    def _render_polygon_parameters(self) -> None:
        st.number_input(label='Choose number of control points',
                                min_value=3,
                                key='cpoints_amount_selector')
        get_normals = st.checkbox(label='Draw normals?',
                                  key='get_normals')
        if get_normals:
            st.color_picker(label='Normals color',
                            value='#0000FF',
                            key='normals_color')

        fill = st.checkbox(label='Fill polygon?',
                           key='fill')

        if fill:
            st.color_picker(label='Fill color',
                            value='#000000',
                            key='fill_color')
            st.selectbox(label='Select Fill algorithm',
                         key='fill_algorithm',
                         options=PolygonFillAlgorithmsEnum.to_list(),
                         format_func=self._tool_algorithm_format_func)

    def _render_delanay_voronoi_parameters(self) -> None:
        st.number_input(label='Choose number of control points',
                        min_value=3,
                        key='cpoints_amount_selector')

    def _render_clipping_parameters(self) -> None:
        st.number_input(label='Choose number of control points',
                        min_value=5,
                        key='cpoints_amount_selector',
                        help='Last 2 points are corners of bounding box.')              
    
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

            ParametricLinesAlgorithmsEnum.hermite: 'Hermite shape',
            ParametricLinesAlgorithmsEnum.bezier: 'Bezier\'s curve',
            ParametricLinesAlgorithmsEnum.bspline: 'Cubic B-Spline',

            TransformingAlgorithmsEnum.move: 'Move',
            TransformingAlgorithmsEnum.scale: 'Scale',
            TransformingAlgorithmsEnum.reflect: 'Reflection',
            TransformingAlgorithmsEnum.rotate: 'Rotation',

            PolygonAlgorithmsEnum.simple: 'Simple custom polygon',
            PolygonAlgorithmsEnum.graham: 'Graham convex hull',
            PolygonAlgorithmsEnum.jarvis: 'Jarvis convex hull',

            PolygonFillAlgorithmsEnum.scan_line_simple: 'Scan Line (no active edges)',
            PolygonFillAlgorithmsEnum.scan_line: 'Scan Line (with active edges)',
            PolygonFillAlgorithmsEnum.simple_floodfill: 'Simple Floodfill',
            PolygonFillAlgorithmsEnum.scan_floodfill: 'ScanLine Floodfill',

            DelanayVoronoiAlgorithmsEnum.delanay: 'Delanay Triangulation',
            DelanayVoronoiAlgorithmsEnum.voronoi: 'Voronoi Diagram',

            ClippingAlgorithmsEnum.cohen_sutherland: 'Cohen-Sutherland'
            
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

        tool = st.session_state.get('tool_selector')
        algorithm = st.session_state.get('tool_algorithm')

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
        # If parametric line or polygon or delanay-voronoi or clipping
        # tool is chosen, this block will work
        if st.session_state.get('cpoints_amount_selector'):

            c_points_amount = st.session_state.get('cpoints_amount_selector')

            if tool == ToolsEnum.parametric_line:            
                enough_point_to_draw[ToolsEnum.parametric_line] = {
                    ParametricLinesAlgorithmsEnum.bezier: c_points_amount,
                    ParametricLinesAlgorithmsEnum.bspline: c_points_amount,
                    ParametricLinesAlgorithmsEnum.hermite: c_points_amount
                }
            
            elif tool == ToolsEnum.polygon:
                enough_point_to_draw[ToolsEnum.polygon] = {
                    PolygonAlgorithmsEnum.simple: c_points_amount,
                    PolygonAlgorithmsEnum.graham: c_points_amount,
                    PolygonAlgorithmsEnum.jarvis: c_points_amount
                }
            
            elif tool == ToolsEnum.delanay_voronoi:
                enough_point_to_draw[ToolsEnum.delanay_voronoi] = {
                    DelanayVoronoiAlgorithmsEnum.delanay: c_points_amount,
                    DelanayVoronoiAlgorithmsEnum.voronoi: c_points_amount
                }
            
            elif tool == ToolsEnum.clipping:
                enough_point_to_draw[ToolsEnum.clipping] = {
                    ClippingAlgorithmsEnum.cohen_sutherland: c_points_amount                    
                }
        
                
        if (len(st.session_state.get('points_list')) ==
            enough_point_to_draw[tool][algorithm]):
            points = st.session_state['points_list']            
            self._send_right_data_to_drawer(tool, algorithm, points)
            st.session_state['points_list'] = None                        
            st.rerun()

    def _send_right_data_to_drawer(self, tool, algorithm, points):
        kwargs = {}
        if tool == ToolsEnum.parametric_line:
            kwargs['enclosed'] = st.session_state.get('parametric_enclosed')
        elif tool == ToolsEnum.polygon:
            kwargs['get_normals'] = st.session_state.get('get_normals')
            kwargs['normals_color'] = st.session_state.get('normals_color', '#0000FF')

            kwargs['fill'] = st.session_state.get('fill')
            kwargs['fill_color'] = st.session_state.get('fill_color', '#000000')
            kwargs['fill_algorithm'] = st.session_state.get('fill_algorithm')
        
        st.session_state['drawer'].draw_shape(
            tool=tool,
            algorithm=algorithm,
            points=points,
            color=st.session_state.get('color_selector', '#000000'),
            alpha=255,
            **kwargs
        )
    
    def _add_shape_to_shapes_dict(self, tool, algorithm, points):
        if st.session_state.get('canvas_shapes') is None:
            st.session_state['canvas_shapes'] = dict()
        shapes = list(st.session_state['canvas_shapes'].keys())
        common_shapes = [shape for shape in shapes
                         if shape.startswith(f'{tool}_')]
        last_common_shape_id = (0 if not common_shapes 
                                else max(list(map(lambda item: int(item.replace(f'{tool}_', '')),
                                                  common_shapes))))
        new_shape_id = last_common_shape_id + 1
    
    def _handle_transforming(self, algorithm):
        if algorithm == TransformingAlgorithmsEnum.move:
            st.session_state.get('transformer').move(
                st.session_state.get('move_axis'),
                st.session_state.get('move_amount')
            )
        elif algorithm == TransformingAlgorithmsEnum.reflect:
            st.session_state.get('transformer').reflect(
                st.session_state.get('reflect_axis')                
            )
        elif algorithm == TransformingAlgorithmsEnum.rotate:
            st.session_state.get('transformer').rotate(
                st.session_state.get('rotate_degree')
            )
        elif algorithm == TransformingAlgorithmsEnum.scale:
            st.session_state.get('transformer').scale(
                st.session_state.get('scale_x'),
                st.session_state.get('scale_y')
            )
        

view = GraphicsRedactorView()
view.run()
