import numpy as np
import matplotlib.pyplot as plt
from Objects import Plane, Sphere


def readline(Type): return map(Type, input().split())


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

    return img / 255 # this divison makes the RGB a floating point in range (-1, 1)


def reflect (l, n):
    #l = vetor unitário que aponta pra fonte de luz
    #n = vetor unitário normal à superfície
    #a função retorna um vetor unitário na direção refletida
    return 2 * np.dot(n,l) * (n - l)

def refract():

def shade ():

########### -- INPUT -- ###########
v_res, h_res = readline(int)
s, d = readline(float)
Ex, Ey, Ez = readline(float)
Lx, Ly, Lz = readline(float)
UPx, UPy, UPz = readline(float)
Br, Bg, Bb = readline(int)
k_obj = int(input())
###################################


########## --- DEFINITIONS --- ##########
E = np.array((Ex, Ey, Ez))
L = np.array((Lx, Ly, Lz))
UP = np.array((UPx, UPy, UPz))
B = np.array((Br, Bg, Bb))

objects = []

for obj in range(k_obj):
    info = input()

    if "*" in info:
        color_info, sphere_info = info.split(" * ")
        Cr, Cg, Cb = map(int, color_info.split())
        Ox, Oy, Oz, r = map(float, sphere_info.split())

        new_sphere = Sphere((Ox, Oy, Oz), r)
        new_sphere.set_color((Cr, Cg, Cb))

        objects.append(new_sphere)
    elif "/" in info:
        color_info, plane_info = info.split(" / ")
        Cr, Cg, Cb = map(int, color_info.split())
        Px, Py, Pz, Nx, Ny, Nz = map(float, plane_info.split())

        new_plane = Plane((Px, Py, Pz), (Nx, Ny, Nz))
        new_plane.set_color((Cr, Cg, Cb))
        objects.append(new_plane)
#########################################


image = render(objects, v_res, h_res, s, d, E, L, UP, B)

# plt.imsave("primeira entrega/imagens/japão_1.png", image)
# plt.imsave("primeira entrega/imagens/olho_1.png", image)
# plt.imsave("primeira entrega/imagens/polonia_1.png", image)
# plt.imsave("primeira entrega/imagens/ilhas_1.png", image)
plt.imsave("primeira entrega/imagens/canto_1.png", image)