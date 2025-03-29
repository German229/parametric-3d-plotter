from geometry.vector3 import Vector3
from geometry.triangle import Triangle
import math
from typing import Callable, Tuple
def func(x, y):
    pass

def generate_points(f : Callable[[float, float], float],\
                    x_range : Tuple[float, float],\
                    y_range : Tuple[float, float],\
                    step : float) -> list[list[Vector3]]:
    """Строим Сетку точек Vector(x, y, z), точка Vector(x, y, z) лежит по обращению points[y][x]"""
    x_min, x_max = x_range
    y_min, y_max = y_range
    y_curr = y_min
    points = []
    while y_curr <= y_max:
        x_curr = x_min
        row = []
        while x_curr <= x_max:
            z = f(x_curr, y_curr)
            row.append(Vector3(x_curr, y_curr, z))
            x_curr += step
        points.append(row)
        y_curr += step
    return points


def build_triangles_from_grid(grid : list[list[Vector3]]) -> list[Triangle]:
    """Принимает 2D-сетку точек и возвращает список треугольников."""
    triangles = []
    rows = len(grid)
    cols = len(grid[0])

    for y in range(rows - 1):
        for x in range(cols - 1):
            p1 = grid[y][x]
            p2 = grid[y][x + 1]
            p3 = grid[y + 1][x]
            p4 = grid[y + 1][x + 1]

            triangles.append(Triangle(p1, p2, p3))
            triangles.append(Triangle(p2, p3, p4))

    return triangles

