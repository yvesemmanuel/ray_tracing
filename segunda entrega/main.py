import numpy as np
import matplotlib.pyplot as plt
from objects import Plane, Sphere
from rendering import render, cast


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
    B = np.array((Br, Bg, Bb))/255

    objects = []

    for obj in range(k_obj):
        info = input()

        if "*" in info:
            illumination_info, sphere_info = info.split(" * ")
            CdR, CdG, CdB, Ka, Kd, Ks, n = map(float, illumination_info.split())
            Ox, Oy, Oz, r = map(float, sphere_info.split())

            new_sphere = Sphere((Ox, Oy, Oz), r)
            new_sphere.set_color((CdR, CdG, CdB))
            new_sphere.set_illumination(Ka, Kd, Ks, n)

            objects.append(new_sphere)
        elif "/" in info:
            illumination_info, plane_info = info.split(" / ")
            CdR, CdG, CdB, Ka, Kd, Ks, n = map(float, illumination_info.split())
            Px, Py, Pz, Nx, Ny, Nz = map(float, plane_info.split())

            new_plane = Plane((Px, Py, Pz), (Nx, Ny, Nz))
            new_plane.set_color((CdR, CdG, CdB))
            new_plane.set_illumination(Ka, Kd, Ks, n)

            objects.append(new_plane)
    #########################################

    CaR, CaG, CaB = readline(float)
    C = np.array((CaR, CaG, CaB))/255
    
    k_pl = int(input())
    lightsources = []
    for source in range(k_pl):
        Cr, Cg, Cb, Lx, Ly, Lz = readline(float)
        lightsources.append((np.array((Cr, Cg, Cb))/255, np.array((Lx, Ly, Lz))))

    image = render(objects, lightsources, v_res, h_res, s, d, E, L, UP, B, C)
    #plt.imsave("segunda entrega/imagens/eclipse.png", image)
    plt.imshow(image)
    plt.show()