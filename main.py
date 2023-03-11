#Import modules
import pygame
import math

import enemy

#Set up window
pygame.init()

winWidth, winHeight = (1024, 512)
window = pygame.display.set_mode((winWidth, winHeight))

#Make player object
class Player:
    def __init__(self, x, y, tm, fov, view):
        self.x = x
        self.y = y
        self.tm = tm #tilemap
        self.fov = fov #field of view
        self.view = view #players angle
        self.movements = {'w': False, 'a':False, 's':False, 'd':False}
        self.distances = []
        self.img = pygame.image.load("texture.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (64, 64))
    
    def update(self): #Player movements
        radAngle = math.radians(self.view)
        if self.movements['w'] == True and self.tm[int(self.y+(math.sin(radAngle)*0.05))][int(self.x+(math.cos(radAngle)*0.05))] == 0:
            self.x += math.cos(radAngle)*0.05
            self.y += math.sin(radAngle)*0.05
        if self.movements['a'] == True:
            self.view -= 3
        if self.movements['d'] == True:
            self.view += 3
            
    def draw(self, window):
        #---TopDown View---
        #Map
        for y, row in enumerate(self.tm):
            for x, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(window, (255,255,255), (x*64, y*64, 64, 64))
                    pygame.draw.rect(window, (0,0,0), (x*64, y*64, 64, 64), 1)
                else:
                    pygame.draw.rect(window, (0,0,0), (x*64, y*64, 64, 64))
                    pygame.draw.rect(window, (255,255,255), (x*64, y*64, 64, 64), 1)
        #player
        pygame.draw.circle(window, (255,255,0), (int(self.x*64), int(self.y*64)), 8)
        #Rays :D
        self.distances = []
        for degree in range(int(self.view-(self.fov/2)), int(self.view+(self.fov/2))):
            radAngle = math.radians(degree)
            rayx = self.x
            rayy = self.y
            
            stop = False
            while self.tm[int(rayy)][int(rayx)] == 0 and stop == False:
                rayx += math.cos(radAngle)*0.01
                rayy += math.sin(radAngle)*0.01

            #Calculate ray distance
            dist = math.sqrt(((rayx-self.x)*(rayx-self.x)+(rayy-self.y)*(rayy-self.y)))
            #Draw the ray
            pygame.draw.line(window, (0,255,0), (self.x*64, self.y*64), (rayx*64, rayy*64))
            

            #Decide if colides horizontally or vertically (To help with drawing tiles)
            rx = round(rayx - int(rayx), 5)
            ry = round(rayy - int(rayy), 5)
            h_col = False
            if rx > .5:
                if ry > .5 - (rx - .5) and ry < .5 + (rx - .5):
                    h_col = True
                else:
                    h_col = False
            elif rx <= .5:
                if ry > .5 - (.5 - rx) and ry < .5 + (.5 - rx):
                    h_col = True
                else:
                    h_col = False
            
            if h_col == True:
                num = ry
            else:
                num = rx

            #Attempt at fixing curved walls. Works somewhat but not really
            angle = math.radians(self.view - degree)
            dist *= math.cos(angle)
            
            self.distances.append((dist, num))
        #draw player view ray
        pygame.draw.line(window, (255,0,0), (self.x*64, self.y*64), ((self.x+math.cos(math.radians(self.view)))*64, (self.y+math.sin(math.radians(self.view)))*64))
        #---3D View---
        for x, line in enumerate(self.distances):
            height = 256 - round(line[0], 1)*42
            if height <= .5:
                height = .5
            w, h = self.img.get_width(), self.img.get_height()

            img_x = int(line[1]*w)
            if img_x > 63:
                img_x = 63
            elif img_x < 0:
                img_x = 0
            img = self.img.subsurface(img_x, 0, 1, h)
            img = pygame.transform.scale(img, (8, int(height*2)))

            window.blit(img, (512+(x*8), 256-height))

        
class Control:
    def __init__(self):
        self.run = True
        self.clock = pygame.time.Clock()
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.movements["w"] = True
                if event.key == pygame.K_a:
                    player.movements["a"] = True
                if event.key == pygame.K_s:
                    player.movements["s"] = True
                if event.key == pygame.K_d:
                    player.movements["d"] = True
                if event.key == pygame.K_ESCAPE:
                    self.run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.movements["w"] = False
                if event.key == pygame.K_a:
                    player.movements["a"] = False
                if event.key == pygame.K_s:
                    player.movements["s"] = False
                if event.key == pygame.K_d:
                    player.movements["d"] = False

game = Control()
tm = [
    [1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,1],
    [1,1,1,1,0,1,0,1],
    [1,0,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1]
]

player = Player(3.5, 3.5, tm, 64, 0)

while game.run:
    window.fill((50,50,50))
    player.draw(window)

    pygame.display.update()
    game.update()
    player.update()

    game.clock.tick(30)

pygame.quit()