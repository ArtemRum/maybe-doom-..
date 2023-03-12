class Enemy:
    def __init__(self, x, y, fov, view):
        self.x = x
        self.y = y
        self.fov = fov #угол обзора
        self.view = view #угол зрения
        self.movements = {'w': False, 'a':False, 's':False, 'd':False}
        self.distances = []

    def update(self): #движение
        radAngle = math.radians(self.view)
        if self.movements['w'] == True and self.tm[int(self.y+(math.sin(radAngle)*0.05))][int(self.x+(math.cos(radAngle)*0.05))] == 0:
            self.x += math.cos(radAngle)*0.05
            self.y += math.sin(radAngle)*0.05
        if self.movements['a'] == True:
            self.view -= 3
        if self.movements['d'] == True:
            self.view += 3

    