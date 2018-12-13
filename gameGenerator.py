###
# Criação e geração de entidades que fazem parte do jogo
###

from random import randint

gameMap = [[None for col in range(6)] for row in range(6)] # empty matrix of size 6x6

#class Bullet:
#    def __init__(self):
#        self.startingPointX = randint(0, 6)
#        self.startingPointY = randint(0, 6)

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
    def __init__(self, x, y):
        #self.turnToPlay = False
        #self.isDead = False
        #self.isAlert = False
        self.isStunned = False
        self.turnsUnableToPlay = 0
        self.coordX = x
        self.coordY = y

class Bike(Entity):
    def __init__(self):
        Entity.__init__(self, 6, 6)
        self.mountedPieces = 0

class mapBehaviour():
    def __init__(self):
        self.alarm = False

def spawnZombies():
    zb1 = Zombie(1,6)
    zb2 = Zombie(6,1)

    # zb1.coordX = 1
    # zb1.coordY = 6

    # zb2.coordX = 6
    # zb2.coordY = 1