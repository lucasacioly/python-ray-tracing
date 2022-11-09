import json
from scene import Scene
import objects
from basic_geom import Color, Point, Vector3
import numpy as np
import generator as gnt
from light import Light
from material import Material

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
        "ambient_light" : info["ambient_light"],
        "lights": tuple(info["lights"]),
        "max_depth": info["max_depth"]
    }

    return info

def load_json_V2(path : str):

    with open(path, 'r') as f:
        info = json.load(f)

    try:
        soft_shadows = info["soft_shadows"]
    except:
        soft_shadows = 0
        
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
        "ambient_light" : info["ambient_light"],
        "lights": tuple(info["lights"]),
        "max_depth": 0,
        "soft_shadows" : soft_shadows,
    }



    return info

def detect_object(object : dict):
    
    new_obj = None

    material = Material(Color(*object["color"]),
                        object["ka"],
                        object["kd"],
                        object["ks"],
                        object["exp"],
                        object["kr"],
                        object["kt"],
                        1/object["index_of_refraction"])

    if "sphere" in object:
        sphere = object["sphere"]
        center = Point(*sphere["center"])
        radius = sphere["radius"]
        new_obj = objects.Sphere(center, radius, material)
    elif "plane" in object:
        plane = object["plane"]
        point = Point(*plane["sample"])
        normal = Vector3(*plane["normal"])
        new_obj = objects.Plane(point, normal, material)
    elif "triangle" in object:
        triangle = object["triangle"]
        p1 = Point(*triangle[0])
        p2 = Point(*triangle[1])
        p3 = Point(*triangle[2])
        new_obj = objects.Triangle(p1, p2, p3, material)
    
    return new_obj

def detect_object_V2(object : dict):
    
    new_obj = None

    material = Material(Color(*object["color"]),
                        object["ka"],
                        object["kd"],
                        object["ks"],
                        object["exp"])

    if "sphere" in object:
        sphere = object["sphere"]
        center = Point(*sphere["center"])
        radius = sphere["radius"]
        new_obj = objects.Sphere(center, radius, material)
    elif "plane" in object:
        plane = object["plane"]
        point = Point(*plane["sample"])
        normal = Vector3(*plane["normal"])
        new_obj = objects.Plane(point, normal, material)
    elif "triangle" in object:
        triangle = object["triangle"]
        p1 = Point(*triangle[0])
        p2 = Point(*triangle[1])
        p3 = Point(*triangle[2])
        new_obj = objects.Triangle(p1, p2, p3, material)
    
    return new_obj

def build_scene(info : dict):

    objts = []

    for obj in info["objects"]:
        new_obj = detect_object(obj)
        objts.append(new_obj)

    lights = []

    for light in info["lights"]:
        lights.append(Light(Point(*light["position"]), Color(*light["intensity"])))

    scene = Scene(
        width = info["width"],
        height = info["height"],
        cam_pixel_size = info["cam_pixel_size"],
        cam_focus_dist = info["cam_focus_dist"],
        cam_eye = Point(*info["cam_eye"]),
        cam_look_at = Point(*info["cam_look_at"]),
        cam_up = Vector3(*info["cam_up"]),
        bg_color = Color(*info["bg_color"]),
        obj_list = objts,
        ambient_light = Color(*info["ambient_light"]),
        lights = lights,
        max_depth = info["max_depth"]
    )

    return scene

if __name__ == "__main__":
    eclipse = load_json('./V3_inputs/newton.json')
    print(eclipse)

    scene = build_scene(eclipse)
    print('ok')
    print(scene.width)
    print(scene.height)
    print(scene.cam_pixel_size)
    print(scene.cam_focus_dist)
    print(scene.cam_eye.vector)
    print(scene.cam_look_at.vector)
    print(scene.cam_up.vector)
    print(scene.bg_color.vector)
    for obj in scene.obj_list:
        print(obj)
    print(scene.ambient_light.vector)
    for light in scene.lights:
        print(light)

    img = gnt.trace_img(scene)
    gnt.save_img('./outputs/newton3', img)

