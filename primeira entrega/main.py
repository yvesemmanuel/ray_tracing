import numpy as np
import matplotlib.pyplot as plt
from objects import Plane, Sphere
from rendering import render


def readline(Type): return map(Type, input().split())


if __name__ == "__main__":
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

    plt.imsave("primeira entrega/imagens/image.png", image)