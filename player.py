import csv

class Player:
    def __init__(self, map_file):
        self.map = self.load_map(map_file)
        self.x = 0
        self.z = 0

    def load_map(self, map_file):
        with open(map_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            return [[int(cell) for cell in row] for row in reader]

    def can_move_to(self, x, z):
        if 0 <= x < len(self.map) and 0 <= z < len(self.map[0]):
            return self.map[x][z] == 1
        return False

    def move(self, direction):
        new_x, new_z = self.x, self.z
        if direction == 'up':
            new_x += 1
        elif direction == 'down':
            new_x -= 1
        elif direction == 'left':
            new_z -= 1
        elif direction == 'right':
            new_z += 1

        if self.can_move_to(new_x, new_z):
            self.x, self.z = new_x, new_z
            return True
        return False
