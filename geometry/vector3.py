import math
class Vector3:
    def __init__(self, x : float, y : float, z : float):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other : "Vector3") -> "Vector3":
        """Перегружаем сложение векторов"""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other : "Vector3") -> "Vector3":
        """Перегружаем умножение векторов"""
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __sub__(self, other : "Vector3") -> "Vector3":
        """Перегружаем разность векторов"""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other : "Vector3") -> float:
        """Скалярное произведение векторов"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other : "Vector3") -> "Vector3":
        """Векторное произведение векторов"""
        c_x = self.y * other.z - self.z * other.y
        c_y = self.z * other.x - self.x * other.z
        c_z = self.x * other.y - self.y * other.x
        return Vector3(c_x, c_y, c_z)

    def __repr__(self):
        """Для корректного вывода"""
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def normalize(self) -> "Vector3":
        """Нормируем вектор"""
        normalizing_koef = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        normalized_x = self.x / normalizing_koef
        normalized_y = self.y / normalizing_koef
        normalized_z = self.z / normalizing_koef

        return Vector3(normalized_x, normalized_y, normalized_z) if normalizing_koef != 0 else Vector3(0, 0, 0)

    def length(self) -> float:
        """Длина вектора |x|"""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def as_tuple(self) -> tuple:
        """Представление вектора в виде tuple"""
        return (self.x, self.y, self.z)



"""Тестирование класса"""
# x1, y1, z1 = map(float, input().split())
# x2, y2, z2 = map(float, input().split())
# vec_1 = Vector3(x1, y1, z1)
# vec_2 = Vector3(x2, y2, z2)
# inpt = input()
# while inpt != "q":
#     print(eval(inpt))
#     inpt = input()