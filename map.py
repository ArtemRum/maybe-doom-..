import random 
import pygame as pg
from settings import *


class Map:
    def __init__(self, game, map_size):
        self.game = game
        self.sc_map = game.sc_map
        self.mini_map = self.generate_maze(random.randint(map_size[0],map_size[1]),random.randint(map_size[0],map_size[1]))
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

    def m_map(self):
        self.sc_map.fill(BLACK)
        map_x, map_y = self.game.player.x*10, self.game.player.y*10
        pg.draw.circle(self.sc_map, RED, (HALF_WIDTH//5, HALF_HEIGHT//5), 5)
        pg.draw.line(self.sc_map, RED, (HALF_WIDTH//5, HALF_HEIGHT//5), (HALF_WIDTH//5+10*math.cos(self.game.player.angle), HALF_HEIGHT//5+10*math.sin(self.game.player.angle)))
        for x, y in self.world_map:
            pg.draw.rect(self.sc_map, DARKBROWN, (HALF_WIDTH//5-map_x+x*10, HALF_HEIGHT//5-map_y+y*10, MAP_TILE, MAP_TILE))
        self.game.screen.blit(self.sc_map, MAP_POS)
        
    def generate_maze(self, width, height):
        # Создаем пустую карту
        maze = [[0 for _ in range(width)] for _ in range(height)]
        
        
        # Генерируем полностью связанный граф клеток
        self.divide(maze, 1, 1, width-2, height-2)
        
        # Удаляем лишние стены, чтобы соответствовать условию не более двух единиц вокруг нуля
        for i in range(height-1):
            for j in range(width-1):
                if maze[i][j] == 0:
                    if self.count_surrounding_walls(maze, i, j) > 2:
                        self.remove_excess_walls(maze, i, j)
        
        for i in range(width):
            maze[0][i] = 1
            maze[height-1][i] = 1
        for i in range(height):
            maze[i][0] = 1
            maze[i][width-1] = 1
        # Установка стартовой и конечной точек
        maze[1][0] = 2
        maze[height-2][width-1] = 6
        maze[height-2][width-2] = 0

        for i in maze:
            for j in i:
                if j == 0:
                    j = '_'
                print(j, end=' ')
            print()
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
        try:
            divide_point = random.randint(2, height-2)
        except ValueError:
            divide_point = 2
        passage = random.randint(x + 1, x + width - 1)
        for i in range(x, x + width + 1):
            maze[y + divide_point][i] = random.randint(1,5)
        maze[y + divide_point][passage] = 0  # Соединяем клетки
        # Гарантируем связность
        adjacent_passage = random.randint(y, y + divide_point - 1)
        maze[adjacent_passage][passage] = 0
        adjacent_passage = random.randint(y + divide_point + 1, y + height)
        maze[adjacent_passage][passage] = 0
        self.divide(maze, x, y, width, divide_point - 1)
        self.divide(maze, x, y + divide_point + 1, width, height - divide_point - 1)

    def split_vertically(self, maze, x, y, width, height):
        try:
            divide_point = random.randint(2, width-2)
        except ValueError:
            divide_point = 2
        passage = random.randint(y + 1, y + height - 1)
        for i in range(y, y + height + 1):
            maze[i][x + divide_point] = random.randint(1,5)
        maze[passage][x + divide_point] = 0  # Соединяем клетки
        # Гарантируем связность
        adjacent_passage = random.randint(x, x + divide_point - 1)
        maze[passage][adjacent_passage] = 0
        adjacent_passage = random.randint(x + divide_point + 1, x + width)
        maze[passage][adjacent_passage] = 0
        self.divide(maze, x, y, divide_point - 1, height)
        self.divide(maze, x + divide_point + 1, y, width - divide_point - 1, height)

    def count_surrounding_walls(self, maze, x, y):
        count = 0
        if maze[x+1][y] in [1, 2, 3, 4, 5]:
            count += 1
        if maze[x-1][y] in [1, 2, 3, 4, 5]:
            count += 1
        if maze[x][y+1] in [1, 2, 3, 4, 5]:
            count += 1
        if maze[x][y-1] in [1, 2, 3, 4, 5]:
            count += 1
        return count

    def remove_excess_walls(self, maze, x, y):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= len(maze) and 0 <= ny <= len(maze[0]):
                maze[nx][ny] = 0