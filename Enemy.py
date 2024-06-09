import pygame

from OpenGL.GL import *
from OpenGL.GLUT import *

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import os
import numpy as np
import pandas as pd
import random
import math

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_PATH, 'map.csv')

matrix = np.array(pd.io.parsers.read_csv(CSV_FILE, header=None)).astype("int")
class Enemy:

    def __init__(self, vel, Scale):
        self.scale = Scale
        self.radio = math.sqrt(self.scale*self.scale + self.scale*self.scale)
        #Se inicializa una posicion establecido
        self.Position = [225, -500, 0]
        #Se inicializa un vector de direccion aleatorio
        self.Direction = [0, 1, 0]
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[1]*self.Direction[1])
        self.Direction[0] /= m
        self.Direction[1] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[1] *= vel
        #deteccion de colision
        self.collision = False
        #Centro de masa
        self.MassCenter = []
        self.MassCenter.append(self.Position[0])
        self.MassCenter.append(self.Position[1])
        #Radio de colisión
        self.size = 16

    def update(self):
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[1] + self.Direction[1]
        self.MassCenter[0] = new_x
        self.MassCenter[1] = new_z

        if(self.collision == False):
            self.Position[0] = new_x
        else:
            self.Direction[0] *= -1.0
            self.Position[0] += self.Direction[0]

        if(self.collision == False):
            self.Position[1] = new_z
        else:
            self.Direction[1] *= -1.0
            self.Position[1] += self.Direction[1]