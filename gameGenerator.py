from random import randint

gameMap = [[None for col in range(6)] for row in range(6)] # empty matrix of size 6x6

class bullet:
    def __init__(self):
        self.startingPointX = randint(0, 6)
        self.startingPointY = randint(0, 6)