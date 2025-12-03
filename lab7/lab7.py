import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from OpenGL.GLU import *
"""Управление экраном вращения осуществляется с помощью стрелоек"""
# Инициализация GLFW
if not glfw.init():
    raise Exception("Ошибка инициализации GLFW")

window = glfw.create_window(800, 600, "Робот в OpenGL", None, None)
if not window:
    glfw.terminate()
    raise Exception("Ошибка создания окна GLFW")

glfw.make_context_current(window)

# Углы поворота по осям
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0


# Функция для рисования куба
def draw_cube(size, color):
    glColor3fv(color)
    glBegin(GL_QUADS)
    # Передняя грань
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    # Задняя грань
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(-size, size, -size)
    # Верхняя грань
    glVertex3f(-size, size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    glVertex3f(-size, size, -size)
    # Нижняя грань
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, -size, -size)
    glVertex3f(-size, -size, -size)
    # Левая грань
    glVertex3f(-size, -size, size)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    # Правая грань
    glVertex3f(size, -size, size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glEnd()


# Функция для рисования сферы
def draw_sphere(radius, color):
    glColor3fv(color)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    gluDeleteQuadric(quadric)


# Функция для рисования цилиндра
def draw_cylinder(radius, height, color):
    glColor3fv(color)
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, radius, height, 32, 32)
    gluDeleteQuadric(quadric)


# Функция для рисования робота
def draw_robot():
    # Голова (сфера)
    glPushMatrix()
    glTranslatef(0, 1.5, 0)
    draw_sphere(0.5, (1.0, 0.0, 0.0))
    glPopMatrix()

    # Тело (куб)
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    draw_cube(1.0, (0.0, 1.0, 0.0))
    glPopMatrix()

    # Руки (цилиндры)
    glPushMatrix()
    glTranslatef(-1.0, 0.5, 0)
    glRotatef(-90, 0, 1.0, 0)
    draw_cylinder(0.2, 1.0, (0.0, 0.0, 1.0))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.0, 0.5, 0)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(0.2, 1.0, (0.0, 0.0, 1.0))
    glPopMatrix()

    # Ноги (цилиндры)
    glPushMatrix()
    glTranslatef(-0.5, -0.5, 0)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.2, 1.0, (1.0, 1.0, 0.0))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.5, -0.5, 0)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.2, 1.0, (1.0, 1.0, 0.0))
    glPopMatrix()


# Главная функция цикла отрисовки
def render():
    global angle_x, angle_y, angle_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Установка вида
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glTranslatef(0, 0, -5)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    # Рисование робота
    draw_robot()

    glfw.swap_buffers(window)
    glfw.poll_events()


# Обработка событий клавиатуры
def key_callback(window, key, scancode, action, mods):
    global angle_x, angle_y, angle_z
    if action == glfw.PRESS:
        if key == glfw.KEY_UP:
            angle_x += 5
        elif key == glfw.KEY_DOWN:
            angle_x -= 5
        elif key == glfw.KEY_LEFT:
            angle_y += 5
        elif key == glfw.KEY_RIGHT:
            angle_y -= 5
        elif key == glfw.KEY_Q:
            angle_z += 5
        elif key == glfw.KEY_W:
            angle_z -= 5


glfw.set_key_callback(window, key_callback)

# Основной цикл
while not glfw.window_should_close(window):
    render()

# Завершаем работу GLFW
glfw.terminate()