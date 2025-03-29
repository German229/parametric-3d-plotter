from geometry.vector3 import Vector3

class Triangle:
    def __init__(self, a : Vector3, b : Vector3, c : Vector3):
        self.a = a
        self.b = b
        self.c = c
    def __repr__(self):
        return f"Triangle({self.a}, {self.b}, {self.c})"




