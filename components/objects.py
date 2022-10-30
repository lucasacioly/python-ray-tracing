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
    T1 = None
    T2 = None
    T3 = None
    point = None
    normal = None
    #alturas
    altura1,altura2,altura3 = np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0])
    #normal dessas alturas
    norm_altura1,norm_altura2,norm_altura3 = 0,0,0
    #hitbox
    min_x,max_x,min_y,max_y,min_z,max_z = 0,0,0,0,0,0

    def __init__(self,color : Color, a:np.array, b:np.array, c:np.array):
        self.color = color
        self.T1 = np.array(a)
        self.T2 = np.array(b)
        self.T3 = np.array(c)
        #descobre dois vetores usando os tres pontos que temos:
        vector1 = (self.T1 - self.T2)
        vector2 = (self.T1 - self.T3)
        #calcula os lados
        self.altura1 = self.get_altura(self.T1,self.T2,self.T3) 
        self.altura2 = self.get_altura(self.T2,self.T3,self.T1) 
        self.altura3 = self.get_altura(self.T3,self.T1,self.T2) 
        #salva as normais
        self.norm_altura1 = np.linalg.norm(self.altura1)
        self.norm_altura2 = np.linalg.norm(self.altura2)
        self.norm_altura3 = np.linalg.norm(self.altura3)
        #multiplica esses danados
        self.normal = np.cross(vector1,vector2)
        self.point = self.T1
        self.min_x = min(a[0],b[0],c[0]) - 0.01#ajusta pois a computacao he uma ciencia imperfeita
        self.min_y = min(a[1],b[1],c[1]) - 0.01
        self.min_z = min(a[2],b[2],c[2]) - 0.01
        self.max_x = max(a[0],b[0],c[0]) + 0.01
        self.max_y = max(a[1],b[1],c[1]) + 0.01
        self.max_z = max(a[2],b[2],c[2]) + 0.01

    def get_area(self,point1,point2,point3):
        base = point1 - point2
        lado_p31 = point1 - point3
        proj_altura = np.array((np.dot(lado_p31, base) / np.dot(base, base)) * base)
        altura = proj_altura - lado_p31
        area = np.linalg.norm(altura)*np.linalg.norm(base) /2
        return area

    def get_altura(self,point1_base,point2_base,point3):
        base = point1_base - point2_base
        lado_p31 = point1_base - point3
        proj_altura = np.array((np.dot(lado_p31, base) / np.dot(base, base)) * base)
        altura = proj_altura - lado_p31
        return altura

    def get_proj(self,de_a,em_b):
        return np.array((np.dot(de_a, em_b) / np.dot(em_b, em_b)) * em_b)

    def intersection(self, ray_origin : Point, ray_direction : Vector3):
        #T = (a*f - a*x0 + b*h - b*y0 + c*g - c*z0)/(-a*α - b*β - c*γ)
        a = self.normal[0]
        b = self.normal[1]
        c = self.normal[2]
        x0 = self.point[0]
        y0 = self.point[1]
        z0 = self.point[2]
        alpha = ray_direction.vector[0]
        beta = ray_direction.vector[1]
        gama = ray_direction.vector[2]
        f = ray_origin.vector[0]
        h = ray_origin.vector[1]
        g = ray_origin.vector[2]


        T = float((a*f - a*x0 + b*h - b*y0 + c*g - c*z0)/(-a*alpha - b*beta - c*gama))
        if(not np.isnan(T)):#testa se esta no plano do triangulo
            #tente pegar o ponto onde reta passa pelo plano
            P = (ray_direction.vector*T + ray_origin.vector)
            if self.min_x<=P[0]<=self.max_x and \
              self.min_y<=P[1]<=self.max_y and \
              self.min_z<=P[2]<=self.max_z:
                proj1 = np.linalg.norm(self.get_proj(de_a=(self.T3-P),em_b=self.altura1))
                alpha1 = 1-proj1/self.norm_altura1
                if(0<=alpha1<=1):
                    proj2 = np.linalg.norm(self.get_proj(de_a=(self.T1-P),em_b=self.altura2))
                    beta2 = 1-proj2/self.norm_altura2
                    if(0<=beta2<=1):
                        proj3 = np.linalg.norm(self.get_proj(de_a=(self.T2-P),em_b=self.altura3))
                        gama3 = 1-proj3/self.norm_altura3
                        if(0<=gama3<=1):
                            return T
        else:   
            return None
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