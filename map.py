from settings import *
import pygame

from numba.core import types
from numba.typed import Dict
from numba import int32

_ = False
matrix_map = [
[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, 4, _, _, _, _, _, 1],
    [1, _, 2, 2, _, _, _, _, _, 2, 2, 2, _, _, _, 3, _, _, _, _, 4, _, _, 1],
    [1, 0, _, _, _, _, _, _, _, _, _, 2, 2, _, _, _, 3, _, _, _, _, _, _, 1],
    [1, _, 2, 2, _, _, _, _, _, _, _, _, 2, _, 4, _, _, 3, _, _, _, 4, _, 1],
    [1, _, _, _, _, _, 4, _, _, 2, 2, _, 2, _, _, _, _, _, _, 4, _, _, _, 1],
    [1, _, 3, _, _, _, 2, _, _, 2, _, _, 2, _, _, _, 4, _, _, _, _, 4, _, 1],
    [1, _, _, 3, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 3, _, _, _, _, _, _, _, 3, _, _, 3, 3, _, _, _, _, 3, 3, _, _, 1],
    [1, _, 3, _, _, _, 3, 3, _, 3, _, _, _, 3, 3, _, _, _, _, 2, 3, _, _, 1],
    [1, _, _, _, _, 3, _, 3, _, _, 3, _, _, _, _, _, 2, 1, _, _, _, _, _, 1],
    [1, _, 4, _, 3, _, _, _, _, 3, _, _, 2, _, _, _, _, _, _, _, _, 2, _, 1],
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, 2, _, _, _, _, _, _, 2, 2, _, 1],
    [1, _, _, 4, _, _, _, _, 4, _, _, _, _, 2, 2, 2, 2, 2, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 4, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
],
[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, _, _, _, 2, _, 3, 1],
    [1, _, 2, 3, 2, 2, _, 2, 2, 2, 2, 2, 2, _, 2, _, _, _, 2, _, _, _, _, 1],
    [1, 0, 2, _, 2, 2, _, 2, _, _, _, _, _, _, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 3, 2, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, 2, 2, 2, 2, 2, _, 2, 2, 2, 2, _, 2, 2, 2, 2, _, 2, 2, 2, _, 1],
    [1, _, _, _, _, _, _, _, _, 2, 3, _, 2, 3, 2, 2, 2, 3, _, _, _, 2, _, 1],
    [1, _, 2, 2, 2, 2, 2, 2, 2, 2, 2, _, 2, _, 2, 2, 2, _, 2, 2, _, 2, _, 1],
    [1, _, _, 3, _, _, 2, 2, 2, _, _, _, 2, _, _, _, _, _, 2, 2, _, 2, _, 1],
    [1, 2, 2, 2, 2, _, 2, 2, _, _, 2, _, 2, 2, 2, 2, 2, _, _, _, _, 2, _, 1],
    [1, _, _, _, _, _, 2, 2, 2, _, 2, _, 2, _, _, _, _, 2, 2, 2, _, 2, _, 1],
    [1, _, 2, 2, _, _, _, 3, _, _, 2, _, _, _, 3, 2, _, _, _, 2, _, 2, _, 1],
    [1, 3, 2, 2, 2, 2, _, _, 2, 2, 3, _, 2, 2, _, 2, _, 2, _, _, 3, 2, _, 1],
    [1, 0, _, 2, _, 2, 2, _, 2, _, _, _, 2, _, _, _, _, _, 2, _, _, _, _, 1],
    [1, 2, _, _, _, _, _, _, _, _, 2, _, _, _, 3, 2, 2, 2, 2, 2, 2, 2, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
],
[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 0, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]]


objects = [
           [['sprite_barrel', (7.1, 2.1)],
            ['sprite_barrel', (5.9, 2.1)],
            ['sprite_pin', (8.7, 2.5)],
            ['npc_devil', (7, 4)],
            ['sprite_flame', (8.6, 5.6)],
            ['sprite_door_v', (3.5, 3.5)],
            ['sprite_door_h', (1.5, 4.5)],
            ['npc_soldier0', (2.5, 1.5)],
            ['npc_soldier0', (5.51, 1.5)],
            ['npc_soldier0', (6.61, 2.92)],
            ['npc_soldier0', (7.68, 1.47)],
            ['npc_soldier0', (8.75, 3.65)],
            ['npc_soldier0', (1.27, 11.5)],
            ['npc_soldier0', (1.26, 8.29)]],
           [['sprite_barrel', (7.1, 2.1)],
            ['sprite_barrel', (5.9, 2.1)],
            ['sprite_door_v', (2, 14)],
            ['sprite_pin', (8.7, 2.5)],
            ['npc_devil', (7, 4)],
            ['sprite_flame', (8.6, 5.6)],
            ['npc_soldier0', (2.5, 1.5)],
            ['npc_soldier0', (5.51, 1.5)],
            ['npc_soldier0', (6.61, 2.92)],
            ['npc_soldier0', (7.68, 1.47)],
            ['npc_soldier0', (8.75, 3.65)],
            ['npc_soldier0', (1.27, 11.5)],
            ['npc_soldier0', (1.26, 8.29)]],
           [['sprite_barrel', (7.1, 2.1)],
            ['sprite_barrel', (5.9, 2.1)],
            ['sprite_pin', (8.7, 2.5)],
            ['npc_devil', (7, 4)],
            ['sprite_flame', (8.6, 5.6)],
            ['sprite_door_v', (3.5, 3.5)],
            ['sprite_door_h', (1.5, 4.5)],
            ['npc_soldier0', (2.5, 1.5)],
            ['npc_soldier0', (5.51, 1.5)],
            ['npc_soldier0', (6.61, 2.92)],
            ['npc_soldier0', (7.68, 1.47)],
            ['npc_soldier0', (8.75, 3.65)],
            ['npc_soldier0', (1.27, 11.5)],
            ['npc_soldier0', (1.26, 8.29)]]
]

class Map:
    def __init__(self, matrix_map):
        self.WORLD_WIDTH = len(matrix_map[0]) * TILE
        self.WORLD_HEIGHT = len(matrix_map) * TILE
        self.world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        self.mini_map = set()
        self.collision_walls = []

        for j, row in enumerate(matrix_map):
            for i, char in enumerate(row):
                if char:
                    self.mini_map.add((i * MAP_TILE, j * MAP_TILE))
                    self.collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
                    if char == 1:
                        self.world_map[(i * TILE, j * TILE)] = 1
                    elif char == 2:
                        self.world_map[(i * TILE, j * TILE)] = 2
                    elif char == 3:
                        self.world_map[(i * TILE, j * TILE)] = 3
                    elif char == 4:
                        self.world_map[(i * TILE, j * TILE)] = 4
