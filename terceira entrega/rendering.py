from logging import raiseExceptions
from this import d
from warnings import catch_warnings
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


def shade(O, objs, P, w, n, Ca, light_sources, e=10E-5):
    Cp = O.Ka * O.color * Ca
    
    for c, L in light_sources:
        l = normalize(L - P)
        r = reflect(l, n)
        new_P = P + e*l

        S = trace(objs, new_P, l)
        S.sort()

        t = 0
        if len(S) != 0:
            t, obj = S[0]

        if len(S) == 0 or (np.dot(l, L - new_P) < t):
            if np.dot(n, l) > 0:
                Cp += (O.Kd * O.color) * (np.dot(n, l) * c)
            
            if np.dot(w, r) > 0:
                Cp += O.Ks * (np.dot(w, r) ** O.n) * c
    
    return Cp


def cast(objs, lightsource, ray_O, ray_D, background_color, Ca, max_depth, e=10E-5):
    c = background_color
    
    S = trace(objs, ray_O, ray_D)
    S.sort()

    if len(S) != 0:
        t, obj = S[0]
        P = ray_O + (ray_D * t)
        w = -1 * ray_D
        n = obj.normal(P)
        c = shade(obj, objs, P, w, n, Ca, lightsource)
         
        if max_depth > 0:
            Rr = reflect(w,n)
            new_Pr = P + e*Rr
            try:
                if obj.Kt > 0:
                    Rt = refract(obj,P,w,n)
                    new_Pt = P + e*Rt
                    c = c + obj.Kt * cast(objs, lightsource, new_Pt, Rt, background_color, Ca, max_depth - 1, e)

                if obj.Kr > 0:
                    c = c + obj.Kr * cast(objs, lightsource, new_Pr, Rr, background_color, Ca, max_depth - 1, e)
            
                
            except:
                c = c + cast(objs,lightsource, new_Pr, Rr, background_color, Ca, max_depth -1, e)
    return c


def reflect(l, n): return 2 * n * np.dot(l, n) - l


def refract (obj, P, w, n):
    cos = np.dot(n,w)
    ior = obj.Nr
    normal = n * 1

    if cos < 0:
        normal *= -1
        ior = 1/ior
        cos *= -1
    
    delta = 1 - ((1/(ior**2)) * (1 - cos **2))
    if delta < 0:
        raise Exception ("erro")

    aux = (np.sqrt(delta) - (1/ior * cos))*normal
    return -1/ior * w - aux


def render(objs, lightsource, v_res, h_res, s, d, E, L, up, background_color, Ca, max_depth):
    w = normalize(E - L)
    u = normalize(np.cross(up, w))
    v = np.cross(w, u)

    # Fred's trick
    Q = np.zeros((v_res, h_res, 3))
    img = np.full((v_res, h_res, 3), background_color)

    Q[0, 0] = E - d*w + s * (((v_res - 1) / 2) * v - ((h_res - 1) / 2) * u)

    for i in range(v_res):
        for j in range(h_res):
            Q[i, j] = Q[0, 0] + s*(j*u - i*v)
            ray_D = normalize(Q[i, j] - E)           
            aux = cast(objs, lightsource, E, ray_D, background_color, Ca, max_depth)
            aux = aux/max(*aux, 1)
            img[i][j] = aux

    return img