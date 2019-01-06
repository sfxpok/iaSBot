#!/usr/bin/env python3
from threading import Thread
from Motor import MoveTank
from ev3dev2.sound import Sound
from ev3dev2.display import Display
import ev3dev2.fonts as fonts
from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, LargeMotor
from ev3dev2.sound import Sound
from ColorDetector import ColorDetector
from Attack import punch, shoot
from Forklift import Fork


def checkColor():
    return ColorDetector().getColor()

class GameMap:
    def __init__(self):
        self.engine = MoveTank()
        self.forkL = Fork()
        self.housesChecked = [(1,1)]
        self.posX = 1
        self.posY = 1
        self.haveAmmo = False
        self.currentPieces = 0
        self.deliveredPieces = 0
        self.levelOneSmell = False
        self.levelTwoSmell = False
        self.direction = self.dirCalibration()
        print(self.direction)
        Sound().speak('Direction ' + self.direction)

        self.realValuesMap = [
                [10,9,8,7,6,5],
                [9,8,7,6,5,4],
                [8,7,6,5,4,3],
                [7,6,5,4,3,2],
                [6,5,4,3,2,1],
                [5,4,3,2,1,0]]
              
        self.heurValueMap = [
                [25,3,6,6,6,30],
                [4,2,2,2,2,4],
                [4,2,3,3,2,4],
                [4,2,3,3,2,4],
                [4,2,2,2,2,4],
                [30,6,6,6,5,30]] 

        self.bulletValue = -10
        self.pieceValue = -15
        self.checkedHouseValue = 1
        self.ZombieValue = 40
        self.danger1Value = 1
        self.danger2Value = 2
        self.danger3Value = 3
        self.danger4Value = 4

        self.smellValues = {
            'Green': 0, # there is no danger
            'Yellow': self.danger1Value,
            'Red': self.danger2Value,
            'Blue': self.danger3Value,
            'Brown': self.danger4Value
        }

        self.zombieValues = {
            'Green': 0, # there is no zombie
            'Yellow': self.ZombieValue, # 2 squares of distance
            'Red': self.ZombieValue, # 1 square of distance
        }

        self.pieceValues = {
            'Green': 0, # there are no pieces
            'Yellow': self.pieceValue,
            'Red': self.bulletValue
        }

        self.lastTurnSmell = 0
        self.foundZombie = False
        self.pickObject = False

    def updateScreen(self):

        # info no ecrã: coords do chappie; se tem bala ou não; se existe cheiro à volta do chappie; quantas peças já devolveu
        lcd = Display()
        updateWarning = Sound()
        lcd.draw.text((10, 10), "Chappie: (" + str(self.posX) + "," + str(self.posY) + ")", font=fonts.load('luBS14'))
        lcd.draw.text((10, 20), "O Chappie tem a bala?: " + str(self.haveAmmo), font=fonts.load('luBS14'))
        lcd.draw.text((10, 30), "Peças na mota: " + str(self.deliveredPieces), font=fonts.load('luBS14'))
        lcd.draw.text((10, 40), "Cheiro nível 1?: " + str(self.levelOneSmell), font=fonts.load('luBS14'))
        lcd.draw.text((10, 50), "Cheiro nível 2?: " + str(self.levelTwoSmell), font=fonts.load('luBS14'))
        lcd.update()
        updateWarning.beep()
        sleep(2)
        # lcd.clear()

    def dirCalibration(self):
        self.engine.engine.on(20,20)
        firstColor = self.waitforColor()
        self.engine.engine.off()

        self.engine.movementDeg(-272)

        self.engine.turnRight()

        self.engine.engine.on(20,20)
        secondColor = self.waitforColor()
        self.engine.engine.off()

        self.engine.movementDeg(-272)

        self.engine.turnLeft()

        if firstColor == 'Red' and secondColor == 'Red':
            return('West')
        elif firstColor == 'Red' and secondColor == 'Black':
            return('North')
        elif firstColor == 'Black' and secondColor == 'Black':
            return('East')
        elif firstColor == 'Black' and secondColor == 'Red':
            return('South') 


    def waitforColor(self):
        while checkColor() == 'White':
            pass
        return checkColor()

    def checkInvalidPositions(self, direction):
        if self.posX == 1 and direction == 'West':
            print('wrong position')
            return False

        if self.posX == 6 and direction == 'East':
            print('wrong position')            
            return False

        if self.posY == 1 and direction == 'North':
            print('wrong position')            
            return False

        if self.posY == 6 and direction == 'South':
            print('wrong position')            
            return False
        return True

    def goDirection(self, direction):
        if self.checkInvalidPositions(direction):
            print('Going to ', direction, ' from X=', self.posX, 'and Y=', self.posY)
            self.setDirection(direction)
            distToMoveOneSquareMotorA = 1139
            distToMoveOneSquareMotorB = 1128
            distToMoveOneSquare = (distToMoveOneSquareMotorA + distToMoveOneSquareMotorB)/2
            self.engine.movementDeg(distToMoveOneSquare)
            if direction == 'North':
                self.posY -= 1
            elif direction == 'South':
                self.posY += 1
            elif direction == 'East':
                self.posX += 1
            elif direction == 'West':
                self.posX -= 1
            self.updateScreen()

    def recognize(self, direction):
        ###
        # Distance between squares:
        #Motor A = 1139
        #Motor B = 1128
        #to implement 31cm = 1134
        # 15.5 = 567
        # 16 = 585
        # 17 = 621
        # 18 = 658 
        ###
        
        if self.checkInvalidPositions(direction):
            self.addHeurAfterRecog(direction)
            self.setDirection(direction)
            self.engine.engine.on(20,20)
            while checkColor() != 'Black':
                pass
            self.engine.engine.off()
            color = [None] * 3
            self.engine.movementDeg(91)
            color[0] = checkColor()
            self.engine.movementDeg(182)
            color[1] = checkColor()
            self.engine.movementDeg(182)
            color[2] = checkColor()
            self.engine.movementDeg(-727)
            return color 
        return 'Invalid'



    def addHeurAfterRecog(self,direction):

        if direction == 'North':
            if ((self.posX),(self.posY-1)) not in self.housesChecked:
                self.housesChecked.append(((self.posX),(self.posY-1)))
                self.heurValueMap[self.posX-1][self.posY-2]+=1
        elif direction == 'East':
            if ((self.posX+1),(self.posY)) not in self.housesChecked:
                self.housesChecked.append(((self.posX+1),(self.posY)))
                self.heurValueMap[self.posX][self.posY-1]+=1
        elif direction == 'South':
            if ((self.posX),(self.posY+1)) not in self.housesChecked:
                self.housesChecked.append(((self.posX),(self.posY+1)))
                self.heurValueMap[self.posX-1][self.posY]+=1
        elif direction == 'West':
            if ((self.posX-1),(self.posY)) not in self.housesChecked:
                self.housesChecked.append(((self.posX-1),(self.posY)))
                self.heurValueMap[self.posX-2][self.posY-1]+=1




        

           

    def fullRecognition(self):
        ### Object color: ###
        # Motorbike part: blue
        # Ammo: Green
        # Zombie distance: level 1 red, level 2 yellow
        # Zombie with motorbike part: Brown

        ### Positions from the array: ###
        # Position 0: Object is North
        # Position 1: Object is East 
        # Position 2: Object is South
        # Position 3: Object is Weast
        # Orientation is clockwise direction

        self.itemsAround = []
        self.itemsAround.append(self.recognize('North'))
        self.itemsAround.append(self.recognize('East'))
        self.itemsAround.append(self.recognize('South'))
        self.itemsAround.append(self.recognize('West'))
        print('Colors: ',str(self.itemsAround))
        for i in range(4):
            if self.itemsAround[i] == 'Invalid':
                self.itemsAround[i] = ['White','White','White']
            for j in range(3):
                if self.itemsAround[i][j] == 'Black':
                    self.itemsAround[i][j] = 'White'
        print('Colors: ',str(self.itemsAround))

        smellsValues = []
        if self.itemsAround[0][0] != 'White':
            smellsValues.append(self.smellValues[self.itemsAround[0][0]])
        else:
            smellsValues.append(0)
        if self.itemsAround[1][0] != 'White':
            smellsValues.append(self.smellValues[self.itemsAround[1][0]])
        else:
            smellsValues.append(0)
        if self.itemsAround[2][0] != 'White':
            smellsValues.append(self.smellValues[self.itemsAround[2][0]])
        else:
            smellsValues.append(0)
        if self.itemsAround[3][0] != 'White':
            smellsValues.append(self.smellValues[self.itemsAround[3][0]])
        else:
            smellsValues.append(0)
        self.lastTurnSmell = self.saveSmell(smellsValues)

        self.heurValueMap[self.posX-1][self.posY-1]+=1

        print('Heuristic Map: ',str(self.heurValueMap[5]))
        print('               ',str(self.heurValueMap[4]))
        print('               ',str(self.heurValueMap[3]))
        print('               ',str(self.heurValueMap[2]))
        print('               ',str(self.heurValueMap[1]))
        print('               ',str(self.heurValueMap[0]))
        
        return self.itemsAround

    def setDirection(self, direction):
        if self.direction != direction:
            if direction == 'North':
                if self.direction == 'South':
                    self.engine.turnRight()
                    self.engine.turnRight()

                if self.direction == 'West':
                    self.engine.turnRight()

                if self.direction == 'East':
                    self.engine.turnLeft()

            if direction == 'South':
                if self.direction == 'North':
                    self.engine.turnRight()
                    self.engine.turnRight() 

                if self.direction == 'East':
                    self.engine.turnRight()

                if self.direction == 'West':
                    self.engine.turnLeft()

            if direction == 'East':
                if self.direction == 'West':
                    self.engine.turnRight()
                    self.engine.turnRight() 

                if self.direction == 'North':
                    self.engine.turnRight()

                if self.direction == 'South':
                    self.engine.turnLeft()
            
            if direction == 'West':
                if self.direction == 'East':
                    self.engine.turnRight()
                    self.engine.turnRight() 

                if self.direction == 'North':
                    self.engine.turnLeft()

                if self.direction == 'South':
                    self.engine.turnRight()

        if direction == 'West' or direction == 'East' or direction == 'North' or direction == 'South':
            self.direction = direction





    #Lista da accoes que o robo deve fazer por turno dependendo do cheiro na sua casa no ultimo turno
    def listActions(self):
        if self.currentPieces == 2:
            if self.posX == 6 and self.posY == 6:
                    self.forkL.dropObject()
                    self.deliveredPieces+=2
                    self.currentPieces-=2
                    print('Victory!')
                    return True
        if self.lastTurnSmell == 0:
            self.search()
            colorArray = self.fullRecognition()
            zombiesDirections = self.whereZombie(colorArray)
            if zombiesDirections[0] != [] or zombiesDirections[1] != []: # are there zombies nearby?
                self.attack(zombiesDirections)
            return False
        else:
            colorArray = self.fullRecognition()
            zombiesDirections = self.whereZombie(colorArray)
            if zombiesDirections[0] != [] or zombiesDirections[1] != []: # are there zombies nearby?
                self.attack(zombiesDirections)
            self.search(colorArray)
            return False

    #Attaque do robo. Se ele tiver a bala ele dispara, senao ele da o ataque de machete
    def attack(self,zombiesDirections):
        if zombiesDirections[0] != []: # attack a zombie nearby
            self.setDirection(zombiesDirections[0][0]) # attack first zombie in the array
        else:
            self.setDirection(zombiesDirections[1][0]) # attack second zombie in the array
        if self.haveAmmo:
            shoot()
        else:
            punch()

    def whereZombie(self,itemsAround=0):
        #Esta funcao recebe o array de items da funcao reconhecimento

        # returns the position of nearby zombies (if they exist)

        directions = {
            0: 'North',
            1: 'East',
            2: 'South',
            3: 'West'
        }

        arrayZombiesDirections = [[],[]]

        # first list inside the array corresponds to yellow
        # second list inside the array corresponds to red

        for i in range(4):
            direction = directions[i]
            zombieColor = itemsAround[i][1]
            if zombieColor == 'Yellow':
                arrayZombiesDirections[0].append(direction)
            elif zombieColor == 'Red':
                arrayZombiesDirections[1].append(direction)

        if arrayZombiesDirections != [[],[]]:
            self.foundZombie = True
        
        return arrayZombiesDirections

    #Funcao que calcula o cheiro na sua casa usando o cheiro de casas adjacentes
    def saveSmell(self,smellsValues):
        #smellsValues[0]-->SmellNorth
        #smellsValues[1]-->SmellEast
        #smellsValues[2]-->SmellSouth
        #smellsValues[3]-->SmellWest

        if ((smellsValues[0] >= 2 and smellsValues[1] >= 2) or
            (smellsValues[1] >= 2 and smellsValues[2] >= 2) or
            (smellsValues[2] >= 2 and smellsValues[3] >= 2) or
            (smellsValues[3] >= 2 and smellsValues[0] >= 2)):
            return 2    #Aqui o valor nao interessa, o importante e que nao seja 0
        else:
            return 0

    #Devolve um array com os valores heuristicos correspondentes
    def addItemsToValues(self,itemsAround=[0,0,0,0]):

        counter = 1
        addValues = []

        if itemsAround != [0,0,0,0]:
            for direction in itemsAround:
                for color in direction:
                    directionValue = 0
                    if counter == 1:
                        directionValue += self.smellValues[color]
                    elif counter == 2:
                        directionValue += self.zombieValues[color]
                    elif counter == 3:
                        directionValue += self.zombieValues[color]
                counter += 1
                addValues.append(directionValue)
        else:
            addValues = [0,0,0,0]
        
        return addValues

    #Adiciona os valores heuristicos dos items as casas adjacentes e calcula a casa com menor valor
    def bestNextHouse(self,itemsAround=None):

        if itemsAround == None:
            itemsAround = [0,0,0,0]

        addValues = self.addItemsToValues(itemsAround)

        if self.posY != 1:
            north = self.realValuesMap[self.posX-1][self.posY-2] + self.heurValueMap[self.posX-1][self.posY-2]+addValues[0]
        else:
            north = 40
        if self.posX != 6:
            east = self.realValuesMap[self.posX][self.posY-1] + self.heurValueMap[self.posX][self.posY-1]+addValues[1]
        else:
            east = 40
        if self.posY != 6:
            south = self.realValuesMap[self.posX-1][self.posY] + self.heurValueMap[self.posX-1][self.posY]+addValues[2]
        else:
            south = 40
        if self.posX != 1:
            west = self.realValuesMap[self.posX-2][self.posY-1] + self.heurValueMap[self.posX-2][self.posY-1]+addValues[3]
        else:
            west = 40

        print('North value: ', str(north))
        print('East value: ', str(east))
        print('South value: ', str(south))
        print('West value: ', str(west))

        min = north # min is the shortest path
        direction = 0
        targetHouse = 'North'

        if min > east:
            min = east
            direction = 1
            targetHouse = 'East'
        if min > south:
            min = south
            direction = 2
            targetHouse = 'South'
        if min > west:
            min = west
            direction = 3
            targetHouse = 'West'
        
        if itemsAround != [0,0,0,0]:
            if itemsAround[direction][2] != 'Green' and itemsAround[direction][1] == 'Green':
                if itemsAround[direction][2] == 'Yellow':
                    self.pickObject = True
                    self.currentPieces+=1
                    if self.currentPieces == 2:
                        for i in range(6)+1:
                            for j in range(6)+1:
                                self.heurValueMap[i][j]=0

                        self.heurValueMap[1][1]=30
                        self.heurValueMap[1][6]=30
                        self.heurValueMap[6][1]=30
                elif itemsAround[direction][2] == 'Red':
                    #FAZER SOM DE CARREGAR BALA!========================================================================
                    self.haveAmmo = True
                
        return targetHouse

    #Calcula a casa para onde deve se movimentar usando a heuristica e movesse para la
    def search(self,colorArray=None):
        targetHouse = self.bestNextHouse(colorArray) #Inserir nesta funçao o array das cores
        self.goDirection(targetHouse)
        if self.pickObject:
            self.forkL.pickObject()
            self.pickObject = False