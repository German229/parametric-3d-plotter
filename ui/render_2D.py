import tkinter as tk
from geometry.vector3 import Vector3
from geometry.triangle import Triangle
from engine.mesh_builder import generate_points, build_triangles_from_grid


def project_point(v: Vector3, scale=100, offset_x=400, offset_y=300):
    return (v.x * scale + offset_x, -v.y * scale + offset_y)

def draw_triangle(canvas, triangle : Triangle, color="black"):
    a = project_point(triangle.a)
    b = project_point(triangle.b)
    c = project_point(triangle.c)
    canvas.create_line(a, b, fill=color)
    canvas.create_line(b, c, fill=color)
    canvas.create_line(c, a, fill=color)



def render_mesh(triangles, width=800, height=600):
    """Открывает окно и рисует все треугольники"""
    root = tk.Tk()
    root.title("3D Mesh Viewer")
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    for tri in triangles:
        draw_triangle(canvas, tri)

    root.mainloop()
