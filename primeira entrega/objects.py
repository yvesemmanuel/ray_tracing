import numpy as np


class Object:
    def set_color(self, RGB_color):
        self.color = np.array(RGB_color)


class Sphere(Object):
    def __init__(self, C, r):
        self.C = np.array(C)
        self.r = r

    def intersection(self, ray_O, ray_D):
        I = self.C - ray_O
        Tca = np.dot(I, ray_D)
        D_sqrt = np.dot(I, I) - (Tca ** 2)

        if D_sqrt > (self.r ** 2):
            return None
        else:
            Thc = ((self.r ** 2) - D_sqrt) ** 0.5
            t0, t1 = Tca - Thc, Tca + Thc

            if t0 > t1:
                t0, t1 = t1, t0
            elif t0 < 0:
                if t1 < 0:
                    return None
                else:
                    return t1

            return t0

    def __str__(self):
        return "Sphere"


class Plane(Object):
    def __init__(self, P, N):
        self.P = np.array(P)
        self.N = np.array(N)

    def intersection(self, ray_O, ray_D):
        e = 1e-6
        den = np.dot(self.N, ray_D)

        if abs(den) > e:
            t = np.dot((self.P - ray_O), self.N) / den

            if t < 0:
                return None
            else:
                return t

        return None

    def __str__(self):
        return "Plane"
