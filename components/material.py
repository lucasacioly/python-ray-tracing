from basic_geom import Color

class Material:

    color : Color = None
    ka : float = None
    kd : float = None
    ks : float = None
    phong_exp : float = None
    
    def __init__(self, color : Color, 
                ambient=0.05,diffuse=1.0, specular=1.0, phong=50):

        self.color = color
        self.ka = ambient
        self.kd = diffuse
        self.ks = specular
        self.phong_exp = phong
    
    def get_color(self):
        return self.color.vector
    
    