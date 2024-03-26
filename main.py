from player import Player
from sprite_objects import *
from ray_casting import ray_casting_walls
from draw import Drawing
from interaction import Interaction
from map import Map, objects, matrix_map

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
sc_map = pygame.Surface(MINIMAP_RES)

lvl = 0
max_lvl = len(matrix_map)

map = Map(matrix_map[lvl])
sprites = Sprites()

[sprites.add_objects(o[0], o[1]) for o in objects[lvl]]

clock = pygame.time.Clock()
player = Player(sprites, map.collision_walls)
drawing = Drawing(sc, sc_map, player, clock)
interaction = Interaction(player, sprites, drawing)

drawing.head()
drawing.menu()
pygame.mouse.set_visible(False)
interaction.play_music()



while True:
    
    if interaction.check_win():
        lvl += 1
        if lvl >= max_lvl:
            drawing.win_trigger = True
            drawing.win()
            lvl = 0
        
        map = Map(matrix_map[lvl])
        sprites = Sprites()
        [sprites.add_objects(o[0], o[1]) for o in objects[lvl]]
        clock = pygame.time.Clock()
        player = Player(sprites, map.collision_walls)
        drawing = Drawing(sc, sc_map, player, clock)
        interaction = Interaction(player, sprites, drawing)
        
    player.movement(drawing)
    drawing.background(player.angle)
    walls, wall_shot = ray_casting_walls(player, drawing.textures, map)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.fps(clock)
    drawing.mini_map(player, map.mini_map)
    drawing.player_weapon([wall_shot, sprites.sprite_shot])

    interaction.interaction_objects(map.world_map)
    interaction.npc_action(player, map.world_map)
    interaction.clear_world()
    

    pygame.display.flip()
    clock.tick()