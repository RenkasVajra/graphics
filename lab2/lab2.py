import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time

# Инициализация GLFW
if not glfw.init():
    raise Exception("Ошибка инициализации GLFW")

window = glfw.create_window(800, 600, "Анимированные фигуры в OpenGL", None, None)
if not window:
    glfw.terminate()
    raise Exception("Ошибка создания окна GLFW")

glfw.make_context_current(window)

# Переменные для анимации
start_time = time.time()
triangle_rotation = 0.0
square_scale = 1.0
circle_offset = 0.0

# Переменные для многоугольника
polygon_scale = 1.0
polygon_rotation = 0.0
polygon_rotation_point = (-0.3, 0.2, 0.0)  # Точка вращения
polygon_position_x = 0.0
polygon_curve_time = 0.0


# Функции для рисования

def clear_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def draw_triangle(vertices, colors):
    glBegin(GL_TRIANGLES)
    for i in range(len(vertices)):
        glColor3fv(colors[i])
        glVertex3fv(vertices[i])
    glEnd()


def draw_quad(vertices, colors):
    glBegin(GL_QUADS)
    for i in range(len(vertices)):
        glColor3fv(colors[i])
        glVertex3fv(vertices[i])
    glEnd()


def draw_polygon(center, radius, num_sides, color=None, mode=GL_POLYGON):
    vertices = []
    angles = np.linspace(0, 2 * np.pi, num_sides + 1)
    for angle in angles[:-1]:
        vertex = center[:2] + radius * np.array([np.cos(angle), np.sin(angle)])
        vertices.append(np.concatenate((vertex, [center[-1]])))

    if isinstance(color, tuple):
        colors = [color] * len(vertices)
    elif isinstance(color, list):
        colors = color
    else:
        colors = [(1.0, 1.0, 1.0)] * len(vertices)

    glBegin(mode)
    for i in range(len(vertices)):
        glColor3fv(colors[i])
        glVertex3fv(vertices[i])
    glEnd()


# Функция кривой для движения многоугольника
def curve_function(x):
    return 0.5 * np.sin(x) + 0.3 * np.cos(2 * x)


# Начальные настройки камеры
modelview_matrix = np.eye(4)
glLoadIdentity()
glOrtho(-1, 1, -1, 1, -1, 1)

# Вершины и цвета треугольника
triangle_vertices = [
    (-1.0, -1.0, 0),
    (1.0, -1.0, 0),
    (0.0, 1.0, 0)
]
triangle_colors = [
    (1.0, 1.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.2, 0.9, 1.0)
]

# Параметры квадрата
square_vertices = [
    (-0.5, -0.5, 0),
    (0.5, -0.5, 0),
    (0.5, 0.5, 0),
    (-0.5, 0.5, 0)
]
square_colors = [
    (1.0, 1.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.2, 0.9, 1.0),
    (0.0, 1.0, 0.0)
]

# Параметры многоугольника (шестиугольник)
polygon_center = (0.0, 0.0, 0.0)
polygon_radius = 0.15
polygon_num_sides = 6
polygon_colors = [
    (0.8, 0.2, 0.8),  # Пурпурный
    (0.2, 0.8, 0.8),  # Голубой
    (0.8, 0.8, 0.2),  # Желтый
    (0.8, 0.2, 0.2),  # Красный
    (0.2, 0.8, 0.2),  # Зеленый
    (0.2, 0.2, 0.8)   # Синий
]

# Главная функция цикла отрисовки
while not glfw.window_should_close(window):
    clear_screen()

    # Обновление анимации
    current_time = time.time() - start_time
    triangle_rotation += 2.0
    square_scale = 0.8 + 0.3 * np.sin(current_time * 2)
    circle_offset = 0.2 * np.sin(current_time * 1.5)

    # Анимация многоугольника
    polygon_scale = 0.8 + 0.4 * np.sin(current_time * 1.2)
    polygon_rotation += 1.5 
    polygon_curve_time += 0.02
    polygon_position_x = 0.5 * np.sin(polygon_curve_time)
    polygon_position_y = curve_function(polygon_position_x)

    # Нарисовать вращающийся треугольник
    glPushMatrix()
    glRotatef(triangle_rotation, 0, 0, 1)
    draw_triangle(triangle_vertices, triangle_colors)
    glPopMatrix()

    # Нарисовать пульсирующий квадрат
    glPushMatrix()
    glScalef(square_scale, square_scale, 1.0)
    draw_quad(square_vertices, square_colors)
    glPopMatrix()

    # Нарисовать движущийся круг
    circle_center = (circle_offset, circle_offset, 0)
    circle_radius = 0.3 + 0.1 * np.cos(current_time)
    circle_num_sides = 50
    circle_color = (0.5 + 0.3 * np.sin(current_time), 0.5, 0.5 + 0.3 * np.cos(current_time))
    draw_polygon(circle_center, circle_radius, circle_num_sides, circle_color)

    glPushMatrix()
    glTranslatef(polygon_position_x, polygon_position_y, 0.0)
    glScalef(polygon_scale, polygon_scale, 1.0)
    glTranslatef(-polygon_rotation_point[0], -polygon_rotation_point[1], -polygon_rotation_point[2])
    glRotatef(polygon_rotation, 0, 0, 1)
    glTranslatef(polygon_rotation_point[0], polygon_rotation_point[1], polygon_rotation_point[2])
    draw_polygon(polygon_center, polygon_radius, polygon_num_sides, polygon_colors)
    glPopMatrix()
    glfw.swap_buffers(window)
    glfw.poll_events()

# Завершаем работу GLFW
glfw.terminate()
