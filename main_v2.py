import tkinter as tk
from ui.render_3D import project_point, draw_triangle
from engine.mesh_builder import generate_points, build_triangles_from_grid
from geometry.vector3 import Vector3
from geometry.triangle import Triangle
import math

def rotate_y(self, angle_rad: float) -> Vector3:
    """Добавляем rotate_y в Vector3 (если не было)"""
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    z = self.z * cos_a - self.x * sin_a
    x = self.z * sin_a + self.x * cos_a
    return Vector3(x, self.y, z)

Vector3.rotate_y = rotate_y  # 'динамически' встраиваем метод

def frange(start, stop, step):
    """Вспомогательная функция для диапазонов с шагом по float"""
    while start <= stop + 1e-9:
        yield start
        start += step


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

params = parse_file("files/5_shell.txt")

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

root = tk.Tk()
root.title("3D Mesh Viewer")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

"""наклон по X"""
camera_angle_x = math.radians(45)

"""наклонять по Y"""
camera_angle_y = math.radians(40)

"""Изначальный угол вращения по Z"""
angle_z_deg = 0

def draw_axes_custom(canvas, angle_z):
    """
    Рисуем оси, тоже под камерным наклоном и поворотом Z.
    """
    origin = Vector3(0, 0, 0)
    x_axis = Vector3(1, 0, 0)
    y_axis = Vector3(0, 1, 0)
    z_axis = Vector3(0, 0, 1)

    # Сначала наклоняем камеру (rotate_x, rotate_y), потом вращаем Z
    def cam_transform(v: Vector3):
        return (
            v
            .rotate_x(camera_angle_x)
            .rotate_y(camera_angle_y)
            .rotate_z(math.radians(angle_z))
        )

    origin_t = cam_transform(origin)
    x_axis_t = cam_transform(x_axis)
    y_axis_t = cam_transform(y_axis)
    z_axis_t = cam_transform(z_axis)

    # Проецируем 2D
    a = project_point(origin_t)
    x = project_point(x_axis_t)
    y = project_point(y_axis_t)
    z = project_point(z_axis_t)

    # Рисуем оси
    canvas.create_line(a, x, fill="red", width=2, arrow="last")
    canvas.create_line(a, y, fill="green", width=2, arrow="last")
    canvas.create_line(a, z, fill="blue", width=2, arrow="last")
    canvas.create_text(x[0] + 10, x[1], text="X", fill="red", font=("Arial", 12, "bold"))
    canvas.create_text(y[0] + 10, y[1], text="Y", fill="green", font=("Arial", 12, "bold"))
    canvas.create_text(z[0] + 10, z[1], text="Z", fill="blue", font=("Arial", 12, "bold"))

def build_and_draw(alpha, beta, angle_z_deg):
    """
    Сборка сетки и отрисовка треугольников.
    angle_z_deg - угол поворота по Z, управляемый слайдером.
    """
    angle_z = math.radians(angle_z_deg)

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
    # Рисуем оси: наклон камеры и поворот Z
    draw_axes_custom(canvas, angle_z_deg)

    for tri in triangles:
        # Сначала «камера» (rotate_x, rotate_y), потом поворот Z
        a = (tri.a
             .rotate_x(camera_angle_x)
             .rotate_y(camera_angle_y)
             .rotate_z(angle_z))
        b = (tri.b
             .rotate_x(camera_angle_x)
             .rotate_y(camera_angle_y)
             .rotate_z(angle_z))
        c = (tri.c
             .rotate_x(camera_angle_x)
             .rotate_y(camera_angle_y)
             .rotate_z(angle_z))

        draw_triangle(canvas, Triangle(a, b, c))

# --- Функция для слайдеров ---
def update_from_sliders(event=None):
    a = alpha_slider.get()
    b = beta_slider.get()
    z_deg = angle_slider.get()
    build_and_draw(a, b, z_deg)

# --- Слайдеры ---
alpha_slider = tk.Scale(root, from_=alpha_min, to=alpha_max, resolution=alpha_step,
                        label="alpha", orient=tk.HORIZONTAL, command=update_from_sliders)
alpha_slider.set(alpha_min)
alpha_slider.pack(fill="x")

beta_slider = tk.Scale(root, from_=beta_min, to=beta_max, resolution=beta_step,
                       label="beta", orient=tk.HORIZONTAL, command=update_from_sliders)
beta_slider.set(beta_min)
beta_slider.pack(fill="x")

angle_slider = tk.Scale(root, from_=-180, to=180, resolution=1,
                        label="Вращение по Z", orient=tk.HORIZONTAL, command=update_from_sliders)
angle_slider.set(angle_z_deg)
angle_slider.pack(fill="x")

# --- Первый запуск ---
build_and_draw(alpha_slider.get(), beta_slider.get(), angle_slider.get())
root.mainloop()
