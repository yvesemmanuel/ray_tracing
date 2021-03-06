import json
import numpy as np
import matplotlib.pyplot as plt
from objects import Plane, Sphere
from rendering import render, cast

path='/Users/lorevilaca/Documents/GithubProjects/ray_tracing/terceira entrega/testes/vidro4.json'
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
    max_depth = data ['max_depth']
    objects = []
    for obj in data['objects']:
        if 'plane' in obj:
            plane = Plane(np.array(obj['plane']['sample']), np.array(obj['plane']['normal']))
            plane.set_color(np.array(obj['color'])/255)
            plane.set_illumination(obj['ka'], obj['kd'], obj['ks'], obj['exp'])
            plane.set_reflection(obj['kr'])
            plane.set_transparency(obj['kt'], obj['index_of_refraction'])
            objects.append(plane)
        if 'sphere' in obj:
            sphere = Sphere(np.array(obj['sphere']['center']), np.array(obj['sphere']['radius']))
            sphere.set_color(np.array(obj['color'])/255)
            sphere.set_illumination(obj['ka'], obj['kd'], obj['ks'], obj['exp'])
            sphere.set_reflection(obj['kr'])
            sphere.set_transparency(obj['kt'], obj['index_of_refraction'])
            objects.append(sphere)
    ambient_light = np.array(data['ambient_light'])/255
    lights = []
    for light in data['lights']:
        lights.append((np.array(light['intensity'])/255, np.array(light['position'])))
    img = render(objects, lights, v_res, h_res, s, d, E, L, up, background_color, ambient_light, max_depth)
    plt.imshow(img)
    plt.show()