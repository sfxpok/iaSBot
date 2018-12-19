
###
# Criação e geração de entidades que fazem parte do jogo
###

#from random import randint
from enum import Enum

gameMap = [[None for col in range(6)] for row in range(6)] # empty matrix of size 6x6

class Entity: # base class for inheritance
    def __init__(self, x, y):
        self.coordX = x
        self.coordY = y

class Object(Entity): # base class for inheritance
    def __init__(self, name, x, y):
        Entity.__init__(self, x, y)
        self.name = name

class Orientation(Enum):
    north = 1
    west = 2
    east = 3
    south = 4

class Robot(Entity):
    def __init__(self):
        Entity.__init__(self, 0, 5)
        self.hasBullet = False
        self.turnToPlay = True # This shoud be false
        self.piecesCarry = 0
        self.canMove = True
        self.canAttack = True
        self.canScout = True
        self.orientation = None
        self.alarm = False

#--------------Section to delete-------

class Zombie(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.isStunned = False
        self.turnsUnableToPlay = 0
        self.hasPiece = False

class Bike(Entity):
    def __init__(self):
        Entity.__init__(self, 5, 0)
        self.mountedPieces = 0

def spawnZombies():
    zb1 = Zombie(0,0)
    zb2 = Zombie(5,5)

#---------End of section--------