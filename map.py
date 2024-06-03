import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import sys
import csv

sys.path.append('..')

screen_width = 800
screen_height = 800
FOVY = 60.0
ZNEAR = 1.0
ZFAR = 900.0
EYE_X = 100
EYE_Y = 15
EYE_Z = 100
CENTER_X = 1.0
CENTER_Y = 15
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
DimBoard = 600
dir = [0.0, 0.0, 1.0]

theta = 300
radius = 0
player_x = 0
player_z = 0
speed = 10
giroSpeed = 10

pygame.init()


def load_map(filename):
    map_data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            map_data.append([int(cell) for cell in row])
    return map_data

map_data = load_map('map.csv')


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
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def lookAt():
    global dir
    global theta
    rad = math.radians(theta)
    dir[0] = math.cos(rad)*speed
    dir[2] = math.sin(rad)*speed


def prepare_wall_vertices(map_data):
    wall_height = 30
    vertices = []
    for z, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == 1:
                vertices.extend([
                    # Frente
                    (x, 0, z), (x+1, 0, z), (x+1, wall_height, z), (x, wall_height, z),
                    # Atrás
                    (x, 0, z+1), (x+1, 0, z+1), (x+1, wall_height, z+1), (x, wall_height, z+1),
                    # Izquierda
                    (x, 0, z), (x, 0, z+1), (x, wall_height, z+1), (x, wall_height, z),
                    # Derecha
                    (x+1, 0, z), (x+1, 0, z+1), (x+1, wall_height, z+1), (x+1, wall_height, z),
                    # Arriba
                    (x, wall_height, z), (x+1, wall_height, z), (x+1, wall_height, z+1), (x, wall_height, z+1),
                ])
    return vertices

wall_vertices = prepare_wall_vertices(map_data)

def draw_walls(vertices):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    for vertex in vertices:
        glVertex3f(*vertex)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    draw_walls(wall_vertices)  # Llamada a la función para dibujar las paredes
    print(f"La posición en x es: {player_x}")
    print(f"La posición en z es: {player_z}")


done = False
Init()
while not done:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        EYE_X += dir[0]
        EYE_Z += dir[2]
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
        player_x = int(EYE_X)
        player_z = int(EYE_Z)
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    if keys[pygame.K_DOWN]:
        EYE_X -= dir[0]
        EYE_Z -= dir[2]
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
        player_x = int(EYE_X)
        player_z = int(EYE_Z)
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    if keys[pygame.K_RIGHT]:
        theta += giroSpeed
        lookAt()
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    if keys[pygame.K_LEFT]:
        theta -= giroSpeed
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
