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
    
    def __init__(self, dim, vel, Scale):
        self.scale = Scale
        self.radio = math.sqrt(self.scale*self.scale + self.scale*self.scale)
        self.DimBoard = dim
        #Se inicializa una posicion establecido
        self.Position = []
        self.Position.append(225)
        self.Position.append(-100)
        self.Position.append(0)
        #Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(-1)
        self.Direction.append(0)
        self.Direction.append(0)
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        #Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel
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
        new_z = self.Position[2] + self.Direction[2]
        self.MassCenter[0] = new_x
        self.MassCenter[1] = new_z
        
        if(abs(new_x) <= self.DimBoard and self.collision == False):
            self.Position[0] = new_x
        else:
            self.Direction[0] *= -1.0
            self.Position[0] += self.Direction[0]
        
        if(abs(new_z) <= self.DimBoard and self.collision == False):
            self.Position[2] = new_z
        else:
            self.Direction[2] *= -1.0
            self.Position[2] += self.Direction[2]