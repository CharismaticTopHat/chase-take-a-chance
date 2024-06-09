import pygame

from OpenGL.GL import *
from OpenGL.GLUT import *

import random
import math

class Coin:
    
    def __init__(self, Scale, locations):
        self.locations = locations
        self.scale = Scale
        self.radio = math.sqrt(self.scale*self.scale + self.scale*self.scale)
        self.available_locations = locations[:]
        self.generate_new_coordinates()
    
    def generate_new_coordinates(self):
        if self.available_locations:
            self.Coordinates = random.choice(self.available_locations)
            self.available_locations.remove(self.Coordinates)  # Remove the chosen coordinates
            self.Position = [self.Coordinates[0], self.Coordinates[1], 5]
            self.MassCenter = [self.Position[0], self.Position[1]]
            self.size = 6
        else:
            print("No available locations for coins!")