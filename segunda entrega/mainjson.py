import json
import numpy as np
import matplotlib.pyplot as plt
from objects import Plane, Sphere
from rendering import render, cast

path='C:\\Users\\lorev\\Documents\\Workspace\\ray_tracing\\segunda entrega\\testes\\eclipse.json'
with open(path) as f:
    data = json.load(f)
    v_res = data['v_res']
    h_res = data['h_res']
    s = data['square_side']
    d = data['dist']
    E = np.array(data['eye'])
    L = np.array(data['look_at'])
    up = np.array(data['up'])
    background_color = np.array(data['background_color'])/255
    objects = []
    for obj in data['objects']:
        if 'plane' in obj:
            plane = Plane(np.array(obj['plane']['sample']), np.array(obj['plane']['normal']))
            plane.set_color(np.array(obj['color'])/255)
            plane.set_illumination(obj['ka'], obj['kd'], obj['ks'], obj['exp'])
            objects.append(plane)
        if 'sphere' in obj:
            sphere = Sphere(np.array(obj['sphere']['center']), np.array(obj['sphere']['radius']))
            sphere.set_color(np.array(obj['color'])/255)
            sphere.set_illumination(obj['ka'], obj['kd'], obj['ks'], obj['exp'])
            objects.append(sphere)
    ambient_light = np.array(data['ambient_light'])/255
    lights = []
    for light in data['lights']:
        lights.append((np.array(light['intensity'])/255, np.array(light['position'])))
    img = render(objects, lights, v_res, h_res, s, d, E, L, up, background_color, ambient_light)
    plt.imshow(img)
    plt.show()