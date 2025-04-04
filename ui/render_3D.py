import tkinter as tk
from geometry.vector3 import Vector3
from geometry.triangle import Triangle
from engine.mesh_builder import generate_points, build_triangles_from_grid
from typing import Callable, Tuple


def project_point(v: Vector3, scale=100, offset_x=400, offset_y=300) -> tuple:
    return (v.x * scale + offset_x, -v.y * scale + offset_y)

def draw_triangle(canvas, triangle : Triangle, light_dir=Vector3(0, 0, 1)) -> None:
    a2d = project_point(triangle.a)
    b2d = project_point(triangle.b)
    c2d = project_point(triangle.c)

    ab = triangle.b - triangle.a
    ac = triangle.c - triangle.a
    normal = ab.cross(ac).normalize()

    light_dir = light_dir.normalize()
    intensity = max(0, normal.dot(light_dir))

    gray = int(255 * intensity)
    color = f'#{gray:02x}{gray:02x}{gray:02x}'

    canvas.create_polygon(a2d, b2d, c2d, fill=color, outline=color)


def draw_axes(canvas, scale=100, offset_x=400, offset_y=300) -> None:
    origin = Vector3(0, 0, 0)
    x_axis = Vector3(1, 0, 0)
    y_axis = Vector3(0, 1, 0)
    z_axis = Vector3(0, 0, 1)

    a = project_point(origin, scale, offset_x, offset_y)
    x = project_point(x_axis, scale, offset_x, offset_y)
    y = project_point(y_axis, scale, offset_x, offset_y)
    z = project_point(z_axis, scale, offset_x, offset_y)

    # Оси со стрелками
    canvas.create_line(a, x, fill="red", width=2, arrow="last")
    canvas.create_line(a, y, fill="green", width=2, arrow="last")
    canvas.create_line(a, z, fill="blue", width=2, arrow="last")

    # Подписи
    canvas.create_text(x[0] + 10, x[1], text="X", fill="red", font=("Arial", 12, "bold"))
    canvas.create_text(y[0] + 10, y[1], text="Y", fill="green", font=("Arial", 12, "bold"))
    canvas.create_text(z[0] + 10, z[1], text="Z", fill="blue", font=("Arial", 12, "bold"))




def render_mesh(triangles : list, angle_z=0.0, angle_x=0.0, width=800, height=600) -> None:
    """Открывает окно и рисует все треугольники"""
    root = tk.Tk()
    root.title("3D Mesh Viewer")
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    draw_axes(canvas)
    rotated_tris = []
    for tri in triangles:
        a = tri.a.rotate_z(angle_z).rotate_x(angle_x)
        b = tri.b.rotate_z(angle_z).rotate_x(angle_x)
        c = tri.c.rotate_z(angle_z).rotate_x(angle_x)
        rotated_tris.append(Triangle(a, b, c))

    for tri in rotated_tris:
        draw_triangle(canvas, tri)
    root.mainloop()
