from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import math

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL, RESIZABLE)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
rotation_speed = 0.1
rotation_x, rotation_y = 0, 0
mouse_x, mouse_y = 0, 0
mouse_down = False

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
    glColor3f(1, 0, 1) # Magenta
    for i in range(segments + 1):
        angle = i / segments * turns * 2 * math.pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = height * i / segments
        glVertex3f(x, y, z)
    glEnd()

def draw_dodecahedron(size):
    phi = (1 + math.sqrt(5)) / 2  # Золотое сечение
    vertices = [
        (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1),
        (0, phi, 1/phi), (0, phi, -1/phi), (0, -phi, 1/phi), (0, -phi, -1/phi),
        (1/phi, 0, phi), (-1/phi, 0, phi), (1/phi, 0, -phi), (-1/phi, 0, -phi),
        (phi, 1/phi, 0), (phi, -1/phi, 0), (-phi, 1/phi, 0), (-phi, -1/phi, 0)
    ]
    vertices = [(v[0] * size, v[1] * size, v[2] * size) for v in vertices]  # задаем масштаб вершинам
    faces = [(0, 8, 4, 13, 12), (1, 14, 15, 5, 9), (2, 10, 6, 13, 12), (3, 15, 7, 11, 14),
             (0, 16, 17, 2, 12), (1, 16, 17, 3, 14), (4, 18, 19, 6, 13), (5, 18, 19, 7, 15),
             (8, 0, 16, 9, 1), (10, 2, 17, 11, 3), (8, 4, 18, 10, 6), (9, 5, 19, 11, 7)]

    glBegin(GL_POLYGON)
    glColor3f(0.5, 0.5, 0.5)  # Серый
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

glEnable(GL_DEPTH_TEST)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
                mouse_x, mouse_y = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
        if event.type == pygame.MOUSEMOTION:
            if mouse_down:
                new_x, new_y = event.pos
                delta_x = new_x - mouse_x
                delta_y = new_y - mouse_y
                rotation_x += delta_y * rotation_speed
                rotation_y += delta_x * rotation_speed
                mouse_x, mouse_y = new_x, new_y
        if event.type == VIDEORESIZE:
            glViewport(0, 0, event.w, event.h)
            gluPerspective(45, (event.w / event.h), 0.1, 50.0)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)

    draw_axis()
    draw_cube(1, 1, 1)
    glTranslatef(2, 0, 0)
    draw_spiral(0.3, 2, 5, 100)
    glTranslatef(-2, 0, 0)
    glTranslatef(0, 2, 0)
    draw_dodecahedron(0.5)
    glTranslatef(0, -2, 0)

    pygame.display.flip()
    pygame.time.wait(10)
