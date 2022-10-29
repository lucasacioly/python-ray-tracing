from basic_geom import Point, Vector3, Color
import numpy as np
from cmath import nan

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

    def intersection(self, ray_origin : Point, ray_direction : Vector3):
        #forma escalar = a(x-x0) + b(y-y0) + c(z-z0) = 0
        #normal = (a,b,c)
        #point = (x0,y0,z0)
        #transforma a forma da reta para:
        #x = f + α*T
        #y = h + β*T
        #z = g + γ*T
        #logo:
        #a((f + α*T)-x0) + b((h + β*T)-y0) + c((g + γ*T)-z0) = 0
        #T = (a*f - a*x0 + b*h - b*y0 + c*g - c*z0)/(-a*α - b*β - c*γ)
        a = self.normal.vector[0]
        b = self.normal.vector[1]
        c = self.normal.vector[2]
        x0 = self.point.vector[0]
        y0 = self.point.vector[1]
        z0 = self.point.vector[2]
        alpha = ray_direction.vector[0]
        beta = ray_direction.vector[1]
        gama = ray_direction.vector[2]
        f = ray_origin.vector[0]
        h = ray_origin.vector[1]
        g = ray_origin.vector[2]

        T = float((a*f - a*x0 + b*h - b*y0 + c*g - c*z0)/(-a*alpha - b*beta - c*gama))

        if(not np.isnan(T) and T>=0):
            return T
        else:
            return None