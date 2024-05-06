from algos.transformation import Transformation
from algos.clipping import Clipping
from algos.roberts import Roberts
import numpy as np


points = [[1, 4], [4, 4], [4, 1], [1, 1]]
transfromations = ['m (-2.5 -2.5)', 'r 90', 's (4/3 2/3)', 'm (8 4)']

print(Transformation.complex_transform2d(points, transfromations))

verts = [[1, 4], [4, 4], [4, 1], [1, 1]]
is_convex = Clipping.is_convex(verts)
print(f'Внутренние нормали: {Clipping.inner_normals(verts)}')

verts2 = [(2, 3), (4, 5), (7, 2), (4, 1)]
line = [(2, 1), (6, 5)]
print(f'Видимая часть отрезка: {Clipping.cyrus_beck(verts2, line)}')

# Пример входных данных: массив массивов граней 3D
faces = [
    [(0, 0, 0), (0, 2, 0), (0, 0, 2)],
    [(0, 0, 0), (0, 2, 0), (2, 0, 0)],
    [(0, 0, 0), (0, 0, 2), (2, 0, 0)],
    [(0, 2, 0), (0, 0, 2), (2, 0, 0)],
]

faces_matrix = Roberts.generate_faces_matrix(faces)
V = faces_matrix.T
print("Матрица граней объекта:")
print(V)
P = np.array([0,0,1,0])
result = np.dot(P, V)

for index, element in enumerate(result):
    print(f'Граней {index+1}: {element}')


verts3 = [(1, 2), (6, 5)]
l1 = [(4, 6), (7, 3)]
l2 = [(0, 0), (7, 1)]
Clipping.cohen_sutherland(verts3, l1)
