from basic_geom import Point, Vector3, Color
from objects import Object
from light import Light

class Scene:
    ''' stores information about the scene to be rendered
        camera and objects '''
    
    width : int = None
    height : int = None
    cam_pixel_size : float = None
    cam_focus_dist : float = None
    cam_eye : Point = None
    cam_look_at : Point = None
    cam_up : Vector3 = None
    bg_color : Color = None
    obj_list : list = None
    ambient_light : Color = None
    lights : list[Light] = None
    max_depth : int = None

    def __init__(self,
                width : int, height : int,
                cam_pixel_size : float, cam_focus_dist : float, cam_eye : Point, 
                cam_look_at : Point, cam_up : Vector3,
                bg_color : Color,
                obj_list : list[Object],
                ambient_light : Color = None, lights : list[Light] = None,
                max_depth = 0):
        self.width = width
        self.height = height
        self.cam_pixel_size = cam_pixel_size
        self.cam_focus_dist = cam_focus_dist
        self.cam_eye = cam_eye
        self.cam_look_at = cam_look_at
        self.cam_up = cam_up
        self.bg_color = bg_color
        self.obj_list = obj_list
        self.ambient_light = ambient_light
        self.lights = lights
        self.max_depth = max_depth
