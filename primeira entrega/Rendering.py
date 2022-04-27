import numpy as np
import matplotlib.pyplot as plt
from objects import Plane, Sphere


def normalize(V): return V / np.linalg.norm(V)


def trace(objs, ray_O, ray_D):
    S = []

    for obj in objs:
        t = obj.intersection(ray_O, ray_D)

        if t:
            S.append((t, obj))

    return S


def cast(objs, ray_O, ray_D, background_color):
    c = background_color
    S = trace(objs, ray_O, ray_D)

    S.sort()
    if len(S) != 0:
        closest_obj = S[0][1]
        c = closest_obj.color

    return c


def render(objs, v_res, h_res, s, d, E, L, up, background_color):
    w = normalize(E - L)
    u = normalize(np.cross(up, w))
    v = np.cross(w, u)

    # Fred's trick
    Q = np.zeros((v_res, h_res, 3))
    img = np.zeros((v_res, h_res, 3))

    Q[0, 0] = E - d*w + s * (((v_res - 1) / 2)*v - ((h_res - 1) / 2)*u)

    for i in range(v_res):
        for j in range(h_res):
            Q[i, j] = Q[0, 0] + s*(j*u - i*v)
            ray_D = normalize(Q[i, j] - E)
            img[i, j] = cast(objs, E, ray_D, background_color)

    return img / 255