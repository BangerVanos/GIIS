import numpy as np


class Roberts:

    @classmethod
    def equation_plane(cls, points):
        x1, y1, z1 = points[0]
        x2, y2, z2 = points[1]
        x3, y3, z3 = points[2]
        a1 = x2 - x1
        b1 = y2 - y1
        c1 = z2 - z1
        a2 = x3 - x1
        b2 = y3 - y1
        c2 = z3 - z1
        a = b1 * c2 - b2 * c1
        b = a2 * c1 - a1 * c2
        c = a1 * b2 - b1 * a2
        d = (- a * x1 - b * y1 - c * z1)

        return a, b, c, d

    @classmethod
    def generate_plane_equations(cls, faces):
        plane_equations = []
        for face in faces:
            points = np.array(face)
            plane_equation = cls.equation_plane(points)
            plane_equations.append(plane_equation)
        return plane_equations

    @classmethod
    def generate_faces_matrix(cls, faces):
        plane_equations = cls.generate_plane_equations(faces)
        return np.array(plane_equations)


