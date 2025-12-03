import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Инициализация GLFW
if not glfw.init():
    raise Exception("Ошибка инициализации GLFW")

window = glfw.create_window(800, 600, "Простые фигуры в OpenGL", None, None)
if not window:
    glfw.terminate()
    raise Exception("Ошибка создания окна GLFW")

glfw.make_context_current(window)


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

# Главная функция цикла отрисовки
while not glfw.window_should_close(window):
    clear_screen()

    # Нарисовать треугольник
    draw_triangle(triangle_vertices, triangle_colors)

    # Нарисовать квадрат
    draw_quad(square_vertices, square_colors)

    # Нарисовать круг 
    circle_center = (0, 0, 0)
    circle_radius = 0.5
    circle_num_sides = 50
    circle_color = (0.5, 0.5, 0.5)
    draw_polygon(circle_center, circle_radius, circle_num_sides, circle_color)

    # Освобождаем буфер кадра
    glfw.swap_buffers(window)
    glfw.poll_events()

# Завершаем работу GLFW
glfw.terminate()
