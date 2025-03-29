from ui.render_2D import *

"Тестовая функция"
def f(x, y):
    return 0.2 * (x**2 - y**2)

grid = generate_points(f, (-2, 2), (-2, 2), 0.3)
triangles = build_triangles_from_grid(grid)

render_mesh(triangles)
