import json
from scene import Scene
import objects
from basic_geom import Color, Point, Vector3
import numpy as np
import generator as gnt

def load_json(path : str):

    with open(path, 'r') as f:
        info = json.load(f)
    
    info = {
        "width": info["h_res"],
        "height": info["v_res"],
        "cam_pixel_size": info["square_side"],
        "cam_focus_dist": info["dist"],
        "cam_eye": tuple(info["eye"]),
        "cam_look_at": tuple(info["look_at"]),
        "cam_up": tuple(info["up"]),
        "bg_color": tuple(info["background_color"]),
        "objects": info["objects"],
    }

    return info


def detect_object(object : dict):
    
    new_obj = None

    color = Color(*object["color"])

    if "sphere" in object:
        sphere = object["sphere"]
        center = Point(*sphere["center"])
        radius = sphere["radius"]
        new_obj = objects.Sphere(color, center, radius)
    elif "plane" in object:
        plane = object["plane"]
        point = Point(*plane["sample"])
        normal = Vector3(*plane["normal"])
        new_obj = objects.Plane(color, point, normal)
    elif "triangle" in object:
        triangle = object["triangle"]
        p1 = Point(*triangle[0])
        p2 = Point(*triangle[1])
        p3 = Point(*triangle[2])
        new_obj = objects.Triangle(color, p1, p2, p3)
    
    return new_obj

def build_scene(info : dict):

    objts = []

    for obj in info["objects"]:
        new_obj = detect_object(obj)
        objts.append(new_obj)

    scene = Scene(
        width = info["width"],
        height = info["height"],
        cam_pixel_size = info["cam_pixel_size"],
        cam_focus_dist = info["cam_focus_dist"],
        cam_eye = np.array([*info["cam_eye"]]),
        cam_look_at = np.array([*info["cam_look_at"]]),
        cam_up = np.array([*info["cam_up"]]),
        bg_color = np.array([*info["bg_color"]])/255,
        obj_list = objts
    )

    return scene

if __name__ == "__main__":
    cone = load_json('./V1_inputs/japan.json')
    print(cone)

    scene = build_scene(cone)

    
    print('\n--------------------------------\n')
    print(scene.width, '1\n')
    print(scene.height,  '2\n')
    print(scene.bg_color, '3\n')
    print(scene.cam_pixel_size,  '3\n')
    print(scene.cam_focus_dist, '4\n')
    print(scene.cam_eye,  '5\n')
    print(scene.cam_look_at,  '6\n')
    print(scene.cam_up,  '7\n')
    for obj in scene.obj_list:
        print(type(obj),   '8\n'    )

    print('\n--------------------------------\n')

    c = np.zeros((2, 4, 3))

    print(c)

    img = gnt.trace_img(scene).astype(float)
    print('ok')
    gnt.save_img('testando', img)

