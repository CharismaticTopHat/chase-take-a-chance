import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import csv
import cv2
from moviepy.editor import VideoFileClip
import ctypes
import time
import sys
from objloader import *
from Enemy import Enemy
from Collectable import Coin

sys.path.append('..')

screen_width = 1000
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
ligeres = 2

GLUT_BITMAP_TIMES_ROMAN_24 = ctypes.c_int(7)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
edo_game = 0


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
    global wall_texture, spider_texture
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
    spider_texture = load_texture("spider_texture.jpg")  # Cargar la textura de la araña

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
    glEnable(GL_TEXTURE_2D)  # Activar texturas antes de renderizar la araña
    glBindTexture(GL_TEXTURE_2D, spider_texture)  # Bind la textura de la araña
    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(enemy_instance.Position[0], -enemy_instance.Position[1], enemy_instance.Position[2])
    glScale(0.5, 0.5, 0.5)
    objetos[0].render()
    glPopMatrix()
    glBindTexture(GL_TEXTURE_2D, 0)  # Unbind la textura
    glDisable(GL_TEXTURE_2D)  # Desactivar texturas después de renderizar la araña


def checkCollision():
    euclidesDistance = math.sqrt(math.pow(player_x - enemy_instance.Position[0], 2) + math.pow(0 - 0, 2) + math.pow(
        player_z - enemy_instance.Position[2], 2))
    radioDistance = playerSize + enemy_instance.size
    if euclidesDistance < radioDistance:
        is_collision = True
    else:
        is_collision = False


def prepare_wall_vertices(map_data):
    wall_height = 100
    vertices = []
    visited = set()

    def add_quad(v):
        vertices.append(v)

    for z in range(len(map_data)):
        for x in range(len(map_data[0])):
            if map_data[z][x] == 0 and (x, z) not in visited:
                # Encontrar el máximo ancho
                max_width = 0
                while x + max_width < len(map_data[0]) and map_data[z][x + max_width] == 0:
                    max_width += 1

                # Encontrar el máximo alto para este ancho
                max_height = 0
                while z + max_height < len(map_data) and all(
                        map_data[z + max_height][x + w] == 0 for w in range(max_width)):
                    max_height += 1

                # Agregar los vértices de la pared fusionada
                for i in range(max_height):
                    for j in range(max_width):
                        visited.add((x + j, z + i))

                # Frente
                add_quad(((x, 0, z), (x + max_width, 0, z), (x + max_width, wall_height, z), (x, wall_height, z)))
                # Atrás
                add_quad(((x, 0, z + max_height), (x + max_width, 0, z + max_height),
                          (x + max_width, wall_height, z + max_height), (x, wall_height, z + max_height)))
                # Izquierda
                add_quad(((x, 0, z), (x, 0, z + max_height), (x, wall_height, z + max_height), (x, wall_height, z)))
                # Derecha
                add_quad(((x + max_width, 0, z), (x + max_width, 0, z + max_height),
                          (x + max_width, wall_height, z + max_height), (x + max_width, wall_height, z)))
                # Arriba
                add_quad(((x, wall_height, z), (x + max_width, wall_height, z),
                          (x + max_width, wall_height, z + max_height), (x, wall_height, z + max_height)))

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
    euclidean_distance = math.sqrt(
        (player_x - enemy_instance.MassCenter[0]) ** 2 + (player_z - abs(enemy_instance.MassCenter[1])) ** 2)
    return euclidean_distance < (playerSize + enemy_instance.size)


def display():
    global edo_game
    if edo_game == 0:
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
            edo_game = 1
        if is_collision_with_coins(player_x, player_z):
            collectedItems -= 1
            if collectedItems == 0:
                edo_game = 2
    elif edo_game == 1:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        show_game_over_message()
    elif edo_game == 2:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
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
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1, 1, 1)  # Color rojo para "Game Over"
    render_text("You win", screen_width // 2 - 100, screen_height // 2, (255, 0, 0))

    glPopMatrix()  # Restaurar la matriz de modelo-vista
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()  # Restaurar la matriz de proyección
    glMatrixMode(GL_MODELVIEW)


def show_game_over_message():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, screen_width, 0, screen_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1.0, 0.0, 0.0)  # Color rojo para "Game Over"
    render_text("Game Over", screen_width // 2 - 100, screen_height // 2, (255, 0, 0))

    glPopMatrix()  # Restaurar la matriz de modelo-vista
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()  # Restaurar la matriz de proyección
    glMatrixMode(GL_MODELVIEW)

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

def render_text(text, x, y, color):
    font = pygame.font.Font(None, 36)  # Cargar una fuente (puedes ajustar el tamaño y el tipo de fuente)
    text_surface = font.render(text, True, color)  # Renderizar el texto en una superficie de Pygame
    text_data = pygame.image.tostring(text_surface, "RGBA", True)  # Convertir la superficie en datos de píxeles

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(),
                 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    glEnable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 1.0)  # Color blanco para el texto
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(x, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + text_surface.get_width(), y)
    glTexCoord2f(1, 0)
    glVertex2f(x + text_surface.get_width(), y + text_surface.get_height())
    glTexCoord2f(0, 0)
    glVertex2f(x, y + text_surface.get_height())
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    
def play_screamer_video():
    # Extrae el audio del video y guárdalo como un archivo temporal
    video = VideoFileClip('BOOGIE.mp4')
    audio_path = 'boogie_audio.mp3'
    video.audio.write_audiofile(audio_path)

    # Inicializa Pygame Mixer para reproducir el audio
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    # Libera la pantalla de Pygame para OpenCV
    pygame.display.quit()

    # Configura la captura de video
    cap = cv2.VideoCapture('BOOGIE.mp4')

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    cv2.namedWindow('Screamer', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Screamer', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Screamer', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Detiene la música
    pygame.mixer.music.stop()

    # Reinitia Pygame display
    pygame.display.init()
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Chase: Take A Chance")
    Init()  # Reinicia el contexto de OpenGL

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
