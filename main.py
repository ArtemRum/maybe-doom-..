import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    def __init__(self):
        self.lvl = 1
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.sc_map = pg.Surface(MINIMAP_RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        map_size_lst=[10+5*(self.lvl-1),20+5*(self.lvl-1)]
        self.sound = Sound(self)
        self.map = Map(self, map_size_lst)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()
        self.map.m_map()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.object_renderer.menu_trigger = True
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)
            if self.player.shot and self.object_handler.check_win():
                self.object_renderer.win_trigger = True 

    def run(self):
        while game:
            self.check_events()
            if self.object_renderer.menu_trigger:
                self.object_renderer.menu()
            self.update()
            if self.object_handler.check_win() and self.object_renderer.win_trigger:
                self.lvl += 1
                self.new_game()
                self.object_renderer.menu_trigger = False
                self.object_renderer.win_trigger = True
                self.object_renderer.win()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()