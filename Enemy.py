import os
import math
import numpy as np
import pandas as pd
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_PATH, 'map.csv')

matrix = np.array(pd.io.parsers.read_csv(CSV_FILE, header=None)).astype("int")

class Enemy:
    def __init__(self, vel, Scale, start, end):
        self.scale = Scale
        self.radio = math.sqrt(self.scale * self.scale + self.scale * self.scale)
        self.grid = Grid(matrix=matrix)
        self.path = self.calculate_path(start, end)
        self.Position = [self.path[0][0], -self.path[0][1], 0]  # usa valores negativos
        self.path_index = 0
        self.move_count = 0
        self.vel = vel
        self.collision = False
        self.MassCenter = [self.Position[0], self.Position[1]]
        self.size = 16

    def calculate_path(self, start, end):
        self.grid.cleanup()
        start_node = self.grid.node(int(start[0]), int(start[1]))
        end_node = self.grid.node(int(end[0]), int(end[1]))
        finder = AStarFinder()
        path, runs = finder.find_path(start_node, end_node, self.grid)
        path = [(node.x, node.y) for node in path]
        return path

    def update(self, new_end):
        if self.path_index < len(self.path) - 1:
            if self.path_index + self.vel < len(self.path):
                next_pos = self.path[self.path_index + self.vel]
            else:
                next_pos = self.path[-1]  # Mantener el último punto como el siguiente destino

            dir_x = next_pos[0] - self.Position[0]
            dir_y = next_pos[1] - self.Position[1]

            distance = math.sqrt(dir_x ** 2 + dir_y ** 2)
            if distance != 0:
                dir_x /= distance
                dir_y /= distance

            new_x = self.Position[0] + dir_x * self.vel
            new_z = self.Position[1] + dir_y * self.vel

            self.MassCenter[0] = new_x
            self.MassCenter[1] = new_z

            if not self.collision:
                self.Position[0] = new_x
                self.Position[1] = new_z

                if abs(self.Position[0] - next_pos[0]) < self.vel and abs(self.Position[1] - next_pos[1]) < self.vel:
                    self.path_index += self.vel

            self.move_count += 1

            # Si el enemigo se mueve muy poco durante varios ciclos, recalcular la ruta
            if self.move_count >= 50 or (distance < 0.1 and self.move_count >= 10):
                self.path = self.calculate_path((self.Position[0], self.Position[1]), new_end)
                self.path_index = 0
                self.move_count = 0
        else:
            # Si el enemigo llega al final de la ruta, recalcular la ruta
            self.path = self.calculate_path((self.Position[0], self.Position[1]), new_end)
            self.path_index = 0
