from math import sin, cos, radians
import numpy as np
from numbers import Number
from enum import StrEnum
from typing import Iterable
from fractions import Fraction


class TransformationType:
    rotate: str = 'r'
    move: str = 'm'
    scale: str = 's'
    flipv: str = 'fv'
    fliph: str = 'fh'


class Transformation:

    @classmethod
    def move(cls, dx: Number, dy: Number):
        return np.array(
            [
                [1, 0, 0],
                [0, 1, 0],
                [dx, dy, 1]
            ]
        )

    @classmethod
    def scale(cls, x: Number, y: Number):
        return np.array(
            [
                [x, 0, 0],
                [0, y, 0],
                [0, 0, 1]
            ]
        )
    
    @classmethod
    def rotate(cls, angle: Number):
        angle = np.deg2rad(float(angle))
        return np.array(
            [
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1]
            ]
        )
    
    @classmethod
    def fliph(cls):
        return np.array(
            [
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
            ]
        )
    
    @classmethod
    def flipv(cls):
        return np.array(
            [
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ]
        )    
    
    @classmethod
    def complex_transform2d(cls, points: Iterable[Iterable[Number] | tuple[Number, Number]],
                            transformations: Iterable[str], log: bool = True) -> dict:
        tr_matrix = np.eye(3)        
        for transfromation in transformations:
            parameters = transfromation.split(' ', maxsplit=1)
            tr_values = parameters[1].translate({ord('('): None, ord(')'): None, ord('{'): None,
                                                 ord('}'): None, ord('['): None, ord(']'): None})
            tr_values_num = list(map(Fraction, tr_values.split(' ')))
            if log:
                print('-'*30)
            if parameters[0] == TransformationType.rotate:
                tr = Transformation.rotate(*tr_values_num)
                tr_matrix = tr_matrix @ tr
                if log:                    
                    print(f'Фигура повёрнута на угол: {tr_values_num} градусов')
                    print(f'Матрица поворота: {tr}')
            elif parameters[0] == TransformationType.move:
                tr = Transformation.move(*tr_values_num)
                tr_matrix = tr_matrix @ tr
                if log:
                    print(f'Фигура сдвинута на вектор: {tr_values_num}')
                    print(f'Матрица сдвига: {tr}')
            elif parameters[0] == TransformationType.scale:
                tr = Transformation.scale(*tr_values_num)
                tr_matrix = tr_matrix @ tr
                if log:
                    print(f'Фигура масштабирована в: {tr_values_num} раз')
                    print(f'Матрица масшиабирования: {tr}')
            elif parameters[0] == TransformationType.fliph:
                tr = tr_matrix @ Transformation.fliph()
                tr_matrix = tr
                if log:
                    print(f'Фигура отражена по горизонтали')
                    print(f'Матрица отражения: {tr}')
            elif parameters[0] == TransformationType.flipv:
                tr = Transformation.flipv()
                tr_matrix = tr_matrix @ Transformation.flipv()
                if log:
                    print(f'Фигура отражена по вертикали')
                    print(f'Матрица отражения: {tr}')
            if log:
                print(f'Итоговая матрица преобразования: {tr_matrix}')
                print('-'*30)        
        new_points = np.append(np.array(points), np.ones((len(points), 1)), axis=1) @ tr_matrix
        new_points = new_points[:, [0, 1]]        
        return {
            'old_points': points,
            'tr_matrix': tr_matrix.tolist(),
            'new_points': new_points.tolist()
        }
