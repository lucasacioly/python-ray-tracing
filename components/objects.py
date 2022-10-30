from basic_geom import Point, Vector3, Color
import numpy as np

class Sphere:

    kind : str = 'sphere'
    color : Color = None
    center : Point = None
    radius : float = None
    
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

    kind : str = 'triangle'
    color : Color = None
    T1 : Point = None
    T2 : Point = None
    T3 : Point = None
    point : Point = None
    normal : Vector3 = None
    #heights
    height1, height2, height3 = np.array([0,0,0]), np.array([0,0,0]), np.array([0,0,0])
    #height norms (modulus)
    norm_height1, norm_height2, norm_height3 = 0, 0, 0
    #hitbox
    min_x,max_x,min_y,max_y,min_z,max_z = 0,0,0,0,0,0

    def __init__(self,color : Color, a:Point, b:Point, c:Point):
        self.color = color
        self.T1 = a
        self.T2 = b
        self.T3 = c
        
        #get two vectors using the points we have:
        vector1 = Vector3(0,0,0)
        vector1.vector = (self.T1.vector - self.T2.vector)
        vector2 = Vector3(0,0,0)
        vector2.vector = (self.T1.vector - self.T3.vector)

        #get sides
        self.height1 = self.get_height(self.T1,self.T2,self.T3) 
        self.height2 = self.get_height(self.T2,self.T3,self.T1) 
        self.height3 = self.get_height(self.T3,self.T1,self.T2) 

        #get normals
        self.norm_height1 = np.linalg.norm(self.height1)
        self.norm_height2 = np.linalg.norm(self.height2)
        self.norm_height3 = np.linalg.norm(self.height3)

        #multiply
        self.normal = Vector3(0,0,0)
        self.normal.vector = np.cross(vector1.vector,vector2.vector)
        self.point = self.T1
        self.min_x = min(a.vector[0],b.vector[0],c.vector[0]) - 0.01 #adjustment. Conputation is imperfect :(
        self.min_y = min(a.vector[1],b.vector[1],c.vector[1]) - 0.01
        self.min_z = min(a.vector[2],b.vector[2],c.vector[2]) - 0.01
        self.max_x = max(a.vector[0],b.vector[0],c.vector[0]) + 0.01
        self.max_y = max(a.vector[1],b.vector[1],c.vector[1]) + 0.01
        self.max_z = max(a.vector[2],b.vector[2],c.vector[2]) + 0.01

    def get_area(self,point1 : Point, point2 : Point, point3 : Point):
        base = point1.vector - point2.vector
        lado_p31 = point1.vector - point3.vector
        proj_height = np.array((np.dot(lado_p31, base) / np.dot(base, base)) * base)
        height = proj_height - lado_p31
        area : float = np.linalg.norm(height)*np.linalg.norm(base) /2
        return area

    def get_height(self, point1_base : Point, point2_base : Point, point3 : Point):
        base = point1_base.vector - point2_base.vector
        lado_p31 = point1_base.vector - point3.vector
        proj_height = np.array((np.dot(lado_p31, base) / np.dot(base, base)) * base)
        height = proj_height - lado_p31
        return height

    def get_proj(self, from_a : np.array, to_b : np.array):
        return np.array((np.dot(from_a, to_b) / np.dot(to_b, to_b)) * to_b)

    def intersection(self, ray_origin : Point, ray_direction : Vector3):
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
        if(not np.isnan(T)):#test if is the triangle plane
            #try to get the point where the rect intersects the plane
            P = (ray_direction.vector*T + ray_origin.vector)
            if self.min_x<=P[0]<=self.max_x and \
              self.min_y<=P[1]<=self.max_y and \
              self.min_z<=P[2]<=self.max_z:
                proj1 = np.linalg.norm(self.get_proj(from_a=(self.T3.vector-P),to_b=self.height1))
                alpha1 = 1-proj1/self.norm_height1
                if(0<=alpha1<=1):
                    proj2 = np.linalg.norm(self.get_proj(from_a=(self.T1.vector-P),to_b=self.height2))
                    beta2 = 1-proj2/self.norm_height2
                    if(0<=beta2<=1):
                        proj3 = np.linalg.norm(self.get_proj(from_a=(self.T2.vector-P),to_b=self.height3))
                        gama3 = 1-proj3/self.norm_height3
                        if(0<=gama3<=1):
                            return T
        else:   
            return None
        return None

class Plane:

    kind : str = 'plane'
    color : Color = None
    point : Point = None
    normal : Vector3 = None

    def __init__(self, color: Color, point:Point, normal:Vector3):
        self.color = color
        self.point = point
        self.normal = normal

    def intersection(self, ray_origin : Point, ray_direction : Vector3):
        #scalar form = a(x-x0) + b(y-y0) + c(z-z0) = 0
        #normal = (a,b,c)
        #point = (x0,y0,z0)
        #transform rect to:
        #x = f + α*T
        #y = h + β*T
        #z = g + γ*T
        #thus:
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