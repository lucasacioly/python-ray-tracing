import numpy as np
from objects import Sphere
from scene import Scene
from basic_geom import Vector3, Point
import matplotlib.pyplot as plt
import random

def nearest_intersected_object(objects :list[Sphere], ray_origin : Point, ray_direction : Vector3):
    distances = [obj.intersection(ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance is not None and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance

def get_dir_camera(scene: Scene, cam_dir : Point, cam_pos : Point):
    #descobre o vetor mira 
    mira = Vector3(0,0,0)
    mira.vector = cam_dir.vector-cam_pos.vector 
    #normaliza ele
    n_mira = mira
    n_mira.normalize()
    #descobre a projeção de up em mira
    up = scene.cam_up
    p_up = Vector3(0,0,0)
    p_up.vector = np.array(up.vector - (np.dot(up.vector, n_mira.vector) / np.dot(n_mira.vector, n_mira.vector)) * n_mira.vector)
    #vamos tentar normalizar ele
    if(not (p_up.vector==[0,0,0]).all()):#se ele for diferente de zero he so normalizar
        n_up = p_up
        n_up.normalize()

    else:#se ele for zero quer dizer que os vetores tem o mesmo sentido 
        #por hora vou tirar na sorte para onde deveria ser o up
        up = Vector3(random.random(), random.random(), random.random())
        p_up.vector = np.array(up.vector - (np.dot(up.vector, n_mira.vector) / np.dot(n_mira.vector, n_mira.vector)) * n_mira.vector)
        n_up = p_up
        n_up.normalize()

    #calcula o terceiro (n_side) vetor
    side = Vector3(0,0,0)
    side.vector = np.cross(n_mira.vector,n_up.vector)
    #normaliza ele e coloca do lado certo
    n_side = side 
    n_side.normalize()
    n_side.vector = -n_side.vector
    #n_side = -(side/np.linalg.norm(side))

    #multiplica o vetor n_mira pela distancia
    n_mira.vector *= scene.cam_focus_dist
    #multiplica o vetor n_up e n_side por square-size
    n_up.vector *=  scene.cam_pixel_size
    n_side.vector *=  scene.cam_pixel_size
    #usa esses valores para obter os pontos 

    return n_side,n_mira,n_up

def trace_img(scene: Scene):

    width = scene.width
    height = scene.height
    image = np.full((height, width, 3), scene.bg_color.vector)

    cam_pos = (scene.cam_eye) #camera position
    cam_dir = (scene.cam_look_at) #camera looking point

    n_side,n_mira,n_up = get_dir_camera(scene,cam_pos=cam_pos,cam_dir=cam_dir)

    #ponto inicial
    ponto_inicial = Point(0,0,0)
    if(width%2 == 0):
        ponto_inicial.vector = (width/2 - 1)*n_side.vector + n_mira.vector + cam_pos.vector
    else:
        ponto_inicial.vector = ((width-1)/2 - 0.5)*n_side.vector + n_mira.vector + cam_pos.vector
    if(height%2 == 0):
        ponto_inicial.vector += (height/2 - 1)*n_up.vector
    else:
        ponto_inicial.vector += ((height-1)/2 - 0.5)*n_up.vector

    ponto_atual = Point(0,0,0)
    for i in range(height-1):
        #calculando a posicao atual de y
        ponto_atual.vector = ponto_inicial.vector - n_up.vector*i
        for j in range(width-1):
            ponto_atual.vector -=  n_side.vector
            pixel = Vector3(ponto_atual.vector[0],ponto_atual.vector[1],ponto_atual.vector[2])

            origin = Vector3(cam_pos.vector[0],cam_pos.vector[1],cam_pos.vector[2])
            direction = Vector3(*(pixel.vector - origin.vector))
            direction.normalize()
            nearest_object, min_distance = nearest_intersected_object(scene.obj_list, origin, direction)
            #print(nearest_object)
            # compute intersection point between ray and nearest object
            #intersection = origin.vector + min_distance * direction.vector
            if(nearest_object is not None):
                image[i, j] = np.clip(nearest_object.color.vector, 0, 1)
            else:
                image[i, j] = scene.bg_color.vector
        print("progress: %d/%d" % (i + 1, height))
    return image


def save_img(nome: str, img):
    plt.imsave(f'{nome}.png', img)