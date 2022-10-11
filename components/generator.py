import numpy as np
from objects import Sphere
from scene import Scene
from basic_geom import Vector3, Point
import matplotlib.pyplot as plt

def nearest_intersected_object(objects :list[Sphere], ray_origin : Point, ray_direction : Vector3):
    distances = [obj.intersection(ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance is not None and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance

def trace_img(scene: Scene):

    width = scene.width
    height = scene.height

    #cam_pos = Point(0, 0, 1)
    cam_pos = scene.cam_eye #camera position
    cam_dir = scene.cam_look_at #camera looking point
    ratio = float(width) / height 
    screen = (-1, 1 / ratio, 1, -1 / ratio) # left, top, right, bottom

    image = np.full((height, scene.width, 3), scene.bg_color.vector)

    for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
            pixel = Vector3(x, y, 0)
            origin = cam_pos
            direction = Vector3(*(pixel.vector - origin.vector))
            direction.normalize()
            nearest_object, min_distance = nearest_intersected_object(scene.obj_list, origin, direction)
            if nearest_object is None:
                continue
            #print(nearest_object)
            # compute intersection point between ray and nearest object
            intersection = origin.vector + min_distance * direction.vector
            image[i, j] = np.clip(nearest_object.color.vector, 0, 1)
            
        print("progress: %d/%d" % (i + 1, height))

    return image


def save_img(nome: str, img):
    plt.imsave(f'{nome}.png', img)