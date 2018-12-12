from random import randint

gameMap = [[None for col in range(6)] for row in range(6)] # empty matrix of size 6x6

class Bullet:
    def __init__(self):
        self.startingPointX = randint(0, 6)
        self.startingPointY = randint(0, 6)

class Entity: # base class for inheritance
    def __init__(self, x, y):
        self.turnToPlay = False
        self.isDead = False
        self.bikePieces = 0
        self.coordX = x
        self.coordY = y

class Robot(Entity):
    def __init__(self):
        self.hasBullet = False
        Entity.__init__(self, 1, 1)
        #self.turnToPlay = True
        #self.bikePieces = 0

class Zombie(Entity):
    def __init__(self):
        #self.turnToPlay = False
        #self.isDead = False
        #self.isAlert = False
        self.isStunned = False

class Bike(Entity):
    def __init__(self):
        Entity.__init__(self, 6, 6)

class mapBehaviour():
    def __init__(self):
        self.alarm = False

def spawnZombies():
    zb1 = Zombie()
    zb2 = Zombie()

    zb1.coordX = 1
    zb1.coordY = 6

    zb2.coordX = 6
    zb2.coordY = 1