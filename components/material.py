from basic_geom import Color

class Material:

    color : Color = None
    ka : float = None
    kd : float = None
    ks : float = None
    phong_exp : float = None

    kr : float = None
    kt : float = None
    refract_idx : float = None
    
    def __init__(self, color : Color, 
                ambient=0.05,diffuse=1.0, specular=1.0, phong=50, 
                kr = None, kt = None, refract_idx = None):

        self.color = color
        self.ka = ambient
        self.kd = diffuse
        self.ks = specular
        self.phong_exp = phong
        self.kr = kr
        self.kt = kt
        self.refract_idx = refract_idx

    
    def get_color(self):
        return self.color.vector
    
    