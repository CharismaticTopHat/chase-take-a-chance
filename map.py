import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import csv
import ctypes
import time

# Import obj loader
from objloader import *
from Enemy import Enemy
from Collectable import Coin

sys.path.append('..')

screen_width = 800
screen_height = 800
FOVY = 60.0
ZNEAR = 1.0
ZFAR = 900.0
EYE_X = 400
EYE_Y = 15
EYE_Z = 310
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
playerSize = 5
player_x = 0
player_z = 0
speed = 10
giroSpeed = 10

collectedItems = 3

objetos = []

coin_locations = [[225, -227], [225, -327], [225, -427], [275, -227], [275, -327], [275, -427]]
coins = [Coin(Scale=1.0, locations=coin_locations) for _ in range(3)]

pesades = 3
ligeres = 5

GLUT_BITMAP_TIMES_ROMAN_24 = ctypes.c_int(7)

pygame.init()

def load_texture(filename):
    texture_surface = pygame.image.load(filename)
    texture_data = pygame.image.tostring(texture_surface, "RGB", True)
    width, height = texture_surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D, 0)  # Unbind the texture
    return texture_id

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
    global wall_texture
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Chase: Take A Chance")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    objetos.append(OBJ("HSpider.obj", swapyz=True))
    objetos[0].generate()
    for i in range(0, 3):
        objetos.append(OBJ("Coin.obj", swapyz=True))
    wall_texture = load_texture("wall_texture.jpg")

def lookAt():
    global dir
    global theta
    rad = math.radians(theta)
    dir[0] = math.cos(rad) * speed
    dir[2] = math.sin(rad) * speed

enemyStart = (30, 30)
enemyEnd = (400, 310)
enemy_instance = Enemy(vel=1, Scale=0.5, start=enemyStart, end=enemyEnd)

def displayobj():
    glDisable(GL_TEXTURE_2D)  # Desactivar texturas antes de renderizar la araña
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(enemy_instance.Position[0], -enemy_instance.Position[1], enemy_instance.Position[2])
    glScale(0.5, 0.5, 0.5)
    objetos[0].render()
    glPopMatrix()
    # No activar texturas aquí ya que solo queremos aplicarlas a las paredes

def checkCollision():
    euclidesDistance = math.sqrt(math.pow(player_x - enemy_instance.Position[0], 2) + math.pow(0 - 0, 2) + math.pow(player_z - enemy_instance.Position[2], 2))
    radioDistance = playerSize + enemy_instance.size
    if euclidesDistance < radioDistance:
        is_collision = True
    else:
        is_collision = False

def prepare_wall_vertices(map_data):
    wall_height = 100
    vertices = []
    for z, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == 0:  # Cambiar a 0 para indicar paredes
                # Frente
                vertices.append(((x, 0, z), (x + 1, 0, z), (x + 1, wall_height, z), (x, wall_height, z)))
                # Atrás
                vertices.append(((x, 0, z + 1), (x + 1, 0, z + 1), (x + 1, wall_height, z + 1), (x, wall_height, z + 1)))
                # Izquierda
                vertices.append(((x, 0, z), (x, 0, z + 1), (x, wall_height, z + 1), (x, wall_height, z)))
                # Derecha
                vertices.append(((x + 1, 0, z), (x + 1, 0, z + 1), (x + 1, wall_height, z + 1), (x + 1, wall_height, z)))
                # Arriba
                vertices.append(((x, wall_height, z), (x + 1, wall_height, z), (x + 1, wall_height, z + 1), (x, wall_height, z + 1)))
    return vertices

wall_vertices = prepare_wall_vertices(map_data)

def draw_walls(vertices):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, wall_texture)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    for quad in vertices:
        glTexCoord2f(0.0, 0.0)
        glVertex3f(*quad[0])
        glTexCoord2f(1.0, 0.0)
        glVertex3f(*quad[1])
        glTexCoord2f(1.0, 1.0)
        glVertex3f(*quad[2])
        glTexCoord2f(0.0, 1.0)
        glVertex3f(*quad[3])
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

def is_collision(new_x, new_z):
    global playerSize
    min_x, max_x = int(new_x - playerSize), int(new_x + playerSize)
    min_z, max_z = int(new_z - playerSize), int(new_z + playerSize)

    for x in range(min_x, max_x + 1):
        for z in range(min_z, max_z + 1):
            if x < 0 or x >= len(map_data[0]) or z < 0 or z >= len(map_data):
                return True  # Está fuera del mapa
            if map_data[z][x] == 0:  # Verifica si la celda es una pared
                return True
    return False

def is_collision_with_enemy(player_x, player_z):
    euclidean_distance = math.sqrt((player_x - enemy_instance.MassCenter[0]) ** 2 + (player_z - abs(enemy_instance.MassCenter[1])) ** 2)
    return euclidean_distance < (playerSize + enemy_instance.size)

def display():
    global collectedItems
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    draw_walls(wall_vertices)
    print(f"JUGADOR en x es: {player_x}")
    print(f"JUGADOR en z es: {player_z}")
    print(f"ENEMIGO en x es: {int(enemy_instance.Position[0])}")
    print(f"ENEMIGO en z es: {int(enemy_instance.Position[1])}")
    enemy_instance.update(new_end=(int(player_x), int(player_z)))
    displayobj()

    for i, coin in enumerate(coins):
        glPushMatrix()
        glRotatef(-90.0, 1.0, 0.0, 0.0)
        glTranslatef(coin.Position[0], coin.Position[1], coin.Position[2])
        glScale(0.5, 0.5, 0.5)
        objetos[i + 1].render()
        glPopMatrix()

    if is_collision_with_enemy(player_x, player_z):
        show_game_over_message()
    if is_collision_with_coins(player_x, player_z):
        collectedItems -= 1
        if collectedItems == 0:
            show_you_win_message()

def is_collision_with_coins(player_x, player_z):
    global collectedItems
    global speed
    for coin in coins:
        euclidean_distance = math.sqrt((player_x - coin.MassCenter[0]) ** 2 + (player_z - abs(coin.MassCenter[1])) ** 2)
        if euclidean_distance < (playerSize + coin.size):
            coins.remove(coin)
            speed -= pesades
            enemy_instance.vel += ligeres
            return True
    return False

def show_you_win_message():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, screen_width, 0, screen_height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3f(0.0, 1.0, 0.0)
    glRasterPos2i(screen_width // 2 - 70, screen_height // 2)
    message = "You win!"
    x = screen_width // 2 - 70
    y = screen_height // 2
    for char in message:
        glRasterPos2i(x, y)
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ctypes.c_int(ord(char)))
        x += glutBitmapWidth(GLUT_BITMAP_TIMES_ROMAN_24, ctypes.c_int(ord(char)))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def show_game_over_message():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, screen_width, 0, screen_height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2i(screen_width // 2 - 50, screen_height // 2)
    message = "Game Over"
    x = screen_width // 2 - 50
    y = screen_height // 2
    for char in message:
        glRasterPos2i(x, y)
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ctypes.c_int(ord(char)))
        x += glutBitmapWidth(GLUT_BITMAP_TIMES_ROMAN_24, ctypes.c_int(ord(char)))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

done = False
Init()
while not done:
    keys = pygame.key.get_pressed()
    new_eye_x, new_eye_z = EYE_X, EYE_Z
    if keys[pygame.K_UP]:
        new_eye_x += dir[0]
        new_eye_z += dir[2]
    if keys[pygame.K_DOWN]:
        new_eye_x -= dir[0]
        new_eye_z -= dir[2]
    if keys[pygame.K_RIGHT]:
        theta += giroSpeed
        lookAt()
    if keys[pygame.K_LEFT]:
        theta -= giroSpeed
        lookAt()

    if not is_collision(new_eye_x, new_eye_z):
        EYE_X, EYE_Z = new_eye_x, new_eye_z
        CENTER_X = EYE_X + dir[0]
        CENTER_Z = EYE_Z + dir[2]
        player_x = int(EYE_X)
        player_z = int(EYE_Z)
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
