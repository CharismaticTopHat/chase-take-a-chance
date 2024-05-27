import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')

# Import obj loader
from objloader import *

#Radio para colisión
radius = 2

screen_width = 800
screen_height = 800
# Campo visual para el observador
FOVY = 60.0
ZNEAR = 1.0
ZFAR = 900.0
# Variables para definir la posicion del observador
# gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
# Posición de la cámara del observador (Coordenadas)/Desde donde lo vemos
EYE_X = 0.0
EYE_Y = 5.0
EYE_Z = 0.0
# Punto de observación (Coordenadas)/A donde vemos
CENTER_X = 1.0
CENTER_Y = 5.0
CENTER_Z = 0.0
# Vector de orientación
UP_X = 0
UP_Y = 1
UP_Z = 0
# Variables para dibujar los ejes del sistema
X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500
Z_MIN = -500
Z_MAX = 500
# Dimension del plano
DimBoard = 200

objetos = []

# Variable de control observador - Cambia cómo ve el usuario
dir = [1.0, 0.0, 0.0]

# Variables para el control del observador
theta = 0.0
radius = 300

pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    # X axis in red
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0.0, 0.0)
    glVertex3f(X_MAX, 0.0, 0.0)
    glEnd()
    # Y axis in green
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()
    # Z axis in blue
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
    glEnd()
    glLineWidth(1.0)


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Chase: Take a Chance")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    #glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 200, 0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded        
    objetos.append(OBJ("School_map.obj", swapyz=True))
    objetos[0].generate()


def lookAt():
    global dir
    global theta
    # 1. Transformar Theta a Radianes
    rad = math.radians(theta)
    # 2. Multiplicar la matriz de rotación en Y con vector de dir
    dir[0] = math.cos(rad)
    dir[2] = math.sin(rad)
    # 3. Center recibe la operación de Eye + Dir

def displayobj():
    glPushMatrix()  
    #correcciones para dibujar el objeto en plano XZ
    #esto depende de cada objeto
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, 15.0)
    glScale(10.0,10.0,10.0)
    objetos[0].render()  
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    # Se dibuja el plano gris
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    
    displayobj()
    
done = False
Init()
while not done:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
            EYE_X = EYE_X + dir[0]
            EYE_Z = EYE_Z + dir[2]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
            glLoadIdentity()
            gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)        
    if keys[pygame.K_DOWN]:
            EYE_X = EYE_X - dir[0]
            EYE_Z = EYE_Z - dir[2]
            CENTER_X = EYE_X + dir[0]
            CENTER_Z = EYE_Z + dir[2]
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