from basic_geom import Point, Vector3, Color
import numpy as np

class Sphere:

    kind = 'sphere'
    color = None
    center = None
    radius = None
    
    def __init__(self, color: Color, center:Point, radius:float):
        self.color = color
        self.center = center
        self.radius = radius

    def intersection(self, ray_origin : Point, ray_direction : Vector3):
        a = np.linalg.norm(ray_direction.vector)** 2
        b = 2 * np.dot(ray_direction.vector, ray_origin.vector - self.center.vector)
        c = np.linalg.norm(ray_origin.vector - self.center.vector) ** 2 - self.radius ** 2
        # solving quadratic equation
        delta = b ** 2 - (4 * a* c)
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / (2 * a)
            t2 = (-b - np.sqrt(delta)) / (2 * a)
            if t1 > 0 and t2 > 0:
                return min(t1, t2)
        return None

class Triangle:

    kind = 'triangle'
    color = None
    a = None
    b = None
    c = None

    def __init__(self, color: Color, a:Point, b:Point, c:Point):
        self.color = color
        self.a = a
        self.b = b
        self.c = c
    
    def intersection(self):
        return None

class Plane:

    kind = 'plane'
    color = None
    point = None
    normal = None

    def __init__(self, color: Color, point:Point, normal:Vector3):
        self.color = color
        self.point = point
        self.normal = normal

    def intersection(self):
        return None