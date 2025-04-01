import tkinter as tk
from ui.render_3D import project_point, draw_axes, draw_triangle
from engine.mesh_builder import generate_points, build_triangles_from_grid
from geometry.vector3 import Vector3
from geometry.triangle import Triangle
import math
from math import sin, cos, tan, exp, pi, sqrt

# --- Вспомогательная функция для диапазонов с шагом ---
def frange(start, stop, step):
    while start <= stop + 1e-9:
        yield start
        start += step

# --- Среда для безопасного eval ---
math_env = {
    "pi": math.pi,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "sqrt": math.sqrt,
    "math": math
}

def parse_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    params = {}
    for line in lines:
        if '=' in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            try:
                params[key] = eval(val, {}, math_env)
            except:
                params[key] = val
    return params

# --- Чтение параметров из файла ---
params = parse_file("files/2_moebius.txt")

x_expr = params["x_expr"]
y_expr = params["y_expr"]
z_expr = params["z_expr"]

u_min = params["u_min"]
u_max = params["u_max"]
v_min = params["v_min"]
v_max = params["v_max"]
u_step = params["u_step"]
v_step = params["v_step"]

alpha_min = params["alpha_min"]
alpha_max = params["alpha_max"]
alpha_step = params["alpha_step"]

beta_min = params["beta_min"]
beta_max = params["beta_max"]
beta_step = params["beta_step"]

# --- Глобальные параметры окна ---
root = tk.Tk()
root.title("3D Mesh Viewer")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

angle_z = math.radians(45)
angle_x = math.radians(30)

def build_and_draw(alpha, beta):
    def user_func(u, v):
        local_vars = {
            "u": u,
            "v": v,
            "alpha": alpha,
            "beta": beta,
            **math_env
        }
        x = eval(x_expr, {}, local_vars)
        y = eval(y_expr, {}, local_vars)
        z = eval(z_expr, {}, local_vars)
        return Vector3(x, y, z)

    grid = generate_points(user_func, (u_min, u_max), (v_min, v_max), u_step, v_step)
    triangles = build_triangles_from_grid(grid)

    canvas.delete("all")
    draw_axes(canvas)
    for tri in triangles:
        a = tri.a.rotate_z(angle_z).rotate_x(angle_x)
        b = tri.b.rotate_z(angle_z).rotate_x(angle_x)
        c = tri.c.rotate_z(angle_z).rotate_x(angle_x)
        draw_triangle(canvas, Triangle(a, b, c))

# --- Слайдеры ---
def update_from_sliders(event=None):
    a = alpha_slider.get()
    b = beta_slider.get()
    build_and_draw(a, b)

alpha_slider = tk.Scale(root, from_=alpha_min, to=alpha_max, resolution=alpha_step,
                        label="alpha", orient=tk.HORIZONTAL, command=update_from_sliders)
alpha_slider.set(alpha_min)
alpha_slider.pack(fill="x")

beta_slider = tk.Scale(root, from_=beta_min, to=beta_max, resolution=beta_step,
                       label="beta", orient=tk.HORIZONTAL, command=update_from_sliders)
beta_slider.set(beta_min)
beta_slider.pack(fill="x")

# --- Первый запуск ---
build_and_draw(alpha_slider.get(), beta_slider.get())
root.mainloop()