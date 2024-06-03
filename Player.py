import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import sys
sys.path.append('..')

<<<<<<< Updated upstream
=======
# Import obj loader
from objloader import *

#Radio para colisión
radius = 2

#Centro de masa
MCx = 0
MCz = 0

>>>>>>> Stashed changes
screen_width = 800
screen_height = 800
FOVY = 60.0
ZNEAR = 1.0
ZFAR = 900.0
EYE_X = 0.0
EYE_Y = 5.0
EYE_Z = 0.0
CENTER_X = 1.0
CENTER_Y = 5.0
CENTER_Z = 0.0
UP_X = 0
UP_Y = 1
UP_Z = 0
X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500
Z_MIN = -500
Z_MAX = 500
DimBoard = 300
dir = [0.0, 0.0, 1.0]

<<<<<<< Updated upstream
theta = 300
radius = 0
player_x = 0
player_z = 0
=======
objetos = []

# Variable de control observador - Cambia cómo ve el usuario, Vector de Dirección
dir = [1.0, 0.0, 0.0]

# Variables para el control del observador
theta = 0.0
radius = 300
>>>>>>> Stashed changes

pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0.0, 0.0)
    glVertex3f(X_MAX, 0.0, 0.0)
    glEnd()
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
<<<<<<< Updated upstream
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
=======
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)   

>>>>>>> Stashed changes

def lookAt():

    global dir
    global theta
    rad = math.radians(theta)
    dir[0] = math.cos(rad)
    dir[2] = math.sin(rad)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    print(f"la posición en x es: {player_x}")
    print(f"la posición en z es: {player_z}")
    glEnd()

done = False
Init()
while not done:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        EYE_X += dir[0]
        EYE_Z += dir[2]
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
        player_x = EYE_X
        player_z = EYE_Z
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    if keys[pygame.K_DOWN]:
        EYE_X -= dir[0]
        EYE_Z -= dir[2]
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
        player_x = EYE_X
        player_z = EYE_Z
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    if keys[pygame.K_RIGHT]:
        theta += 1
        lookAt()
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    if keys[pygame.K_LEFT]:
        theta -= 1
        lookAt()
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
