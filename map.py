import random 
import pygame as pg
from settings import PLAYER_POS
_ = False
map_objects=[2,3,4,5]
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, 1],
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 3, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, 3, 4, _, 4, 3, _, 1],
    [1, _, _, 5, _, _, _, _, _, _, 3, _, 3, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 4, _, _, _, _, _, _, 4, _, _, 4, _, _, _, 1],
    [1, 1, 3, 3, _, _, 3, 3, 1, 3, 3, 1, 3, 1, 1, 1],
    [1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 4, _, _, 4, 3, 3, 3, 3, 3, 3, 3, 3, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 5, _, _, _, 5, _, _, _, 5, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map #self.map_generation()
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]
        
    def generate_maze(self, width, height):
        # Создаем пустую карту
        maze = [[0 for _ in range(width)] for _ in range(height)]
        
        # Устанавливаем внешние стены
        for i in range(width):
            maze[0][i] = 1
            maze[height-1][i] = 1
        for i in range(height):
            maze[i][0] = 1
            maze[i][width-1] = 1
            
        # Генерация лабиринта с использованием алгоритма "Рекурсивное разбиение"
        self.divide(maze, 1, 1, width-2, height-2)
        
        # Установка стартовой и конечной точек
        maze[1][0] = 2
        maze[height-2][width-1] = 3
        
        return maze

    def divide(self, maze, x, y, width, height):
        if width < 3 or height < 3:
            return
        
        if width < height:
            self.split_horizontally(maze, x, y, width, height)
        elif height < width:
            self.split_vertically(maze, x, y, width, height)
        else:
            if random.choice([True, False]):
                self.split_horizontally(maze, x, y, width, height)
            else:
                self.split_vertically(maze, x, y, width, height)

    def split_horizontally(self, maze, x, y, width, height):
        divide_point = random.randint(2, height-2)
        passage = random.randint(x + 1, x + width - 1)
        for i in range(x, x + width + 1):
            maze[y + divide_point][i] = 1
        maze[y + divide_point][passage] = 0  # Соединяем клетки
        self.divide(maze, x, y, width, divide_point - 1)
        self.divide(maze, x, y + divide_point + 1, width, height - divide_point - 1)

    def split_vertically(self, maze, x, y, width, height):
        divide_point = random.randint(2, width-2)
        passage = random.randint(y + 1, y + height - 1)
        for i in range(y, y + height + 1):
            maze[i][x + divide_point] = 1
        maze[passage][x + divide_point] = 0  # Соединяем клетки
        self.divide(maze, x, y, divide_point - 1, height)
        self.divide(maze, x + divide_point + 1, y, width - divide_point - 1, height)