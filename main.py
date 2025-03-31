from ui.render_3D import *
import math

"Тестовая функция"
def f(x, y):
    return 0.2 * (x**4 - y**2)

grid = generate_points(f, (-2, 2), (-2, 2), 0.3)
triangles = build_triangles_from_grid(grid)
angle_z = math.radians(30)
angle_x = math.radians(45)
render_mesh(triangles, angle_z=angle_z, angle_x=angle_x)
