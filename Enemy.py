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
        # Calcula el path usando el algoritmo A*
        self.path = self.calculate_path(matrix, start, end)
        # Inicializa en la primera posición del camino
        self.Position = [self.path[0][0], -self.path[0][1], 0]  # usa valores negativos
        self.path_index = 0
        self.move_count = 0  # Contador de movimientos
        self.vel = vel
        self.collision = False
        self.MassCenter = [self.Position[0], self.Position[1]]
        self.size = 16

    def calculate_path(self, matrix, start, end):
        grid = Grid(matrix=matrix)
        start_node = grid.node(int(start[0]), int(start[1]))
        end_node = grid.node(int(end[0]), int(end[1]))
        finder = AStarFinder()
        path, runs = finder.find_path(start_node, end_node, grid)
        path = [(node.x, node.y) for node in path]
        return path

    def update(self, new_end):
        if self.path_index < len(self.path) - 1:
            # Movimiento hacia la siguiente posición en el camino
            next_pos = self.path[self.path_index + 1]
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
                    self.path_index += 1

            self.move_count += 1

            if self.move_count >= 50:
                print("recalculando path")
                self.path = self.calculate_path(matrix, (self.Position[0], self.Position[1]), new_end)
                self.path_index = 0
                self.move_count = 0
                print(f"Nueva posición de inicio: {self.Position[0]}, {-self.Position[1]}")
                print(f"Nuevo destino: {new_end}")
                print(self.path)
