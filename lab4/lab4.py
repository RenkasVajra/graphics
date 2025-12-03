import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np


if not glfw.init():
    raise Exception("Ошибка инициализации GLFW")

window = glfw.create_window(800, 600, "Треугольник Серпинского", None, None)
if not window:
    glfw.terminate()
    raise Exception("Ошибка создания окна GLFW")

glfw.make_context_current(window)


# Функция для рисования треугольника
def draw_triangle(vertices):
    glBegin(GL_TRIANGLES)
    for vertex in vertices:
        glVertex2fv(vertex)
    glEnd()


# Функция для построения треугольника Серпинского
def sierpinski(vertices, level):
    if level == 0:
        draw_triangle(vertices)
    else:
        v1, v2, v3 = vertices
        v12 = (v1 + v2) / 2
        v23 = (v2 + v3) / 2
        v31 = (v3 + v1) / 2

        sierpinski([v1, v12, v31], level - 1)
        sierpinski([v12, v2, v23], level - 1)
        sierpinski([v31, v23, v3], level - 1)


# Главная функция цикла отрисовки
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Установка вида
    glOrtho(-1, 1, -1, 1, -1, 1)

    # Вершины исходного треугольника
    vertices = np.array([
        [-0.5, -0.5],
        [0.5, -0.5],
        [0.0, 0.5]
    ], dtype=np.float32)

    # Уровень рекурсии
    level = 5

    # Построение треугольника Серпинского
    sierpinski(vertices, level)

    glfw.swap_buffers(window)
    glfw.poll_events()


# Основной цикл
while not glfw.window_should_close(window):
    render()

# Завершаем работу GLFW
glfw.terminate()