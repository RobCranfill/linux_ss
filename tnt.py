"""
from https://www.reddit.com/r/pygame/comments/15xk7d1/trying_to_make_a_multimonitor_screensaver/
and https://pastebin.com/GF2fyBPy

urk - requires opengl

"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

def tesseract_vertices():
    return np.array([
        [-1, -1, -1, -1],
        [-1, -1, -1,  1],
        [-1, -1,  1, -1],
        [-1, -1,  1,  1],
        [-1,  1, -1, -1],
        [-1,  1, -1,  1],
        [-1,  1,  1, -1],
        [-1,  1,  1,  1],
        [ 1, -1, -1, -1],
        [ 1, -1, -1,  1],
        [ 1, -1,  1, -1],
        [ 1, -1,  1,  1],
        [ 1,  1, -1, -1],
        [ 1,  1, -1,  1],
        [ 1,  1,  1, -1],
        [ 1,  1,  1,  1],
    ])

def tesseract_edges():
    return (
        (0, 1), (0, 2), (0, 4), (0, 8),
        (1, 3), (1, 5), (1, 9),
        (2, 3), (2, 6), (2, 10),
        (3, 7), (3, 11),
        (4, 5), (4, 6), (4, 12),
        (5, 7), (5, 13),
        (6, 7), (6, 14),
        (7, 15),
        (8, 9), (8, 10), (8, 12),
        (9, 11), (9, 13),
        (10, 11), (10, 14),
        (11, 15),
        (12, 13), (12, 14),
        (13, 15),
        (14, 15)
    )

def tesseract_faces():
    return [
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (0, 1, 3, 2),
        (4, 5, 7, 6),
        (0, 2, 6, 4),
        (1, 3, 7, 5),
        (8, 9, 13, 12),
        (10, 11, 15, 14),
        (8, 9, 11, 10),
        (12, 13, 15, 14),
        (8, 10, 14, 12),
        (9, 11, 15, 13),
        (0, 1, 9, 8),
        (2, 3, 11, 10),
        (0, 2, 10, 8),
        (1, 3, 11, 9),
        (4, 5, 13, 12),
        (6, 7, 15, 14),
        (4, 6, 14, 12),
        (5, 7, 15, 13),
    ]

def draw_tesseract(vertices, edges, faces, colors):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv(colors[vertex])
            glVertex3fv(vertices[vertex][:3])
    glEnd()

    glBegin(GL_POLYGON)
    for face in faces:
        for vertex in face:
            glColor4fv(np.append(colors[vertex], 0.5)) # Set opacity to 50%
            glVertex3fv(vertices[vertex][:3])
    glEnd()

def project_4d_to_3d(vertices, w):
    projection_matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1,  0]
    ])
    return np.dot(vertices, projection_matrix.T)


def rotation_matrix_4d(angle, axis1, axis2):
    c = np.cos(angle)
    s = np.sin(angle)
    mat = np.identity(4)
    mat[axis1, axis1] = c
    mat[axis1, axis2] = -s
    mat[axis2, axis1] = s
    mat[axis2, axis2] = c
    return mat

def main():
    pygame.init()
    display = (1920, 1080)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    clock = pygame.time.Clock()
    angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        vertices_4d = tesseract_vertices()

        colors = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 1],
            [0.5, 0.5, 0.5],
            [1, 0.5, 0],
            [0.5, 1, 0],
            [0, 0.5, 1],
            [1, 1, 0.5],
            [1, 0.5, 1],
            [0.5, 1, 1],
            [1, 0.5, 0.5],
            [0.5, 1, 0.5]
        ])

        _rotate_xw = rotation_matrix_4d(angle, 0, 3)
        _rotate_yw = rotation_matrix_4d(angle, 1, 3)
        _rotate_zw = rotation_matrix_4d(angle, 2, 3)

        vertices_4d = vertices_4d.dot(_rotate_xw).dot(_rotate_yw).dot(_rotate_zw)

        vertices_3d = project_4d_to_3d(vertices_4d, 2)
        edges = tesseract_edges()
        faces = tesseract_faces()

        glEnable(GL_BLEND) # Enable blending
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # Enable transparency

        draw_tesseract(vertices_3d, edges, faces, colors)

        pygame.display.flip()
        clock.tick(165)
        angle += 0.01 * (60 / 165)

if __name__ == "__main__":
    main()
