from ui.render_3D import render_mesh
from engine.mesh_builder import generate_points, build_triangles_from_grid
from geometry.vector3 import Vector3
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

def input_eval(prompt: str) -> float:
    return eval(input(prompt), {}, math_env)

# --- Ввод выражений ---
print("Введите выражение для x(u,v):")
x_expr = input("x(u,v) = ")

print("Введите выражение для y(u,v):")
y_expr = input("y(u,v) = ")

print("Введите выражение для z(u,v):")
z_expr = input("z(u,v) = ")

# --- Ввод диапазонов параметров u и v ---
u_min = input_eval("u_min = ")
u_max = input_eval("u_max = ")
v_min = input_eval("v_min = ")
v_max = input_eval("v_max = ")
u_step = input_eval("u_step = ")
v_step = input_eval("v_step = ")

# --- Ввод диапазонов параметров alpha и beta ---
alpha_min = input_eval("alpha_min = ")
alpha_max = input_eval("alpha_max = ")
alpha_step = input_eval("alpha_step = ")

beta_min = input_eval("beta_min = ")
beta_max = input_eval("beta_max = ")
beta_step = input_eval("beta_step = ")

# --- Основной цикл по alpha и beta ---
for alpha in frange(alpha_min, alpha_max, alpha_step):
    for beta in frange(beta_min, beta_max, beta_step):
        print(f"\n🔧 Построение графика для alpha = {alpha}, beta = {beta}")

        # Функция, вычисляющая координаты точки
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

        # Построение точек и треугольников
        grid = generate_points(user_func, (u_min, u_max), (v_min, v_max), u_step, v_step)
        triangles = build_triangles_from_grid(grid)

        # Отображение графика
        angle_z = math.radians(45)
        angle_x = math.radians(30)
        render_mesh(triangles, angle_z=angle_z, angle_x=angle_x)
