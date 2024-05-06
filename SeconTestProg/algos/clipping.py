import numpy as np
from typing import Iterable
from numbers import Number
from fractions import Fraction


class Clipping:

    @classmethod
    def ccw(cls, prev: Iterable[Number], cur: Iterable[Number], next: Iterable[Number]):
        dx1 = cur[0] - prev[0]
        dx2 = next[0] - cur[0]
        dy1 = cur[1] - prev[1]
        dy2 = next[1] - cur[1]

        prod = dx1 * dy2 - dx2 * dy1
        if prod == 0:
            return prod, 0
        elif prod < 0:
            return prod, -1
        else:
            return prod, 1
    
    @classmethod
    def is_convex(cls, verts: Iterable[Iterable[Number]]) -> bool:
        print('Проверка многоугольника на выпуклость')
        signs = []
        for ind, vert in enumerate(verts):
            print('-'*30)
            cur = vert
            prev = verts[(ind - 1) % len(verts)]
            next = verts[(ind + 1) % len(verts)]
            print(f'Проверка векторов, образованных точками: {prev}-{cur} и {cur}-{next}')
            ccw = cls.ccw(prev, cur, next)
            signs.append(ccw[1])
            sense = {
                0: 'нулевой',
                1: 'положительный',
                -1: 'отрицательный'
            }
            print(f'Произведение векторов равно: {ccw[0]}k')
            print(f'Знак произведения веторов: {sense[ccw[1]]}')
            print('-'*30)
        result = set(signs)
        if len(result) > 1:
            print('Полигон вогнутый, среди векторых произведений присутствуют разные знаки')
            return False
        elif max(result) == 0:
            print('Все знаки произведений равны нулю, вектор вырождается в отрезок')
            return False
        elif max(result) == 1:
            print('Полигон выпуклый, внутренние нормали ориентированы влево от его контура')
            return True
        elif max(result) == -1:
            print('Полигон выпуклый, внутренние нормали ориентированы вправо от его контура')
            return True
        
    @classmethod
    def inner_normals(cls, verts: Iterable[Iterable[Number]]) -> Iterable[Iterable[Number]]:
        print('Поиск внутренних нормалей вектора')
        inner_normals: list[tuple[Number]] = []
        for ind, vert in enumerate(verts):
            cur = vert
            next = verts[(ind + 1) % len(verts)]
            nnext = verts[(ind + 2) % len(verts)]
            nx = -(next[1] - cur[1])
            ny = next[0] - cur[0]
            n_sign = np.sign(nx * (nnext[0] - cur[0]) + ny * (nnext[1] - cur[1]))
            print('-'*30)
            print(f'Нормаль для ребра из вершин: {(cur, next)}')
            if n_sign == -1:
                print(f'Получившаяся нормаль: {(nx, ny)}, обращена вне полигона')
                nx, ny = -nx, -ny
                print(f'После обращения внутрь: {(nx, ny)}')
            else:
                print(f'Получившаяся нормаль: {(nx, ny)}, обращена внутрь полигона')
            inner_normals.append((nx, ny))
            print('-'*30)
        return inner_normals
    
    @classmethod
    def cyrus_beck(cls, verts: Iterable[Iterable[Number]],
                   line: Iterable[Iterable[Number]]) -> tuple[Iterable[Number]]:
        
        def dot(p0, p1) -> Number:
            return p0[0] * p1[0] + p0[1] * p1[1]
        
        n = len(verts)
        d = (line[1][0] - line[0][0], line[1][1] - line[0][1])
        edges = [(verts[i], verts[(i + 1) % n]) for i in range(n)]
        print(f'Рёбра многоугольника: {edges}')
        params: dict[tuple[Number, Number], Number] = {}
        nums: dict[tuple[Number, Number], Number] = {}
        dens: dict[tuple[Number, Number], Number] = {}
        for ind, edge in enumerate(edges):
            print('-'*30)
            print(f'Рассматриваемое ребро: {edge}')
            f = edge[0]
            n = (-(edge[1][1] - edge[0][1]), edge[1][0] - edge[0][0])
            print(f'Нормаль: {n}')
            w = (line[0][0] - f[0], line[0][1] - f[1])
            den = dot(d, n)
            num = dot(w, n)
            if den == 0:
                print('Отрезок параллелен ребру/выродился в точку, найти параметр t невозможно')
            else:
                sign = np.sign(num / den)
                t = Fraction(f'{'-' if sign == -1 else ''}{abs(num)}/{abs(den)}') * (-1)
                print(f'Для данного отрезка параметр t равен {t}')
                params[edge] = t
                nums[edge] = num
                dens[edge] = den
        
        if not any([0 <= t <= 1 for t in params.values()]):
            if (all([num < 0 for num in nums.values()]) and 
                all([(num + den) < 0 for num, den in zip(nums.values(), dens.values())])):
                print('Отрезок отсекается тривиально, он полностью невидим')
                return None
            elif (all([num > 0 for num in nums.values()]) and 
                  all([(num + den) > 0 for num, den in zip(nums.values(), dens.values())])):
                print('Отрезок изображается тривиально, он полностью видимый')
                return line
        else:
            t_sups = [params[edge] for edge in params if dens[edge] < 0]
            t_infs = [params[edge] for edge in params if dens[edge] > 0]
            print(f'Потенциальные верхние пределы: {t_sups}')
            print(f'Потенциальные нижние пределы: {t_infs}')
            t_sup = min(t_sups)
            t_inf = max(t_infs)

            print(f'Выбранный верхний предел: {t_sup}')
            print(f'Выбранный нижний предел: {t_inf}')

            if t_sup < t_inf:
                print('Верхний предел меньше нижнего, отрезок невидим!')
                return None
            else:
                new_pair = [(line[0][0] + d[0] * t_inf, line[0][1] + d[1] * t_inf), 
                            (line[0][0] + d[0] * t_sup, line[0][1] + d[1] * t_sup)]
                print(f'Отрезок частично виден, видимая часть отрезка: {new_pair}')
                return new_pair

    @classmethod
    def cohen_sutherland(cls, b_points: Iterable[Iterable[Number]],
                         line: Iterable[Iterable[Number]]):
        
        INSIDE = 0
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8

        x_min = b_points[0][0]
        y_min = b_points[0][1]

        x_max = b_points[1][0]
        y_max = b_points[1][1]
        
        x1, y1 = line[0]
        x2, y2 = line[1]

        def compute_code(p) -> int:            

            code = INSIDE         

            x = p[0]
            y = p[1]

            if x < x_min:
                code |= LEFT
            elif x > x_max:
                code |= RIGHT
            if y < y_min:
                code |= BOTTOM
            elif y > y_max:
                code |= TOP
            
            return code
        
        code1 = compute_code(line[0])
        code2 = compute_code(line[1])

        print(f'Код для первой точки линии: {code1:04b}')
        print(f'Код для второй точки линии: {code2:04b}')

        accept = False

        while True:

            if code1 == 0 and code2 == 0:
                print('Отсечённая линия лежит внутри окна')
                accept = True
                break
                
            elif (code1 & code2) != 0:
                print('Данный отрезок лежит вне окна')
                break

            else:
                print('-'*30)
                print('Отрезок нуждается в отсекании')
                x = 1
                y = 1

                if code1 != 0:
                    print('Начальная точка лежит вне окна!')
                    code_out = code1
                    op = (x1, y1)
                
                else:
                    print('Конечная точка лежит вне окна!')
                    code_out = code2
                    op = (x2, y2)
                
                # Find intersection point
                # using formulas y = y1 + slope * (x - x1),
                # x = x1 + (1 / slope) * (y - y1)
                if code_out & TOP:
                    # Point is above the clip rectangle
                    print(f'Рассматриваемая точка {op} выше окна')
                    x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                    y = y_max
                elif code_out & BOTTOM:
                    # Point is below the clip rectangle
                    print(f'Рассматриваемая точка {op} ниже окна')
                    x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                    y = y_min
                elif code_out & RIGHT:
                    # Point is to the right of the clip rectangle
                    print(f'Рассматриваемая точка {op} справа от окна')
                    y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                    x = x_max
                elif code_out & LEFT:
                    # Point is to the left of the clip rectangle
                    print(f'Рассматриваемая точка {op} слева от окна')
                    y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                    x = x_min
                
                # Now intersection point (x, y) is found
                # We replace point outside clipping rectangle
                # by intersection point
                if code_out == code1:
                    x1 = x
                    y1 = y
                    code1 = compute_code((x1, y1))
                    print(f'Новая начальная точка: {(x1, y1)}')
                else:
                    x2 = x
                    y2 = y
                    code2 = compute_code((x2, y2))
                    print(f'Новая конечная точка: {(x2, y2)}')
                
                print('-'*30)

        if accept:
            print(f'Линия отсечена, новые точки: {(x1, y1)}, {(x2, y2)}')
            return [(x1, y1), (x2, y2)]
        else:
            print('Линия лежит вне пределов окна')
                
