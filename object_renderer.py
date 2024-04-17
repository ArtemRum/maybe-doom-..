import pygame as pg
from settings import *
from random import  randrange
import sys 
import time


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.music = game.sound
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        
        self.menu_picture = pg.image.load('resources/img/bg.jpg').convert()   
        
        self.font = pg.font.SysFont('Arial', 36, bold=True)
        self.font_win = pg.font.Font('resources/font/font.ttf', 144)
        
        self.menu_trigger = True
        self.win_trigger = False

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        
    def menu(self):
        pg.mouse.set_visible(True)
        self.music.menu()
        
        x = 0

        button_font = pg.font.Font('resources/font/font.ttf', 72)
        label_font = pg.font.Font('resources/font/font1.otf', 400)
        start = button_font.render('START', 1, pg.Color('lightgray'))
        button_start = pg.Rect(0, 0, 400, 150)
        button_start.center = HALF_WIDTH, HALF_HEIGHT
        exit = button_font.render('EXIT', 1, pg.Color('lightgray'))
        button_exit = pg.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200

        while self.menu_trigger:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.blit(self.menu_picture, (0, 0), (x % WIDTH, HALF_HEIGHT, WIDTH, HEIGHT))
            x += 1

            pg.draw.rect(self.screen, BLACK, button_start, 25)
            self.screen.blit(start, (button_start.centerx - 120, button_start.centery - 45))

            pg.draw.rect(self.screen, BLACK, button_exit, 25)
            self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 45))

            color = randrange(40)
            label = label_font.render('doom', 1, (color, color, color))
            self.screen.blit(label, (15, -30))

            mouse_pos = pg.mouse.get_pos()
            mouse_click = pg.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pg.draw.rect(self.screen, BLACK, button_start, 25)
                self.screen.blit(start, (button_start.centerx - 125, button_start.centery - 50))
                if mouse_click[0]:
                    self.music.theme()
                    pg.mouse.set_visible(False)
                    self.menu_trigger = False

            elif button_exit.collidepoint(mouse_pos):
                pg.draw.rect(self.screen, BLACK, button_exit, 25)
                self.screen.blit(exit, (button_exit.centerx - 80, button_exit.centery - 40))
                if mouse_click[0]:
                    pg.quit()
                    sys.exit()

            pg.display.flip()
            self.clock.tick(20)

    def win(self):
        self.music.win()
        pg.mouse.set_visible(True)
        button_font = pg.font.Font('resources/font/font.ttf', 72)
        rect = pg.Rect(0, 0, 1000, 300)
        rect.center = HALF_WIDTH, HALF_HEIGHT
        restart = button_font.render('RESTART', 1, pg.Color('lightgray'))
        button_restart = pg.Rect(0, 0, 400, 150)
        button_restart.center = HALF_WIDTH, HALF_HEIGHT + 200
        
   
        pg.draw.rect(self.screen, BLACK, rect, 50)

        pg.draw.rect(self.screen, BLACK, button_restart, 25)        
        self.screen.blit(restart, (button_restart.centerx - 185, button_restart.centery - 45))

        while self.win_trigger:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    
            render = self.font_win.render('YOU WIN!!!', 1, (randrange(40, 120), 0, 0))      
            self.screen.blit(render, (rect.centerx - 430, rect.centery - 90))
            
            mouse_pos = pg.mouse.get_pos()
            mouse_click = pg.mouse.get_pressed()
            if button_restart.collidepoint(mouse_pos):
                if mouse_click[0]:
                    self.music.theme()
                    self.win_trigger = False
                    pg.mouse.set_visible(False)
            pg.display.flip()
            self.clock.tick(20)

    def game_over(self):
        pg.mouse.set_visible(True)
        button_font = pg.font.Font('resources/font/font.ttf', 72)
        rect = pg.Rect(0, 0, 1000, 300)
        rect.center = HALF_WIDTH, HALF_HEIGHT
        restart = button_font.render('RESTART', 1, pg.Color('lightgray'))
        button_restart = pg.Rect(0, 0, 400, 150)
        button_restart.center = HALF_WIDTH, HALF_HEIGHT + 200
        
   
        pg.draw.rect(self.screen, BLACK, rect, 50)

        pg.draw.rect(self.screen, BLACK, button_restart, 25)        
        self.screen.blit(restart, (button_restart.centerx - 185, button_restart.centery - 45))

        while self.win_trigger:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    
            render = self.font_win.render('YOU LOSE!!', 1, (randrange(40, 120), 0, 0))      
            self.screen.blit(render, (rect.centerx - 430, rect.centery - 90))
            
            mouse_pos = pg.mouse.get_pos()
            mouse_click = pg.mouse.get_pressed()
            if button_restart.collidepoint(mouse_pos):
                if mouse_click[0]:
                    pg.mixer.music.stop()
                    self.win_trigger = False
                    pg.mouse.set_visible(False)
            pg.display.flip()
            self.clock.tick(20)
            
    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }
