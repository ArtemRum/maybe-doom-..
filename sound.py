import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.npc_shot.set_volume(0.2)
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        
        pg.mixer.music.set_volume(0.3)
        
    def menu(self):
        pg.mixer.music.stop()
        pg.mixer.music.load(self.path + 'music/menu.mp3')
        pg.mixer.music.play(-1)
        
    def theme(self):
        pg.mixer.music.stop()
        pg.mixer.music.load(self.path + 'music/theme.mp3')
        pg.mixer.music.play(-1)
        
    def win(self):
        pg.mixer.music.stop()
        pg.mixer.music.load(self.path + 'music/win.mp3')
        pg.mixer.music.play(-1)