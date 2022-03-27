import numpy as np
import matplotlib.pyplot as plt


def reflected(V, axis): return V - 2 * np.dot(V, axis) * axis


def normalize(V): return V / np.linalg.norm(V)


def sphere_intersect(center, radius, ray_origin, ray_diretion):
    a = 1  # here "a = |d| ** 2"
    b = 2 * np.dot(ray_diretion, ray_origin - center)
    c = np.square(np.linalg.norm(ray_origin - center)) - np.square(radius)
    delta = np.square(b) - 4 * a * c

    if delta > 0:  # if the ray intersects the sphere
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2

        if (t1 and t2) > 0:  # if the intersection is in the ray direction, return the nearest one
            return min(t1, t2)

    return None  # if the ray is tangent or don"t even touch the sphere

def sphere_intersect1(center, radius, ray_origin, ray_diretion):
    I = center - ray_origin
    Tca = np.dot(I, ray_diretion)
    D_sqrt = np.dot(I, I) - (Tca ** 2)
    
    if D_sqrt > (radius ** 2):
        return None
    else:
        Thc = np.sqrt((radius ** 2) - D_sqrt)
        t0, t1 = Tca - Thc, Tca + Thc

        if t0 > t1:
            t0, t1 = t1, t0
        elif t0 < 0:
            if t1 < 0:
                return None
            else:
                return t1
        else:
            return t0

def nearest_intersected_object(objects, ray_origin, ray_direction):
    distances = [sphere_intersect1(
        obj["center"], obj["radius"], ray_origin, ray_direction) for obj in objects]
    nearest_object = None

    # check for objetct with the minimum distance from the camera
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]

    return nearest_object, min_distance


def phong_illumination(Ka, Kd, Ks, Ia, Id, Is, L, N, V, alpha):
    illumination = np.zeros((3))

    # ambient
    illumination += Ka * Ia

    # diffuse
    illumination += Kd * Id * np.dot(L, N)

    # specular
    H = normalize(L + V)
    illumination += Ks * Is * np.dot(N, H) ** (alpha / 4)

    return illumination


######## --- DEFINITIONS --- ########
width = 300
height = 200
image = np.zeros((height, width, 3))

camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio)  # left, top, right, bottom


objects = [
    {"center": np.array([-0.2, 0, -1]), "radius": 0.7, "ambient": np.array([0.1, 0, 0]), "diffuse": np.array(
        [0.7, 0, 0]), "specular": np.array([1, 1, 1]), "shininess": 100, "reflection": 0.5},
    {"center": np.array([0.1, -0.3, 0]), "radius": 0.1, "ambient": np.array([0.1, 0, 0.1]), "diffuse": np.array(
        [0.7, 0, 0.7]), "specular": np.array([1, 1, 1]), "shininess": 100, "reflection": 0.5},
    {"center": np.array([-0.3, 0, 0]), "radius": 0.15, "ambient": np.array([0, 0.1, 0]), "diffuse": np.array(
        [0, 0.6, 0]), "specular": np.array([1, 1, 1]), "shininess": 100, "reflection": 0.5},
    {"center": np.array([0, -9000, 0]), "radius": 9000 - 0.7, "ambient": np.array([0.1, 0.1, 0.1]),
     "diffuse": np.array([0.6, 0.6, 0.6]), "specular": np.array([1, 1, 1]), "shininess": 100, "reflection": 0.5}
]

light = {"position": np.array([5, 5, 5]), "ambient": np.array(
    [1, 1, 1]), "diffuse": np.array([1, 1, 1]), "specular": np.array([1, 1, 1])}

max_depth = 3
##### --- END OF DEFINITION --- #####


for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        pixel = np.array([x, y, 0])
        origin = camera
        direction = normalize(pixel - origin)

        color = np.zeros((3))
        reflection = 1

        for k in range(max_depth):
            # check for intersections
            nearest_object, min_distance = nearest_intersected_object(
                objects, origin, direction)
            if nearest_object is None:
                break

            # compute intersection point between ray and nearest object
            intersection = origin + min_distance * direction

            # shift the intersection point in order to avoid identifying the object itself as an object between the light and itself
            normal_to_surface = normalize(
                intersection - nearest_object["center"])
            shifted_point = intersection + 1e-5 * normal_to_surface

            # calculate the nearest object between the object pixel and the light
            intersection_to_light = normalize(
                light["position"] - shifted_point)
            _, min_distance = nearest_intersected_object(
                objects, shifted_point, intersection_to_light)

            intersection_to_light_distance = np.linalg.norm(
                light["position"] - intersection)

            # if there is an object between the light and the pixel, don't colour it
            is_shadowed = min_distance < intersection_to_light_distance
            if is_shadowed:
                break

            illumination = np.zeros((3))

            # ambient
            illumination += nearest_object["ambient"] * light["ambient"]

            # diffuse
            illumination += nearest_object["diffuse"] * light["diffuse"] * \
                np.dot(intersection_to_light, normal_to_surface)

            # specular
            intersection_to_camera = normalize(camera - intersection)
            H = normalize(intersection_to_light + intersection_to_camera)
            illumination += nearest_object["specular"] * light["specular"] * np.dot(
                normal_to_surface, H) ** (nearest_object["shininess"] / 4)

            # reflection
            color += reflection * illumination
            reflection *= nearest_object["reflection"]

            origin = shifted_point
            direction = reflected(direction, normal_to_surface)

        image[i, j] = np.clip(color, 0, 1)
    print("%d/%d" % (i + 1, height))

plt.imsave("image1.png", image)