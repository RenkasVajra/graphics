import glfw
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from OpenGL.GLU import *
"""
Управление танком:
Стрелки - вращение вида
Q/W - вращение вокруг оси Z
R - сброс вида
"""
# Инициализация GLFW
if not glfw.init():
    raise Exception("Ошибка инициализации GLFW")

window = glfw.create_window(1000, 700, "Автомат Калашникова в OpenGL", None, None)
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


# Дополнительные вспомогательные функции для АК-47
def draw_cone(radius, height, color):
    """Рисует конус"""
    glColor3fv(color)
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, 0.0, height, 32, 32)
    gluDeleteQuadric(quadric)


def draw_disk(inner_radius, outer_radius, color):
    """Рисует плоский диск"""
    glColor3fv(color)
    quadric = gluNewQuadric()
    gluDisk(quadric, inner_radius, outer_radius, 32, 1)
    gluDeleteQuadric(quadric)


def draw_partial_torus(inner_radius, outer_radius, start_angle, sweep_angle, color):
    """Рисует частичный тор"""
    glColor3fv(color)
    quadric = gluNewQuadric()
    gluPartialDisk(quadric, inner_radius, outer_radius, 32, 1, start_angle, sweep_angle)
    gluDeleteQuadric(quadric)


def draw_truncated_cone(bottom_radius, top_radius, height, color):
    """Рисует усеченный конус"""
    glColor3fv(color)
    quadric = gluNewQuadric()
    gluCylinder(quadric, bottom_radius, top_radius, height, 32, 32)
    gluDeleteQuadric(quadric)


def draw_torus(inner_radius, outer_radius, color):
    """Рисует тор (кольцо)"""
    glColor3fv(color)
    quadric = gluNewQuadric()
    gluDisk(quadric, inner_radius, outer_radius, 32, 1)
    gluDeleteQuadric(quadric)


def draw_curved_surface(width, height, depth, curvature, color):
    """Рисует изогнутую поверхность с помощью сегментов"""
    glColor3fv(color)
    segments = 8
    for i in range(segments):
        for j in range(segments):
            # Создаем криволинейную поверхность
            x1 = (i / segments - 0.5) * width
            y1 = (j / segments - 0.5) * height
            z1 = curvature * (x1**2 + y1**2)

            x2 = ((i+1) / segments - 0.5) * width
            y2 = (j / segments - 0.5) * height
            z2 = curvature * (x2**2 + y2**2)

            x3 = ((i+1) / segments - 0.5) * width
            y3 = ((j+1) / segments - 0.5) * height
            z3 = curvature * (x3**2 + y3**2)

            x4 = (i / segments - 0.5) * width
            y4 = ((j+1) / segments - 0.5) * height
            z4 = curvature * (x4**2 + y4**2)

            glBegin(GL_QUADS)
            glVertex3f(x1, y1, z1 + depth/2)
            glVertex3f(x2, y2, z2 + depth/2)
            glVertex3f(x3, y3, z3 + depth/2)
            glVertex3f(x4, y4, z4 + depth/2)
            glEnd()


def draw_rounded_corner(radius, segments, color):
    glColor3fv(color)
    for i in range(segments):
        angle1 = i * 3.14159 / 2 / segments
        angle2 = (i + 1) * 3.14159 / 2 / segments

        x1 = radius * (1 - math.cos(angle1))
        y1 = radius * (1 - math.sin(angle1))
        x2 = radius * (1 - math.cos(angle2))
        y2 = radius * (1 - math.sin(angle2))

        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(x1, 0, 0)
        glVertex3f(x2, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, y1, 0)
        glVertex3f(0, y2, 0)
        glEnd()


def draw_organic_shape(length, width, height, color):
    glColor3fv(color)
    segments = 12

    for i in range(segments):
        t1 = i / segments
        t2 = (i + 1) / segments

        # S-образная кривая
        x1 = t1 * length - length/2
        y1 = height/2 * math.sin(t1 * 3.14159 * 2)
        z1 = 0

        x2 = t2 * length - length/2
        y2 = height/2 * math.sin(t2 * 3.14159 * 2)
        z2 = 0

        glBegin(GL_QUADS)
        glVertex3f(x1, y1, z1 - width/2)
        glVertex3f(x2, y2, z2 - width/2)
        glVertex3f(x2, y2, z2 + width/2)
        glVertex3f(x1, y1, z1 + width/2)
        glEnd()


def draw_rifle():
    glPushMatrix()
    glTranslatef(0, 0, 0)


    glPushMatrix()
    glTranslatef(0, 0.08, 0)
    glScalef(0.8, 0.12, 0.3)
    draw_cube(1.0, (0.55, 0.55, 0.55))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -0.02, 0)
    glScalef(0.82, 0.16, 0.32)
    draw_cube(1.0, (0.55, 0.55, 0.55))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -0.14, 0)
    glScalef(0.75, 0.08, 0.28)
    draw_cube(1.0, (0.55, 0.55, 0.55))
    glPopMatrix()


    glPushMatrix()
    glTranslatef(0.38, 0, 0)
    glRotatef(15, 0, 1, 0)
    glScalef(0.04, 0.32, 0.3)
    draw_cube(1.0, (0.55, 0.55, 0.55))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.38, 0, 0)
    glRotatef(-15, 0, 1, 0)
    glScalef(0.04, 0.32, 0.3)
    draw_cube(1.0, (0.55, 0.55, 0.55))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.38, 0.14, 0.14)
    draw_sphere(0.04, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.38, 0.14, 0.14)
    draw_sphere(0.04, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.38, -0.14, 0.14)
    draw_sphere(0.04, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.38, -0.14, 0.14)
    draw_sphere(0.04, (0.5, 0.5, 0.5))
    glPopMatrix()

    # Крышка ствольной коробки с рифлением
    glPushMatrix()
    glTranslatef(0, 0.22, 0)
    glScalef(0.82, 0.02, 0.32)
    draw_cube(1.0, (0.5, 0.5, 0.5))
    glPopMatrix()

    for i in range(6):
        glPushMatrix()
        glTranslatef(-0.3 + i * 0.1, 0.23, 0)
        glScalef(0.02, 0.01, 0.3)
        draw_cube(1.0, (0.45, 0.45, 0.45))
        glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.2, -0.1, 0)
    glScalef(0.3, 0.2, 0.25)
    draw_cube(1.0, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.35, -0.05, 0)
    draw_cylinder(0.08, 0.1, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.2, 0.15, 0.13)
    glScalef(0.08, 0.04, 0.06)
    draw_cube(1.0, (0.3, 0.3, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.3, -0.08, 0)
    glScalef(0.15, 0.08, 0.25)
    draw_cube(1.0, (0.55, 0.55, 0.55))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.25, 0.05, 0.16)
    glScalef(0.04, 0.04, 0.04)
    draw_cube(1.0, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.25, 0.05, -0.16)
    glScalef(0.04, 0.04, 0.04)
    draw_cube(1.0, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.05, -0.25, 0)
    glScalef(0.15, 0.08, 0.25)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.15, 0.08, 0.15)
    glScalef(0.06, 0.04, 0.03)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.15, 0.08, -0.15)
    glScalef(0.06, 0.04, 0.03)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.6, 0, 0)
    glRotatef(90, 0, 1, 0)

    draw_cylinder(0.035, 1.8, (0.4, 0.4, 0.4))

    glPushMatrix()
    glTranslatef(0, 0, -0.1)
    draw_truncated_cone(0.045, 0.035, 0.1, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, 1.8)

    draw_cylinder(0.04, 0.08, (0.3, 0.3, 0.3))

    glPushMatrix()
    glTranslatef(0, 0.02, 0)
    glScalef(0.06, 0.02, 0.03)
    draw_cube(1.0, (0.25, 0.25, 0.25))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.02, 0, 0)
    glScalef(0.02, 0.04, 0.03)
    draw_cube(1.0, (0.25, 0.25, 0.25))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.02, 0, 0)
    glScalef(0.02, 0.04, 0.03)
    draw_cube(1.0, (0.25, 0.25, 0.25))
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.8, 0.08, 0)
    glRotatef(90, 0, 1, 0)

    draw_cylinder(0.025, 0.6, (0.5, 0.5, 0.5))

    glPushMatrix()
    glTranslatef(0, 0, 0.3)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.035, 0.03, (0.45, 0.45, 0.45))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.9, 0.08, 0)
    draw_cylinder(0.04, 0.08, (0.45, 0.45, 0.45))

    glPushMatrix()
    glTranslatef(0, 0.05, 0)
    draw_cylinder(0.045, 0.02, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.85, 0.08, 0)
    draw_cylinder(0.03, 0.04, (0.5, 0.5, 0.5))
    glPopMatrix()


    glPushMatrix()
    glTranslatef(1.75, 0.12, 0)
    glScalef(0.02, 0.08, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.7, 0.06, 0)
    glScalef(0.08, 0.04, 0.04)
    draw_cube(1.0, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.2, 0.15, 0)
    glScalef(0.15, 0.06, 0.03)
    draw_cube(1.0, (0.5, 0.5, 0.5))

    glPushMatrix()
    glTranslatef(0, 0.02, 0)
    glScalef(0.08, 0.02, 0.04)
    draw_cube(1.0, (0.1, 0.1, 0.1))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.8, -0.08, 0)

    glPushMatrix()
    glScalef(0.6, 0.08, 0.25)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -0.04, 0)
    glScalef(0.6, 0.04, 0.22)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, 0.12)
    glScalef(0.6, 0.12, 0.01)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, -0.12)
    glScalef(0.6, 0.12, 0.01)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.2, -0.08, 0)
    glScalef(0.15, 0.12, 0.2)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.0, -0.02, -0.12)
    glScalef(0.04, 0.04, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.2, 0, 0)


    glPushMatrix()
    glTranslatef(0, 0.08, 0)
    glScalef(0.7, 0.08, 0.25)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -0.02, 0)
    glScalef(0.75, 0.12, 0.28)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -0.12, 0)
    glScalef(0.6, 0.08, 0.22)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.35, 0, 0)
    glScalef(0.12, 0.25, 0.2)
    draw_cube(1.0, (0.35, 0.3, 0.25))

    glPushMatrix()
    glTranslatef(-0.35, -0.12, 0.02)

    glPushMatrix()
    glScalef(0.03, 0.06, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.015, -0.02, 0)
    glRotatef(-15, 0, 0, 1)
    glScalef(0.015, 0.03, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.005, 0.02, 0)
    glScalef(0.02, 0.02, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.8, -0.08, -0.12)
    glScalef(0.04, 0.08, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.5, -0.2, 0)

  
    glPushMatrix()
    glRotatef(15, 0, 0, 1)  
    glScalef(0.1, 0.32, 0.06)  
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -0.2, 0)
    glRotatef(10, 0, 0, 1)  
    glScalef(0.09, 0.12, 0.055)  
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.03, -0.08, 0)
    glRotatef(25, 0, 0, 1)
    glScalef(0.06, 0.18, 0.05)  
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()


    glPushMatrix()
    glTranslatef(-0.02, 0.06, 0)
    glRotatef(-10, 0, 0, 1)
    glScalef(0.08, 0.08, 0.05)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.02, -0.05, 0.03)
    draw_sphere(0.025, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.02, -0.05, -0.03)
    draw_sphere(0.025, (0.4, 0.35, 0.3))
    glPopMatrix()

    for i in range(7): 
        glPushMatrix()
        glTranslatef(-0.02 + i * 0.008, -0.02, 0.03)
        glScalef(0.003, 0.28, 0.005)  
        draw_cube(1.0, (0.35, 0.3, 0.25))
        glPopMatrix()

    glPopMatrix()


    glPushMatrix()
    glTranslatef(-0.3, -0.15, 0)
    glScalef(0.08, 0.1, 0.05)
    draw_cube(1.0, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.4, -0.08, 0)
    glScalef(0.2, 0.08, 0.08)
    draw_cube(1.0, (0.45, 0.45, 0.45))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.35, -0.12, 0.02)
    glScalef(0.03, 0.06, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.1, -0.25, 0)

    
    for i in range(20):  
        angle = math.sin(i * 0.18) * 22  
        glPushMatrix()
        glTranslatef(0, i * 0.045, 0)  
        glRotatef(angle, 0, 0, 1) 
        glScalef(0.12, 0.045, 0.08)
        draw_cube(1.0, (0.3, 0.3, 0.3))
        glPopMatrix()


        if i < 19:  
            glPushMatrix()
            glTranslatef(0.055, i * 0.045 + 0.0225, 0)
            draw_sphere(0.015, (0.3, 0.3, 0.3))
            glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0.95, 0)  
    glRotatef(5, 0, 0, 1)
    glScalef(0.13, 0.02, 0.09)
    draw_cube(1.0, (0.35, 0.35, 0.35))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -0.02, 0)
    glScalef(0.13, 0.02, 0.09)
    draw_cube(1.0, (0.35, 0.35, 0.35))

    glPushMatrix()
    glTranslatef(-0.06, 0, 0)
    glScalef(0.03, 0.03, 0.02)
    draw_cube(1.0, (0.3, 0.3, 0.3))
    glPopMatrix()

    glPopMatrix()

    for i in range(15):
        glPushMatrix()
        glTranslatef(0.055, i * 0.045 - 0.02, 0)
        glScalef(0.008, 0.04, 0.09)
        draw_cube(1.0, (0.25, 0.25, 0.25))
        glPopMatrix()

        if i > 0 and i < 14:
            glPushMatrix()
            glTranslatef(0, i * 0.045, 0.035)
            glScalef(0.03, 0.015, 0.005)
            draw_cube(1.0, (0.2, 0.2, 0.2))
            glPopMatrix()


    for i in range(22):  
        angle_offset = math.sin(i * 0.18) * 14  
        glPushMatrix()

        glTranslatef(0, i * 0.045, 0) 
        glRotatef(angle_offset, 0, 0, 1)

        glPushMatrix()
        glScalef(0.08, 0.022, 0.022)
        draw_cube(1.0, (0.9, 0.8, 0.1))
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.04, 0, 0)
        glScalef(0.005, 0.025, 0.025)
        draw_cube(1.0, (0.8, 0.7, 0.08))
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.042, 0, 0)
        draw_cone(0.01, 0.015, (0.2, 0.2, 0.2))
        glPopMatrix()

        glPopMatrix()

    glPopMatrix()


    glPushMatrix()
    glTranslatef(1.0, 0.08, -0.15)
    glScalef(0.04, 0.04, 0.08)
    draw_cube(1.0, (0.2, 0.2, 0.2))

    glPushMatrix()
    glTranslatef(0, 0, 0.04)
    draw_torus(0.02, 0.01, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.0, 0.08, -0.15)
    glScalef(0.04, 0.04, 0.08)
    draw_cube(1.0, (0.2, 0.2, 0.2))

    glPushMatrix()
    glTranslatef(0, 0, 0.04)
    draw_torus(0.02, 0.01, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.9, -0.08, 0)

    glPushMatrix()
    glScalef(0.15, 0.02, 0.04)
    draw_cube(1.0, (0.8, 0.8, 0.8))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.08, 0, 0)
    glScalef(0.06, 0.03, 0.03)
    draw_cube(1.0, (0.4, 0.35, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.05, 0, 0)
    glScalef(0.02, 0.06, 0.02)
    draw_cube(1.0, (0.6, 0.6, 0.6))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.0, -0.05, 0)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(0.008, 0.4, (0.6, 0.6, 0.6))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.2, 0.18, 0.12)
    glScalef(0.08, 0.04, 0.04)
    draw_cube(1.0, (0.4, 0.4, 0.4))

    glPushMatrix()
    glTranslatef(0.04, 0.02, 0.02)
    glScalef(0.02, 0.02, 0.02)
    draw_cube(1.0, (0.3, 0.3, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0.02, 0.02)
    glScalef(0.02, 0.02, 0.02)
    draw_cube(1.0, (0.3, 0.3, 0.3)) 
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.04, 0.02, 0.02)
    glScalef(0.02, 0.02, 0.02)
    draw_cube(1.0, (0.6, 0.1, 0.1)) 
    glPopMatrix()

    glPopMatrix()


    glPushMatrix()
    glTranslatef(0.25, 0.15, 0.08)
    glScalef(0.03, 0.02, 0.04)
    draw_cube(1.0, (0.5, 0.5, 0.5))
    glPopMatrix()


    glPushMatrix()
    glTranslatef(0.35, 0.08, -0.08)
    glScalef(0.06, 0.04, 0.08)
    draw_cube(1.0, (0.45, 0.45, 0.45))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.35, -0.08, 0.08)
    glScalef(0.04, 0.06, 0.03)
    draw_cube(1.0, (0.5, 0.5, 0.5))

    glPushMatrix()
    glTranslatef(0, 0.03, 0)
    glScalef(0.02, 0.02, 0.04)
    draw_cube(1.0, (0.45, 0.45, 0.45))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.35, 0.08, -0.08)
    glScalef(0.06, 0.04, 0.08)
    draw_cube(1.0, (0.45, 0.45, 0.45))

    glPushMatrix()
    glTranslatef(0, 0, 0.04)
    glScalef(0.03, 0.02, 0.02)
    draw_cube(1.0, (0.2, 0.2, 0.2))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.15, 0.18, 0)
    glScalef(0.4, 0.02, 0.03)
    draw_cube(1.0, (0.5, 0.5, 0.5))

    for i in range(9):
        glPushMatrix()
        glTranslatef(i * 0.044 - 0.2, 0.01, 0)
        glScalef(0.008, 0.01, 0.04)
        draw_cube(1.0, (0.4, 0.4, 0.4))
        glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.3, -0.12, 0)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(0.008, 0.15, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.4, -0.05, 0.08)
    draw_cylinder(0.015, 0.02, (0.3, 0.3, 0.3))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1.7, -0.08, 0)
    glScalef(0.06, 0.02, 0.04)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.3, 0.05, -0.12)
    glScalef(0.08, 0.02, 0.01)
    draw_cube(1.0, (0.1, 0.1, 0.1))
    glPopMatrix()

    for i in range(4):
        angle = i * 90
        glPushMatrix()
        glTranslatef(0.3 * math.cos(math.radians(angle)), 0.3 * math.sin(math.radians(angle)), 0.2)
        draw_cylinder(0.005, 0.02, (0.3, 0.3, 0.3))
        glPopMatrix()

    glPushMatrix()
    glTranslatef(0.75, 0.05, 0)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(0.01, 0.02, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.3, 0.12, 0)
    glScalef(0.15, 0.06, 0.1)
    draw_cube(1.0, (0.5, 0.5, 0.5))

    glPushMatrix()
    glTranslatef(0.08, 0.04, 0)
    glScalef(0.02, 0.04, 0.08)
    draw_cube(1.0, (0.45, 0.45, 0.45))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.4, 0.18, 0.08)
    glRotatef(45, 0, 0, 1)
    glScalef(0.08, 0.04, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))

    for i in range(3):
        glPushMatrix()
        glTranslatef(i * 0.02 - 0.02, 0.02, 0.01)
        glScalef(0.015, 0.02, 0.005)
        draw_cube(1.0, (0.35, 0.35, 0.35))
        glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.25, 0.08, 0.1)
    glScalef(0.04, 0.08, 0.06)
    draw_cube(1.0, (0.5, 0.5, 0.5))

    glPushMatrix()
    glTranslatef(0, 0.04, 0)
    glScalef(0.03, 0.03, 0.04)
    draw_cube(1.0, (0.45, 0.45, 0.45))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.05, -0.12, 0.08)
    glScalef(0.04, 0.08, 0.03)
    draw_cube(1.0, (0.4, 0.4, 0.4))

    glPushMatrix()
    glTranslatef(0, 0.04, 0.015)
    glScalef(0.02, 0.02, 0.01)
    draw_cube(1.0, (0.35, 0.35, 0.35))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.15, 0.15, 0.12)
    glScalef(0.06, 0.04, 0.04)
    draw_cube(1.0, (0.6, 0.6, 0.6))

    glPushMatrix()
    glTranslatef(0.03, 0.02, 0.02)
    glScalef(0.02, 0.03, 0.02)
    draw_cube(1.0, (0.55, 0.55, 0.55))
    glPopMatrix()

    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.1, 0.08, 0)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(0.015, 0.4, (0.7, 0.7, 0.8)) 
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.1, 0.08, 0)

    glPushMatrix()
    glScalef(0.12, 0.04, 0.06)
    draw_cube(1.0, (0.5, 0.5, 0.5))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.08, 0.04, 0)
    glScalef(0.04, 0.02, 0.08)
    draw_cube(1.0, (0.45, 0.45, 0.45))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0.02, 0.03)
    glScalef(0.1, 0.01, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0.02, -0.03)
    glScalef(0.1, 0.01, 0.02)
    draw_cube(1.0, (0.4, 0.4, 0.4))
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()
def render():
    global angle_x, angle_y, angle_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluPerspective(45, (1000 / 700), 0.1, 50.0)
    glTranslatef(0, 0, -6)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    draw_rifle()

    glfw.swap_buffers(window)
    glfw.poll_events()


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
        elif key == glfw.KEY_R:
            angle_x, angle_y, angle_z = 0, 0, 0


glfw.set_key_callback(window, key_callback)

while not glfw.window_should_close(window):
    render()

glfw.terminate()