from src.additional_math import Pixel, Point
from numbers import Number
from src.first_order_lines.first_order_lines import FirstOrderLine
from math import atan2, floor
from functools import cmp_to_key


class Polygon:

    @classmethod
    def simple_polygon(cls, c_points: list[Point], color: str = '#000000',
                       alpha: int = 255, **kwargs) -> list[Pixel]:
        c_points.append(c_points[0])

        px_list: list[Pixel] = []

        for i in range(len(c_points) - 1):
            cur_point = c_points[i]
            next_point = c_points[i + 1]

            px_list.extend(FirstOrderLine.bresenham(
                Point(cur_point.x, cur_point.y),
                Point(next_point.x, next_point.y),
                color, alpha
            ))
        
        if kwargs.get('fill'):
            fill_color = kwargs.get('fill_color')
            fill_color = ('#000000' if fill_color is None
                          else fill_color)
            px_list.extend(
                PolygonFill.general_fill(kwargs.get('fill_algorithm'),
                                         c_points, fill_color)
            )
        
        if kwargs.get('get_normals'):
            normals_color = kwargs.get('normals_color')
            normals_color = ('#0000FF' if normals_color
                             is None else normals_color)
            px_list.extend(
                PolygonProperty.normals(c_points, normals_color)
            )
        
        return px_list

    @classmethod
    def graham(cls, c_points: list[Point], color: str = '#000000',
               alpha: int = 255, **kwargs) -> list[Pixel]:
        
        # Finding anchor point
        anchor_point = c_points[0]
        for point in c_points:
            if point.y < anchor_point.y:
                anchor_point = point
            elif point.y == anchor_point.y and point.x < anchor_point.x:
                anchor_point = point
        
        # Polar angle
        def polar_angle(point_1: Point, point_2: Point):
            y_span = point_1.y - point_2.y
            x_span = point_1.x - point_2.x

            return atan2(y_span, x_span)
        
        # Compare points condition for sort
        def sort_condition(point_1: Point, point_2: Point):
            polar_ang1 = polar_angle(anchor_point, point_1)
            polar_ang2 = polar_angle(anchor_point, point_2)
            if polar_ang1 < polar_ang2:
                return -1
            elif polar_ang1 > polar_ang2:
                return 1
            else:
                dist_1 = point_1.distance(anchor_point)
                dist_2 = point_2.distance(anchor_point)

                if dist_1 < dist_2:
                    return -1
                elif dist_1 > dist_2:
                    return 1

            return 0

        # Sorting control points
        c_points.sort(key=cmp_to_key(sort_condition))

        convex_hull_points: list[Point] = [anchor_point, c_points[0]]

        for point in c_points[1:]:
            while not PolygonProperty.rotation(convex_hull_points[-2],
                                                    convex_hull_points[-1],
                                                    point) == 1:
                convex_hull_points.pop()
            convex_hull_points.append(point)        

        px_list: list[Pixel] = []

        for i in range(len(convex_hull_points) - 1):
            cur_point = convex_hull_points[i]
            next_point = convex_hull_points[i + 1]

            px_list.extend(FirstOrderLine.bresenham(
                Point(cur_point.x, cur_point.y),
                Point(next_point.x, next_point.y),
                color, alpha
            ))
        
        if kwargs.get('fill'):
            fill_color = kwargs.get('fill_color')
            fill_color = ('#000000' if fill_color is None
                          else fill_color)
            px_list.extend(
                PolygonFill.general_fill(kwargs.get('fill_algorithm'),
                                         convex_hull_points, fill_color)
            )

        if kwargs.get('get_normals'):
            normals_color = kwargs.get('normals_color')
            normals_color = ('#0000FF' if normals_color
                             is None else normals_color)
            px_list.extend(
                PolygonProperty.normals(convex_hull_points, normals_color)
            )

        return px_list

    @classmethod
    def jarvis(cls, c_points: list[Point], color: str = '#000000',
               alpha: int = 255, **kwargs) -> list[Pixel]:
        
        n = len(c_points)
        
        # Finding anchor point index
        anchor_point_ind = 0
        for i in range(1, n):
            if c_points[i].x < c_points[anchor_point_ind].x:
                anchor_point_ind = i
            elif (c_points[i].x == c_points[anchor_point_ind].x
                  and c_points[i].y < c_points[anchor_point_ind].y):
                anchor_point_ind = i
        
        p = anchor_point_ind
        convex_hull_points: list[Point] = []
        convex_hull_points.append(c_points[p])        

        while(True):
            
            q = (p + 1) % n

            for i in range(n):
                if i == p:
                    continue
                rot = PolygonProperty.rotation(c_points[p],
                                               c_points[i],
                                               c_points[q])
                if rot == 1 or (rot == 0 and c_points[p].distance(c_points[i]) > 
                                c_points[p].distance(c_points[q])):
                    q = i
            
            p = q

            if p == anchor_point_ind:
                break
            convex_hull_points.append(c_points[q])
        
        convex_hull_points.append(convex_hull_points[0])
        
        px_list: list[Pixel] = []

        for i in range(len(convex_hull_points) - 1):
            cur_point = convex_hull_points[i]
            next_point = convex_hull_points[i + 1]

            px_list.extend(FirstOrderLine.bresenham(
                Point(cur_point.x, cur_point.y),
                Point(next_point.x, next_point.y),
                color, alpha
            ))
        
        if kwargs.get('fill'):
            fill_color = kwargs.get('fill_color')
            fill_color = ('#000000' if fill_color is None
                          else fill_color)
            px_list.extend(
                PolygonFill.general_fill(kwargs.get('fill_algorithm'),
                                         convex_hull_points, fill_color)
            )

        if kwargs.get('get_normals'):
            normals_color = kwargs.get('normals_color')
            normals_color = ('#0000FF' if normals_color
                             is None else normals_color)
            px_list.extend(
                PolygonProperty.normals(convex_hull_points, normals_color)
            )

        return px_list


class PolygonProperty:

    @classmethod
    def is_convex(cls, c_points: list[Point]) -> bool:
        for i in range(1, len(c_points) - 1):
            if cls.rotation(c_points[i - 1],
                            c_points[i],
                            c_points[i + 1]) == -1:
                return False
        return True

    @classmethod
    def normals(cls, c_points: list[Point], color: str = '#0000FF',
                alpha: int = 255, **kwargs) -> list[Pixel]:
        
        px_list: list[Pixel] = []

        for i in range(len(c_points) - 1):
            cur_point = c_points[i]
            next_point = c_points[i + 1]

            normal_x = next_point.y - cur_point.y
            normal_y = cur_point.x - next_point.x

            normal_dist = Point(normal_x, normal_y).distance(Point(0, 0))

            normalized_x = normal_x / normal_dist
            normalized_y = normal_y / normal_dist

            start_x = int((cur_point.x + next_point.x) // 2 + normalized_x * 50)
            start_y = int((cur_point.y + next_point.y) // 2 + normalized_y * 50)

            end_x = int((cur_point.x + next_point.x) // 2 - normalized_x * 50)
            end_y = int((cur_point.y + next_point.y) // 2 - normalized_y * 50)

            px_list.extend(FirstOrderLine.bresenham(
                Point(start_x, start_y), Point(end_x, end_y),
                color, alpha
            ))
        
        return px_list

    @classmethod
    def rotation(cls, prev_point, cur_point: Point, next_point: Point) -> bool:
        ux = cur_point.x - prev_point.x
        uy = cur_point.y - prev_point.y

        vx = next_point.x - cur_point.x
        vy = next_point.y - cur_point.y

        mul = ux * vy - uy * vx

        if mul == 0:
            # collinear
            return 0
        elif mul < 0:
            # counter-clockwise
            return -1
        elif mul > 0:
            # clockwise
            return 1
    
    @classmethod
    def is_point_in_polygon(cls, point: Point, polygon_points: list[Point]) -> bool:

        x_max = max([point.x for point in polygon_points])
        y_max = max([point.y for point in polygon_points])
        x_min = min([point.x for point in polygon_points])
        y_min = min([point.y for point in polygon_points])

        if not (x_min < point.x < x_max and y_min < point.y < y_max):
            return False

        intersections = 0

        x, y = point.x, point.y

        for i in range(len(polygon_points) - 1):
            point_1 = polygon_points[i]
            point_2 = polygon_points[i + 1]

            p1x, p1y = point_1.x, point_1.y
            p2x, p2y = point_2.x, point_2.y

            if y < p1y == y < p2y:
                continue

            if x < (p2x - p1x) * (y - p1y) / (p2y - p1y) + p1x:
                intersections += 1
        
        return intersections % 2 == 1
    
    @classmethod
    def find_line_polygon_intersections(cls, line_start: Point, line_end: Point,
                                        polygon_points: list[Point]) -> list[Point]:
        
        def segment_intersection(l1s: Point, l1e: Point,
                                 l2s: Point, l2e: Point) -> Point | None:
            if cls.rotation(l1s, l1e, l2e) == 0 or cls.rotation(l1s, l1e, l2s) == 0:
                return None            

            dl1 = l1e - l1s
            dl2 = l2e - l2s                       

            dly = l2s.y - l1s.y
            dlx = l2s.x - l1s.x

            divider = (dl2.x * dl1.y - dl2.y * dl1.x)
            if divider == 0:
                return None

            a = (dl2.x * dly - dl2.y * dlx) / divider
            b = (dl1.x * dly - dl1.y * dlx) / divider

            if 0 < a < 1 and 0 < b < 1:
                x = int(l1s.x + a * dl1.x)
                y = int(l1s.y + a * dl1.y)
                return Point(x, y)
            return None
                                   
        
        inter_list: list[Point] = []
        temp_dict: dict[str, Point] = {}
        
        for i in range(len(polygon_points) - 1):
            pol_1 = polygon_points[i]
            pol_2 = polygon_points[i + 1]

            min_y = min(pol_1.y, pol_2.y)
            max_y = max(pol_1.y, pol_2.y)

            
            inter_point = segment_intersection(line_start, line_end,
                                               pol_1, pol_2)            
            if inter_point:                                
                if not temp_dict.get(f'{inter_point.x}-{inter_point.y}'):
                    inter_list.append(inter_point)
                elif (inter_point.y == min_y) or (inter_point.y == max_y):                                        
                    inter_list.append(inter_point)                                                                      
                temp_dict[f'{inter_point.x}-{inter_point.y}'] = inter_point                        
        return sorted(inter_list, key=lambda p: p.x)


class PolygonFill:

    @classmethod
    def general_fill(cls, algorithm: str, polygon_points: list[Point],
                     fill_color: str = '#000000',
                     alpha: int = 255) -> list[Pixel]:
        FILL_ALGORITHMS = {
            'scan_line_simple': cls.simple_scan_lines_fill,
            'scan_line': cls.scan_lines_fill,
            'floodfill_simple': cls.simple_floodfill,
            'floodfill_scan': cls.scanline_floodfill
        }
        return FILL_ALGORITHMS[algorithm](polygon_points, fill_color, alpha)
    
    @classmethod
    def simple_scan_lines_fill(cls, polygon_points: list[Point],
                               fill_color: str = '#000000',
                               alpha: int = 255) -> list[Pixel]:
        x_s = [point.x for point in polygon_points]
        y_s = [point.y for point in polygon_points]

        x_min = min(x_s)
        x_max = max(x_s)

        y_min = min(y_s)
        y_max = max(y_s)    

        px_list: list[Pixel] = []
        inter_points: list[Point] = []        

        for y in range(y_min + 1, y_max):
            points = PolygonProperty.find_line_polygon_intersections(
                Point(x_min, y), Point(x_max, y), polygon_points
            )
            if len(points) > 1:
                inter_points.extend(points)            

        def sort_condition(point_1: Point, point_2: Point):
            if (point_1.y < point_2.y or
                (point_1.y == point_2.y and point_1.x <= point_2.x)):
                return -1
            elif (point_2.y < point_1.y or
                (point_2.y == point_1.y and point_2.x <= point_1.x)):
                return 1
            else:
                return 0
        
        inter_points.sort(key=cmp_to_key(sort_condition))
        
        for i in range(0, len(inter_points) - 1, 2):
            point_1 = inter_points[i]
            point_2 = inter_points[i + 1]                       
            px_list.extend(
                FirstOrderLine.bresenham(
                    point_1 + Point(1, 0), point_2 - Point(1, 0), fill_color,
                    alpha
                )
            )
        return px_list
    
    @classmethod
    def scan_lines_fill(cls, polygon_points: list[Point],
                        fill_color: str = '#000000',
                        alpha: int = 255) -> list[Pixel]:
        '''Reference: https://www.educative.io/answers/what-is-scanline-fill-algorithm'''    
        
        y_s = [point.y for point in polygon_points]
        y_min = min(y_s)
        y_max = max(y_s)
                
        edges: list[tuple[Point, Point, dict]] = [(p1 := polygon_points[i], p2 := polygon_points[i + 1],
                                                  {'y_min': min(p1.y, p2.y),
                                                   'y_max': max(p1.y, p2.y),
                                                   'x': p1.x if p1.y < p2.y else p2.x,
                                                   'in_slope': (p2.x - p1.x) / (p2.y - p1.y)})
                                                   for i in range(len(polygon_points) - 1)]
        edges.sort(key=lambda item: item[2]['y_min'])
        active_edges: list[tuple[Point, Point, dict]] = []                

        def move_edges(y: Number, edges, active_edges):
            new_edges = []            
            for edge in edges:
                if not (edge[2]['y_min'] == y):
                    new_edges.append(edge)
                else:
                    active_edges.append(edge)           
            return new_edges, active_edges            
        
        def move_active_edges(y: Number, active_edges):
            new_active_edges = []
            for active_edge in active_edges:
                if not (active_edge[2]['y_max'] == y):                    
                    new_active_edges.append(active_edge)
            return new_active_edges
        
        def update_active_x(active_edges):            
            for active_edge in active_edges:
                active_edge[2]['x'] = (active_edge[2]['x'] + 
                                       active_edge[2]['in_slope'])
            return active_edges

        
        px_list: list[Pixel] = []
        
        y = y_min                
        while len(edges) > 0 or len(active_edges) > 0:            
            edges, active_edges = move_edges(y, edges, active_edges)                        
            active_edges.sort(key=lambda item: item[2]['x'])                        
            for i in range(len(active_edges) - 1):
                px_list.extend(
                    FirstOrderLine.bresenham(
                        Point(int(active_edges[i][2]['x']), y),
                        Point(int(active_edges[i + 1][2]['x']), y),
                        fill_color, alpha
                    )
                )
            y += 1
            active_edges = move_active_edges(y, active_edges)
            active_edges = update_active_x(active_edges)                                
                
        return px_list
    
    @classmethod
    def simple_floodfill(cls, polygon_points: list[Point],
                         fill_color: str = '#000000',
                         alpha: int = 255) -> list[Pixel]:
        centroid: Point = Point(
            sum([point.x for point in polygon_points[:-1]]) 
            // (len(polygon_points) - 1),
            sum([point.y for point in polygon_points[:-1]])
            // (len(polygon_points) - 1)
        )        

        point_stack: list[Point] = []
        point_stack.insert(0, centroid)
        painted: list[Point] = []

        px_list: list[Pixel] = []

        def paint():
            pt = point_stack.pop()
            painted.append(pt)
            px_list.append(
                Pixel(pt, fill_color, alpha)
            )
            handle_neighbours(pt)

        def handle_neighbours(pt: Point):
            neighbours: tuple = (
                Point(pt.x + 1, pt.y),
                Point(pt.x - 1, pt.y),
                Point(pt.x, pt.y + 1),
                Point(pt.x, pt.y - 1)
            )
            for n_pt in neighbours:                
                if (PolygonProperty.is_point_in_polygon(n_pt, polygon_points)
                    and n_pt not in painted):                    
                    point_stack.append(n_pt)
        
        while point_stack:
            paint()                       
        
        return px_list
    
    @classmethod
    def scanline_floodfill(cls, polygon_points: list[Point],
                           fill_color: str = '#000000',
                           alpha: int = 255) -> list[Pixel]:
        centroid: Point = Point(
            sum([point.x for point in polygon_points[:-1]]) 
            // (len(polygon_points) - 1),
            sum([point.y for point in polygon_points[:-1]])
            // (len(polygon_points) - 1)
        )

        stack: list[tuple] = []
        stack.append((centroid.x, centroid.x, centroid.y, 1))
        stack.append((centroid.x, centroid.x, centroid.y - 1, -1))

        px_list: list[Pixel] = []

        while stack:
            px_struct = stack.pop()
            x = px_struct[0]
            x1 = px_struct[0]
            x2 = px_struct[1]
            y = px_struct[2]
            dy = px_struct[3]
            if PolygonProperty.is_point_in_polygon(Point(x, y), polygon_points):
                while PolygonProperty.is_point_in_polygon(Point(x - 1, y),
                                                          polygon_points):
                    px_list.append(
                        Pixel(Point(x - 1, y), fill_color, alpha)
                    )
                    x -= 1
                if x < x1:
                    stack.append((x, x1 - 1, y - dy, -dy))
            while x1 <= x2:
                while PolygonProperty.is_point_in_polygon(
                    Point(x1, y), polygon_points
                ):
                    px_list.append(
                        Pixel(Point(x1, y), fill_color, alpha)
                    )
                    x1 += 1
                if x1 > x:
                    stack.append((x, x1 - 1, y + dy, dy))
                if x1 - 1 > x2:
                    stack.append((x2 + 1, x1 - 1, y - dy, -dy))
                x1 += 1
                while x1 < x2 and not PolygonProperty.is_point_in_polygon(
                    Point(x1, y), polygon_points
                ):
                    x1 += 1
                x = x1            
            if len(stack) > 100:
                break            
            
        return px_list
