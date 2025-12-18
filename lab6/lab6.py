import glfw
import math
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Инициализация GLFW
if not glfw.init():
    raise Exception("Ошибка инициализации GLFW")

window = glfw.create_window(1200, 800, "OpenGL Shapes Demo - GLFW", None, None)
if not window:
    glfw.terminate()
    raise Exception("Ошибка создания окна GLFW")

glfw.make_context_current(window)

# Настройка проекционной матрицы (один раз при инициализации)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (1200/800), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

rotation_speed = 0.1
rotation_x, rotation_y = 0, 0
mouse_x, mouse_y = 0, 0
mouse_down = False
draw_mode_lines = True
current_mode = GL_LINE_LOOP if draw_mode_lines else GL_QUADS  # Правильное начальное значение


def draw_square(center_x, center_y, size, color, mode):
    """Рисует квадрат"""
    half_size = size / 2.0
    vertices = [
        (center_x - half_size, center_y - half_size, 0),
        (center_x + half_size, center_y - half_size, 0),
        (center_x + half_size, center_y + half_size, 0),
        (center_x - half_size, center_y + half_size, 0)
    ]

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINE_LOOP)
    else:
        glBegin(GL_QUADS)

    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()


def draw_quadrilateral(center_x, center_y, width, height, color, mode):
    """Рисует четырехугольник"""
    half_width = width / 2.0
    half_height = height / 2.0
    vertices = [
        (center_x - half_width, center_y - half_height, 0),
        (center_x + half_width, center_y - half_height, 0),
        (center_x + half_width, center_y + half_height, 0),
        (center_x - half_width, center_y + half_height, 0)
    ]

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINE_LOOP)
    else:
        glBegin(GL_QUADS)

    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()


def draw_circle(center_x, center_y, radius, segments, color, mode):
    """Рисует круг"""
    vertices = []
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        vertices.append((x, y, 0))

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINE_LOOP)
    else:
        glBegin(GL_POLYGON)

    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()


def draw_polygon(center_x, center_y, radius, sides, color, mode):
    """Рисует правильный многоугольник"""
    vertices = []
    for i in range(sides):
        angle = 2.0 * math.pi * i / sides
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        vertices.append((x, y, 0))

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINE_LOOP)
    else:
        glBegin(GL_POLYGON)

    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()




def draw_parallelepiped(center_x, center_y, center_z, lx, ly, lz, color, mode):
    """Рисует параллелепипед (куб - частный случай)"""
    vertices = [
        (center_x - lx/2, center_y - ly/2, center_z - lz/2),  # 0
        (center_x + lx/2, center_y - ly/2, center_z - lz/2),  # 1
        (center_x + lx/2, center_y + ly/2, center_z - lz/2),  # 2
        (center_x - lx/2, center_y + ly/2, center_z - lz/2),  # 3
        (center_x - lx/2, center_y - ly/2, center_z + lz/2),  # 4
        (center_x + lx/2, center_y - ly/2, center_z + lz/2),  # 5
        (center_x + lx/2, center_y + ly/2, center_z + lz/2),  # 6
        (center_x - lx/2, center_y + ly/2, center_z + lz/2)   # 7
    ]

    faces = [
        (0, 1, 2, 3),
        (1, 5, 6, 2),
        (5, 4, 7, 6),
        (4, 0, 3, 7),
        (3, 2, 6, 7),
        (4, 5, 1, 0)
    ]

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
        for edge in edges:
            for vertex_idx in edge:
                glVertex3fv(vertices[vertex_idx])
        glEnd()
    else:
        for face in faces:
            glBegin(GL_QUADS)
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx])
            glEnd()


def draw_pyramid(center_x, center_y, center_z, base_size, height, color, mode):
    """Рисует пирамиду с квадратным основанием"""
    half_base = base_size / 2.0
    apex_y = center_y + height / 2.0
    base_y = center_y - height / 2.0

    vertices = [
        (center_x - half_base, base_y, center_z - half_base),  
        (center_x + half_base, base_y, center_z - half_base),  
        (center_x + half_base, base_y, center_z + half_base),  
        (center_x - half_base, base_y, center_z + half_base), 
        (center_x, apex_y, center_z) 
    ]

    faces = [
        (0, 1, 2, 3), 
        (0, 1, 4),    
        (1, 2, 4),     
        (2, 3, 4),    
        (3, 0, 4)     
    ]

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        edges = [(0,1), (1,2), (2,3), (3,0), (0,4), (1,4), (2,4), (3,4)]
        for edge in edges:
            for vertex_idx in edge:
                glVertex3fv(vertices[vertex_idx])
    else:
        for face in faces:
            if len(face) == 4:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_TRIANGLES)
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx])
            glEnd()


def draw_trapezoid(center_x, center_y, center_z, top_width, bottom_width, depth, height, color, mode):
    """Рисует трапецию (усеченную пирамиду)"""
    half_top = top_width / 2.0
    half_bottom = bottom_width / 2.0
    half_depth = depth / 2.0
    half_height = height / 2.0

    vertices = [
        (center_x - half_bottom, center_y - half_height, center_z - half_depth),  # 0
        (center_x + half_bottom, center_y - half_height, center_z - half_depth),  # 1
        (center_x + half_bottom, center_y - half_height, center_z + half_depth),  # 2
        (center_x - half_bottom, center_y - half_height, center_z + half_depth),  # 3
        (center_x - half_top, center_y + half_height, center_z - half_depth),     # 4
        (center_x + half_top, center_y + half_height, center_z - half_depth),     # 5
        (center_x + half_top, center_y + half_height, center_z + half_depth),     # 6
        (center_x - half_top, center_y + half_height, center_z + half_depth)      # 7
    ]

    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7)   # left
    ]

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
        for edge in edges:
            for vertex_idx in edge:
                glVertex3fv(vertices[vertex_idx])
    else:
        for face in faces:
            glBegin(GL_QUADS)
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx])
            glEnd()


def draw_tetrahedron(center_x, center_y, center_z, size, color, mode):
    """Рисует тетраэдр"""
    a = size / math.sqrt(2)
    vertices = [
        (center_x, center_y + a/2, center_z),
        (center_x - a/2, center_y - a/6, center_z - a/2),
        (center_x + a/2, center_y - a/6, center_z - a/2),
        (center_x, center_y - a/6, center_z + a/2)
    ]

    faces = [
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 1), 
        (1, 3, 2) 
    ]

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        edges = [(0,1), (0,2), (0,3), (1,2), (2,3), (3,1)]
        for edge in edges:
            for vertex_idx in edge:
                glVertex3fv(vertices[vertex_idx])
    else:
        for face in faces:
            glBegin(GL_TRIANGLES)
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx])
            glEnd()


# Круглые объекты

def draw_polygonal_pyramid(center_x, center_y, center_z, base_radius, height, sides, color, mode):
    """Рисует пирамиду с многоугольным основанием"""
    vertices = []
    base_y = center_y - height / 2.0
    apex_y = center_y + height / 2.0

    # Вершины основания
    for i in range(sides):
        angle = 2.0 * math.pi * i / sides
        x = center_x + base_radius * math.cos(angle)
        z = center_z + base_radius * math.sin(angle)
        vertices.append((x, base_y, z))

    # Вершина
    vertices.append((center_x, apex_y, center_z))
    apex_idx = sides

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        # Ребра основания
        for i in range(sides):
            glVertex3fv(vertices[i])
            glVertex3fv(vertices[(i + 1) % sides])
        # Ребра к вершине
        for i in range(sides):
            glVertex3fv(vertices[i])
            glVertex3fv(vertices[apex_idx])
    else:
        # Основание
        glBegin(GL_POLYGON)
        for i in range(sides):
            glVertex3fv(vertices[i])
        glEnd()

        # Боковые грани
        for i in range(sides):
            glBegin(GL_TRIANGLES)
            glVertex3fv(vertices[i])
            glVertex3fv(vertices[(i + 1) % sides])
            glVertex3fv(vertices[apex_idx])
            glEnd()


def draw_cone(center_x, center_y, center_z, base_radius, height, segments, color, mode):
    """Рисует конус"""
    vertices = []
    base_y = center_y - height / 2.0
    apex_y = center_y + height / 2.0

    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = center_x + base_radius * math.cos(angle)
        z = center_z + base_radius * math.sin(angle)
        vertices.append((x, base_y, z))

    vertices.append((center_x, apex_y, center_z))
    apex_idx = segments

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        for i in range(segments):
            glVertex3fv(vertices[i])
            glVertex3fv(vertices[(i + 1) % segments])
        for i in range(segments):
            glVertex3fv(vertices[i])
            glVertex3fv(vertices[apex_idx])
    else:
        glBegin(GL_POLYGON)
        for i in range(segments):
            glVertex3fv(vertices[i])
        glEnd()

        for i in range(segments):
            glBegin(GL_TRIANGLES)
            glVertex3fv(vertices[i])
            glVertex3fv(vertices[(i + 1) % segments])
            glVertex3fv(vertices[apex_idx])
            glEnd()


def draw_cylinder(center_x, center_y, center_z, bottom_radius, top_radius, height, segments, color, mode):
    """Рисует цилиндр"""
    vertices = []
    bottom_y = center_y - height / 2.0
    top_y = center_y + height / 2.0

    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = center_x + bottom_radius * math.cos(angle)
        z = center_z + bottom_radius * math.sin(angle)
        vertices.append((x, bottom_y, z))

    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = center_x + top_radius * math.cos(angle)
        z = center_z + top_radius * math.sin(angle)
        vertices.append((x, top_y, z))

    bottom_start = 0
    top_start = segments

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        for i in range(segments):
            glVertex3fv(vertices[bottom_start + i])
            glVertex3fv(vertices[bottom_start + (i + 1) % segments])
        for i in range(segments):
            glVertex3fv(vertices[top_start + i])
            glVertex3fv(vertices[top_start + (i + 1) % segments])
        for i in range(segments):
            glVertex3fv(vertices[bottom_start + i])
            glVertex3fv(vertices[top_start + i])
    else:
        glBegin(GL_POLYGON)
        for i in range(segments):
            glVertex3fv(vertices[bottom_start + i])
        glEnd()

        glBegin(GL_POLYGON)
        for i in range(segments):
            glVertex3fv(vertices[top_start + i])
        glEnd()

        for i in range(segments):
            glBegin(GL_QUADS)
            glVertex3fv(vertices[bottom_start + i])
            glVertex3fv(vertices[bottom_start + (i + 1) % segments])
            glVertex3fv(vertices[top_start + (i + 1) % segments])
            glVertex3fv(vertices[top_start + i])
            glEnd()


def draw_sphere_lines(center_x, center_y, center_z, radius, segments, color):
    """Рисует сферу апроксимацией линиями"""
    glColor3fv(color)


    for i in range(8): 
        phi = 2 * math.pi * i / 8
        glBegin(GL_LINE_STRIP)
        for j in range(9): 
            theta = math.pi * j / 8
            x = center_x + radius * math.sin(theta) * math.cos(phi)
            y = center_y + radius * math.sin(theta) * math.sin(phi)
            z = center_z + radius * math.cos(theta)
            glVertex3f(x, y, z)
        glEnd()


    for j in range(5): 
        theta = math.pi * j / 4
        glBegin(GL_LINE_LOOP)
        for i in range(16):
            phi = 2 * math.pi * i / 16
            x = center_x + radius * math.sin(theta) * math.cos(phi)
            y = center_y + radius * math.sin(theta) * math.sin(phi)
            z = center_z + radius * math.cos(theta)
            glVertex3f(x, y, z)
        glEnd()


def draw_sphere_triangles(center_x, center_y, center_z, radius, segments, color):
    """Рисует сферу апроксимацией треугольниками"""
    glColor3fv(color)

    vertices = []
    for j in range(segments // 2 + 1):
        theta = math.pi * j / (segments // 2)
        for i in range(segments + 1):
            phi = 2 * math.pi * i / segments

            x = center_x + radius * math.sin(theta) * math.cos(phi)
            y = center_y + radius * math.sin(theta) * math.sin(phi)
            z = center_z + radius * math.cos(theta)
            vertices.append((x, y, z))

    for j in range(segments // 2):
        for i in range(segments):
            glBegin(GL_TRIANGLES)
            glVertex3fv(vertices[j * (segments + 1) + i])
            glVertex3fv(vertices[j * (segments + 1) + i + 1])
            glVertex3fv(vertices[(j + 1) * (segments + 1) + i])
            glEnd()

            glBegin(GL_TRIANGLES)
            glVertex3fv(vertices[j * (segments + 1) + i + 1])
            glVertex3fv(vertices[(j + 1) * (segments + 1) + i + 1])
            glVertex3fv(vertices[(j + 1) * (segments + 1) + i])
            glEnd()


def draw_sphere_pentagons(center_x, center_y, center_z, radius, color):
    """Рисует икосаэдр"""
    phi = (1 + math.sqrt(5)) / 2 

    vertices = [
        (0, 1, phi), (0, 1, -phi), (0, -1, phi), (0, -1, -phi),
        (1, phi, 0), (1, -phi, 0), (-1, phi, 0), (-1, -phi, 0),
        (phi, 0, 1), (phi, 0, -1), (-phi, 0, 1), (-phi, 0, -1)
    ]

    vertices = [(center_x + radius * x, center_y + radius * y, center_z + radius * z)
                for x, y, z in vertices]

    faces = [
        (0, 8, 4, 5, 1), (0, 1, 6, 10, 7), (1, 5, 9, 11, 6),
        (2, 3, 9, 5, 8), (2, 7, 10, 11, 3), (4, 8, 2, 7, 0),
        (9, 3, 11), (10, 6, 11), (4, 0, 7), (5, 4, 8)
    ]

    glColor3fv(color)
    for face in faces:
        if len(face) == 5:
            glBegin(GL_POLYGON)
        else:
            glBegin(GL_TRIANGLES)

        for vertex_idx in face:
            glVertex3fv(vertices[vertex_idx])
        glEnd()


def draw_3d_spiral(center_x, center_y, center_z, radius, height, turns, segments, color, mode):
    """Рисует трехмерную спираль (типа пружины)"""
    glColor3fv(color)

    points = []
    for i in range(segments + 1):
        t = i / segments
        angle = t * turns * 2 * math.pi
        r = radius * (1 - t * 0.3)
        x = center_x + r * math.cos(angle)
        y = center_y + height * t
        z = center_z + r * math.sin(angle)
        points.append((x, y, z))

    if mode == GL_LINE_LOOP:
        glBegin(GL_LINE_STRIP)
        for point in points:
            glVertex3fv(point)
        glEnd()
    else:
        glBegin(GL_QUADS)
        width = 0.05
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]

            if i < len(points) - 2:
                next_p = points[i + 2]
                dir_x = next_p[0] - p1[0]
                dir_z = next_p[2] - p1[2]
                length = math.sqrt(dir_x**2 + dir_z**2)
                if length > 0:
                    perp_x = -dir_z / length * width
                    perp_z = dir_x / length * width
                else:
                    perp_x = width
                    perp_z = 0
            else:
                perp_x = width
                perp_z = 0

            glVertex3f(p1[0] + perp_x, p1[1], p1[2] + perp_z)
            glVertex3f(p1[0] - perp_x, p1[1], p1[2] - perp_z)
            glVertex3f(p2[0] - perp_x, p2[1], p2[2] - perp_z)
            glVertex3f(p2[0] + perp_x, p2[1], p2[2] + perp_z)
        glEnd()


def draw_torus(center_x, center_y, center_z, major_radius, minor_radius, major_segments, minor_segments, color, mode):
    """Рисует тор (бублик)"""
    glColor3fv(color)

    vertices = []
    for i in range(major_segments + 1):
        u = 2 * math.pi * i / major_segments
        for j in range(minor_segments + 1):
            v = 2 * math.pi * j / minor_segments

            x = center_x + (major_radius + minor_radius * math.cos(v)) * math.cos(u)
            y = center_y + minor_radius * math.sin(v)
            z = center_z + (major_radius + minor_radius * math.cos(v)) * math.sin(u)

            vertices.append((x, y, z))

    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        for i in range(major_segments):
            for j in range(minor_segments):
                idx1 = i * (minor_segments + 1) + j
                idx2 = i * (minor_segments + 1) + (j + 1)
                glVertex3fv(vertices[idx1])
                glVertex3fv(vertices[idx2])

        for j in range(minor_segments):
            for i in range(major_segments):
                idx1 = i * (minor_segments + 1) + j
                idx2 = (i + 1) * (minor_segments + 1) + j
                glVertex3fv(vertices[idx1])
                glVertex3fv(vertices[idx2])
    else:
        for i in range(major_segments):
            for j in range(minor_segments):
                idx1 = i * (minor_segments + 1) + j
                idx2 = i * (minor_segments + 1) + (j + 1)
                idx3 = (i + 1) * (minor_segments + 1) + (j + 1)
                idx4 = (i + 1) * (minor_segments + 1) + j

                glBegin(GL_QUADS)
                glVertex3fv(vertices[idx1])
                glVertex3fv(vertices[idx2])
                glVertex3fv(vertices[idx3])
                glVertex3fv(vertices[idx4])
                glEnd()


# Правильные многогранники

def draw_hexahedron(center_x, center_y, center_z, size, color, mode):
    """Рисует гексаэдр (куб)"""
    return draw_parallelepiped(center_x, center_y, center_z, size, size, size, color, mode)


def draw_octahedron(center_x, center_y, center_z, size, color, mode):
    """Рисует октаэдр"""
    vertices = [
        (center_x + size, center_y, center_z),      # 0 - right
        (center_x - size, center_y, center_z),      # 1 - left
        (center_x, center_y + size, center_z),      # 2 - top
        (center_x, center_y - size, center_z),      # 3 - bottom
        (center_x, center_y, center_z + size),      # 4 - front
        (center_x, center_y, center_z - size)       # 5 - back
    ]

    faces = [
        (0, 2, 4), (0, 4, 3), (0, 3, 5), (0, 5, 2),  # правые грани
        (1, 2, 5), (1, 5, 3), (1, 3, 4), (1, 4, 2)   # левые грани
    ]

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        edges = [(0,2), (0,3), (0,4), (0,5), (1,2), (1,3), (1,4), (1,5), (2,4), (2,5), (3,4), (3,5)]
        for edge in edges:
            for vertex_idx in edge:
                glVertex3fv(vertices[vertex_idx])
    else:
        for face in faces:
            glBegin(GL_TRIANGLES)
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx])
            glEnd()


def draw_icosahedron(center_x, center_y, center_z, size, color, mode):
    """Рисует икосаэдр"""
    phi = (1 + math.sqrt(5)) / 2

    vertices = [
        (center_x + 0, center_y + 1, center_z + phi),
        (center_x + 0, center_y + 1, center_z - phi),
        (center_x + 0, center_y - 1, center_z + phi),
        (center_x + 0, center_y - 1, center_z - phi),
        (center_x + 1, center_y + phi, center_z + 0),
        (center_x + 1, center_y - phi, center_z + 0),
        (center_x - 1, center_y + phi, center_z + 0),
        (center_x - 1, center_y - phi, center_z + 0),
        (center_x + phi, center_y + 0, center_z + 1),
        (center_x + phi, center_y + 0, center_z - 1),
        (center_x - phi, center_y + 0, center_z + 1),
        (center_x - phi, center_y + 0, center_z - 1)
    ]

    vertices = [(x * size, y * size, z * size) for x, y, z in vertices]

    faces = [
        (0, 8, 4), (0, 4, 6), (0, 6, 10), (0, 10, 8), (0, 2, 8),
        (2, 8, 5), (2, 5, 9), (2, 9, 3), (2, 3, 7), (2, 7, 10),
        (1, 4, 8), (1, 8, 5), (1, 5, 9), (1, 9, 11), (1, 11, 6),
        (3, 9, 11), (3, 11, 7), (6, 11, 10), (4, 6, 1), (7, 3, 1)
    ]

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        edges = []
        for face in faces:
            for i in range(len(face)):
                edges.append((face[i], face[(i + 1) % len(face)]))
        edges = list(set(edges))
        for edge in edges:
            glVertex3fv(vertices[edge[0]])
            glVertex3fv(vertices[edge[1]])
    else:
        for face in faces:
            glBegin(GL_TRIANGLES)
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx])
            glEnd()


def draw_dodecahedron(center_x, center_y, center_z, size, color, mode):
    """Рисует додекаэдр"""
    phi = (1 + math.sqrt(5)) / 2  # Золотое сечение

    vertices = [
        (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
        (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1),
        (0, phi, 1/phi), (0, phi, -1/phi), (0, -phi, 1/phi), (0, -phi, -1/phi),
        (1/phi, 0, phi), (-1/phi, 0, phi), (1/phi, 0, -phi), (-1/phi, 0, -phi),
        (phi, 1/phi, 0), (phi, -1/phi, 0), (-phi, 1/phi, 0), (-phi, -1/phi, 0)
    ]

    vertices = [(center_x + x * size, center_y + y * size, center_z + z * size) for x, y, z in vertices]

    faces = [
        (0, 8, 4, 13, 12), (1, 14, 15, 5, 9), (2, 10, 6, 13, 12), (3, 15, 7, 11, 14),
        (0, 16, 17, 2, 12), (1, 16, 17, 3, 14), (4, 18, 19, 6, 13), (5, 18, 19, 7, 15),
        (8, 0, 16, 9, 1), (10, 2, 17, 11, 3), (8, 4, 18, 10, 6), (9, 5, 19, 11, 7)
    ]

    glColor3fv(color)
    if mode == GL_LINE_LOOP:
        glBegin(GL_LINES)
        edges = []
        for face in faces:
            for i in range(len(face)):
                edges.append((face[i], face[(i + 1) % len(face)]))
        edges = list(set(edges))
        for edge in edges:
            glVertex3fv(vertices[edge[0]])
            glVertex3fv(vertices[edge[1]])
    else:
        for face in faces:
            glBegin(GL_POLYGON)
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx])
            glEnd()


def draw_axis():
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 1)
    glEnd()

def draw_cube(lx, ly, lz):
    vertices = [(-lx/2, -ly/2, -lz/2), (lx/2, -ly/2, -lz/2), (lx/2, ly/2, -lz/2), (-lx/2, ly/2, -lz/2),
                (-lx/2, -ly/2, lz/2), (lx/2, -ly/2, lz/2), (lx/2, ly/2, lz/2), (-lx/2, ly/2, lz/2)]
    edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
    glBegin(GL_LINES)
    glColor3f(1, 1, 1)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_spiral(radius, height, turns, segments):
    glBegin(GL_LINE_STRIP)
    glColor3f(1, 0, 1)
    for i in range(segments + 1):
        angle = i / segments * turns * 2 * math.pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = height * i / segments
        glVertex3f(x, y, z)
    glEnd()

glEnable(GL_DEPTH_TEST)

def key_callback(window, key, scancode, action, mods):
    global draw_mode_lines
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            draw_mode_lines = not draw_mode_lines
            print(f"Режим переключен: {'Линии' if draw_mode_lines else 'Полигоны'}")
        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

def mouse_button_callback(window, button, action, mods):
    global mouse_down, mouse_x, mouse_y
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            mouse_down = True
            mouse_x, mouse_y = glfw.get_cursor_pos(window)
        elif action == glfw.RELEASE:
            mouse_down = False

def cursor_pos_callback(window, xpos, ypos):
    global mouse_x, mouse_y, rotation_x, rotation_y, rotation_speed
    if mouse_down:
        delta_x = xpos - mouse_x
        delta_y = ypos - mouse_y
        rotation_x += delta_y * rotation_speed
        rotation_y += delta_x * rotation_speed
        mouse_x, mouse_y = xpos, ypos

def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height if height > 0 else 1, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

glfw.set_key_callback(window, key_callback)
glfw.set_mouse_button_callback(window, mouse_button_callback)
glfw.set_cursor_pos_callback(window, cursor_pos_callback)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

# Настройки OpenGL
glEnable(GL_DEPTH_TEST)
glClearColor(0.1, 0.1, 0.2, 1.0)  # Темно-синий фон вместо черного
glShadeModel(GL_SMOOTH)

# Счетчик для анимации
frame_count = 0

while not glfw.window_should_close(window):
    # Определяем текущий режим рисования
    current_mode = GL_LINE_LOOP if draw_mode_lines else GL_QUADS

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -8)

    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)

    frame_count += 1
    anim_angle = frame_count * 0.5

    draw_mode = GL_LINES if draw_mode_lines else GL_QUADS

    glPushMatrix()
    glTranslatef(-4, 2, 0)
    glScalef(0.3, 0.3, 1)

    # Квадрат
    draw_square(0, 0, 2, (1, 0, 0), draw_mode)
    glTranslatef(4, 0, 0)

    # Четырехугольник
    draw_quadrilateral(0, 0, 2.5, 1.5, (0, 1, 0), draw_mode)
    glTranslatef(4, 0, 0)

    # Круг
    draw_circle(0, 0, 1, 32, (0, 0, 1), draw_mode)
    glTranslatef(4, 0, 0)

    # Многоугольник
    draw_polygon(0, 0, 1, 6, (1, 1, 0), draw_mode)

    glPopMatrix()

    # Основные фигуры
    glPushMatrix()
    glTranslatef(-3, 0, 0)
    glScalef(0.8, 0.8, 0.8)

    # Параллелепипед (куб)
    draw_parallelepiped(0, 0, 0, 1, 1, 1, (1, 0, 0), draw_mode)
    glTranslatef(2, 0, 0)

    # Пирамида
    draw_pyramid(0, 0, 0, 1, 1.2, (0, 1, 0), draw_mode)
    glTranslatef(2, 0, 0)

    # Тетраэдр
    draw_tetrahedron(0, 0, 0, 0.8, (0, 0, 1), draw_mode)

    glPopMatrix()

    # Круглые фигуры
    glPushMatrix()
    glTranslatef(-1, -2, 0)
    glScalef(0.8, 0.8, 0.8)

    # Цилиндр
    draw_cylinder(0, 0, 0, 0.4, 0.4, 1.2, 16, (1, 1, 0), draw_mode)
    glTranslatef(2, 0, 0)

    # Конус
    draw_cone(0, 0, 0, 0.5, 1.2, 16, (1, 0, 1), draw_mode)
    glTranslatef(2, 0, 0)

    # Тор
    draw_torus(0, 0, 0, 0.6, 0.2, 12, 8, (0, 1, 1), draw_mode)

    glPopMatrix()

    # Правильные многогранники
    glPushMatrix()
    glTranslatef(2, 0, 0)
    glScalef(0.6, 0.6, 0.6)

    # Гексаэдр (куб)
    draw_hexahedron(0, 0, 0, 0.8, (0.8, 0.8, 0.8), draw_mode)
    glTranslatef(0, -2, 0)

    # Октаэдр
    draw_octahedron(0, 0, 0, 0.8, (0.2, 0.8, 0.8), draw_mode)
    glTranslatef(0, -2, 0)

    # Додекаэдр
    draw_dodecahedron(0, 0, 0, 0.6, (0.7, 0.9, 0.5), draw_mode)

    glPopMatrix()

    mode_name = "Линии" if draw_mode_lines else "Полигоны"
    glfw.set_window_title(window, f"OpenGL Shapes Demo - Режим: {mode_name} (Пробел для переключения, Esc - выход)")

    glfw.swap_buffers(window)
    glfw.poll_events()

    import time
    time.sleep(0.01)

glfw.terminate()
