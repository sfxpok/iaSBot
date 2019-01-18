#!/usr/bin/env python3
import sys
from threading import Thread
from Motor import MoveTank
from ev3dev2.sound import Sound
from ev3dev2.display import Display
import ev3dev2.fonts as fonts
from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, LargeMotor
from ev3dev2.sound import Sound
from ColorDetector import ColorDetector
from ev3dev2.sensor.lego import ColorSensor
from Attack import punch, shoot
from Forklift import Fork

#Returns color from sensor
def checkColor():
    color = ColorDetector().getColor()
    print ('the color detected is ', color)
    return color

class GameMap:
    def __init__(self):
        self.engine = MoveTank()
        self.forkL = Fork()
        self.posX = 1
        self.posY = 1
        self.haveAmmo = False
        self.currentPieces = 0
        self.deliveredPieces = 0
        self.levelOneSmell = False
        self.levelTwoSmell = False
        self.direction = "South"
        #self.dirCalibration()
        print(self.direction)
        Sound().speak('Direction ' + self.direction)


        #Mapa de valores reais
        self.realValuesMap = [
                [10,9,8,7,6,5],
                [9,8,7,6,5,4],
                [8,7,6,5,4,3],
                [7,6,5,4,3,2],
                [6,5,4,3,2,1],
                [5,4,3,2,1,0]]
              
        #Mapa de valores heuristicos
        self.heurValueMap = [
                [25,6,8,8,8,30],
                [7,2,2,2,2,7],
                [7,2,3,3,2,7],
                [7,2,3,3,2,7],
                [7,2,2,2,2,7],
                [30,8,8,8,8,30]] 

        #Valores heuristicos das pecas/bala/zombie/cheiros
        self.bulletValue = -28
        self.pieceValue = -20
        self.ZombieValue = 40
        self.danger1Value = 5
        self.danger2Value = 10
        self.danger3Value = 15
        self.danger4Value = 20


        #Valores heuristicos das cores dos cheiros
        self.smellValues = {
            'White': 0,
            'Green': 0, # there is no danger
            'Yellow': self.danger1Value,
            'Red': self.danger2Value,
            'Blue': self.danger3Value,
            'Brown': self.danger4Value
        }

        #Valores heuristicos das cores dos zombies
        self.zombieValues = {
            'White':0,
            'Green': 0, # there is no zombie
            'Yellow': self.ZombieValue, # 2 squares of distance
            'Red': self.ZombieValue, # 1 square of distance
        }

        #Valores heuristicos das cores das peças
        self.pieceValues = {
            'White':0,
            'Green': 0, # there are no pieces
            'Yellow': self.pieceValue,
            'Red': self.bulletValue
        }

        self.lastTurnSmell = 0  #Cheiro do ultimo turno
        self.recFirstLastTurn = False
        self.catchBullet = False #Tem bala para levantar
        self.pickBullet_direction = ''
        self.pickPiece_direction = ''
        self.zombie_direction = ''


        #Variaveis de emergencia
        self.safe_posX = self.posX
        self.safe_posY = self.posY
        self.safe_haveAmmo = self.haveAmmo
        self.safe_currentPieces = self.currentPieces
        self.safe_deliveredPieces = self.deliveredPieces
        self.safe_levelOneSmell = self.levelOneSmell
        self.safe_levelTwoSmell = self.levelTwoSmell
        self.safe_direction = self.direction
        self.safe_heurValueMap = self.heurValueMap
        self.safe_lastTurnSmell = self.lastTurnSmell
        self.safe_recFirstLastTurn = self.recFirstLastTurn
        self.safe_catchBullet = self.catchBullet
        self.safe_pickBullet_direction = self.pickBullet_direction
        self.safe_pickPiece_direction = self.pickPiece_direction
        self.safe_zombie_direction = self.zombie_direction


    #Guardar variaveis de emergencia em caso de o sensor falhar
    def saveTurn(self):
        self.safe_posX = self.posX
        self.safe_posY = self.posY
        self.safe_haveAmmo = self.haveAmmo
        self.safe_currentPieces = self.currentPieces
        self.safe_deliveredPieces = self.deliveredPieces
        self.safe_levelOneSmell = self.levelOneSmell
        self.safe_levelTwoSmell = self.levelTwoSmell
        self.safe_direction = self.direction
        self.safe_heurValueMap = self.heurValueMap
        self.safe_lastTurnSmell = self.lastTurnSmell
        self.safe_recFirstLastTurn = self.recFirstLastTurn
        self.safe_catchBullet = self.catchBullet
        self.safe_pickBullet_direction = self.pickBullet_direction
        self.safe_pickPiece_direction = self.pickPiece_direction
        self.safe_zombie_direction = self.zombie_direction

    #Usar as variaveis de emergencia
    def repeatTurn(self):
        print('Going to repeat turn!')
        self.posX = self.safe_posX
        self.posY = self.safe_posY
        self.haveAmmo = self.safe_haveAmmo
        self.currentPieces = self.safe_currentPieces
        self.deliveredPieces = self.safe_deliveredPieces
        self.levelOneSmell = self.safe_levelOneSmell
        self.levelTwoSmell = self.safe_levelTwoSmell
        self.direction = self.safe_direction
        self.heurValueMap = self.safe_heurValueMap
        self.lastTurnSmell = self.safe_lastTurnSmell
        self.recFirstLastTurn = self.safe_recFirstLastTurn
        self.catchBullet = self.safe_catchBullet
        self.pickBullet_direction = self.safe_pickBullet_direction
        self.pickPiece_direction = self.safe_pickPiece_direction
        self.zombie_direction = self.safe_zombie_direction


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

    #Diz para onde esta virado no inicio
    def dirCalibration(self):
        self.engine.engine.on(15,15)
        firstColor = self.waitforColor()
        self.engine.engine.off()

        self.engine.movementDeg(-272)

        self.engine.turnRight()

        self.engine.engine.on(15,15)
        secondColor = self.waitforColor()
        self.engine.engine.off()

        self.engine.movementDeg(-272)

        self.engine.turnLeft()

        print('First color: ', firstColor)
        print('Second color: ', secondColor)


        #Define a direcao inicial dependendo das duas cores lidas
        if firstColor == 'Red' and secondColor == 'Red':
            return('West')
        elif firstColor == 'Red' and secondColor == 'Black':
            return('North')
        elif firstColor == 'Black' and secondColor == 'Black':
            return('East')
        elif firstColor == 'Black' and secondColor == 'Red':
            return('South') 
        return 'Error'


    def waitforColor(self):
        color = ColorSensor().color_name
        while  color == 'White':
            color = ColorSensor().color_name
            pass
        return color

    #Verifica se a posicao e valida
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

    #Vai para o quadrado numa certa direcao
    def goDirection(self, direction):
        if self.checkInvalidPositions(direction):
            
            #Altera o valor da heuristica para o robo conseguir chegar a casa (2,2)
            if self.posX == 2 and self.posY == 5 and direction == 'North':
                self.heurValueMap[1][2] = 2
                self.heurValueMap[1][1] = 0
            #Faz reset a heuristica do mapa, para assim poder continuar voltas ao mapa
            if self.posX == 2 and self.posY == 3 and direction == 'North':
                self.heurValueMap = [
                [25,6,8,8,8,30],
                [7,2,2,2,2,7],
                [7,2,3,3,2,7],
                [7,2,3,3,2,7],
                [7,2,2,2,2,7],
                [30,8,8,8,8,30]]
            

            print('Going to ', direction, ' from X=', self.posX, 'and Y=', self.posY)
            print('Current direction: ', self.direction)
            self.setDirection(direction)
            distToMoveOneSquareMotorA = 1139
            distToMoveOneSquareMotorB = 1128
            distToMoveOneSquare = (distToMoveOneSquareMotorA + distToMoveOneSquareMotorB)/2
            self.engine.movementDeg(distToMoveOneSquare)
            #Altera as suas coordenadas dependendo da direcao para onde vai
            if direction == 'North':
                self.posY -= 1
            elif direction == 'South':
                self.posY += 1
            elif direction == 'East':
                self.posX += 1
            elif direction == 'West':
                self.posX -= 1

            #Caso chegue a mota com duas pecas
            if self.currentPieces >= 1:
                if (self.posX == 6 and self.posY == 6):
                    self.forkL.dropObject()
                    self.deliveredPieces+=2
                    self.currentPieces-=2
                    sys.exit("Victory!")
        

            # usar isto apenas quando o reconhecimento está desativado
            """ self.heurValueMap[self.posX-1][self.posY-2]+=2
            self.heurValueMap[self.posX][self.posY-1]+=2
            self.heurValueMap[self.posX-1][self.posY]+=2
            self.heurValueMap[self.posX-2][self.posY-1]+=2
            self.heurValueMap[self.posX-1][self.posY-1]+=2 """

            #Dar print da heuristica do mapa(apenas as casas) para testes(Inclinar cabeca para a esquerda)
            # print('Heuristic Map: ',str(self.heurValueMap[5]))
            # print('               ',str(self.heurValueMap[4]))
            # print('               ',str(self.heurValueMap[3]))
            # print('               ',str(self.heurValueMap[2]))
            # print('               ',str(self.heurValueMap[1]))
            # print('               ',str(self.heurValueMap[0]))

            self.updateScreen()

    #Le as 3 cores numa certa direcao
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
            if self.currentPieces < 2:
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


    #Adiciona 2 a heuristica do quadrado para onde vai fazer o reconhecimento
    def addHeurAfterRecog(self,direction):

        if direction == 'North':
            self.heurValueMap[self.posX-1][self.posY-2]+=2
        elif direction == 'East':
            self.heurValueMap[self.posX][self.posY-1]+=2
        elif direction == 'South':
            self.heurValueMap[self.posX-1][self.posY]+=2
        elif direction == 'West':
            self.heurValueMap[self.posX-2][self.posY-1]+=2
           
    #Faz o reconhecimento todo
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

        #Array dos cheiros para o robo determinar o cheiro na sua casa
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
        #Determina o cheiro na sua casa para poder usar no proximo turno
        self.lastTurnSmell = self.saveSmell(smellsValues)

        #Adiciona 2 ao valor heuristico da casa presente apenas no caso que nao tenha duas pecas
        if self.currentPieces < 2:
            self.heurValueMap[self.posX-1][self.posY-1]+=2
        
        return self.itemsAround

    #Vira o robo para uma certa direcao
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
        #Imprime a direcao inicial e guarda os valores de emergencia
        print('Starting direction: ', self.direction)
        self.saveTurn()

        #Realizar esta lista de accoes se o cheiro no ultimo turno era 0
        if self.lastTurnSmell == 0 and not(self.recFirstLastTurn):
            self.search() 
            colorArray = self.fullRecognition()
            self.rememberLastTurn(colorArray)
            zombiesDirections = self.whereZombie(colorArray)
            if zombiesDirections != [[],[]]: # are there zombies nearby?
                self.attack(zombiesDirections)
            self.recFirstLastTurn = False
            
        #Realizar esta lista de accoes caso o cheiro no ultimo turno nao era 0
        else:
            colorArray = self.fullRecognition()
            self.rememberLastTurn(colorArray)
            zombiesDirections = self.whereZombie(colorArray)
            if zombiesDirections[0] != [] or zombiesDirections[1] != []: # Existe zombies por perto?
                self.attack(zombiesDirections)
            self.search(colorArray) 
            self.recFirstLastTurn = True
        
        #Imprime o mapa da heuristica(Inclinar a cabeca para a esquerda)
        print('Heuristic Map: ',str(self.heurValueMap[5]))
        print('               ',str(self.heurValueMap[4]))
        print('               ',str(self.heurValueMap[3]))
        print('               ',str(self.heurValueMap[2]))
        print('               ',str(self.heurValueMap[1]))
        print('               ',str(self.heurValueMap[0]))

        return False


    #Guarda as direcoes dos zombies/pecas/bala para nao se esquecer no proximo turno
    def rememberLastTurn(self, colorArray):

        directions = {
            0: 'North',
            1: 'East',
            2: 'South',
            3: 'West'
        }

        for direction_int in range(4):
            if colorArray[direction_int][1] != 'Green' and colorArray[direction_int][1] != 'White':
                self.zombie_direction = directions[direction_int]
                print('Zombie detected! Direction: ', self.zombie_direction)
            if colorArray[direction_int][2] == 'Yellow':
                self.pickPiece_direction = directions[direction_int]
                print('Piece detected! Direction: ', self.pickPiece_direction)
            if colorArray[direction_int][2] == 'Red':
                self.pickBullet_direction = directions[direction_int]
                print('Bullet detected! Direction: ', self.pickBullet_direction)

    #O robo ataca se houver um zombie. Se ele tiver a bala ele dispara, senao ele da o ataque de machete
    def attack(self,zombiesDirections):
        if zombiesDirections[1] != []: # Priority to attack zombie with piece
            direction_of_attak = zombiesDirections[1][0]
            self.setDirection(direction_of_attak) # attack first zombie in the array
            self.currentPieces+=1
            self.forkL.startAlarm()
            #Limpa a heuristica do mapa(excepto os cantos)
            if self.currentPieces == 2:
                        for i in range(6):
                            for j in range(6):
                                self.heurValueMap[i][j] = 0
                        self.heurValueMap[0][0] = 30
                        self.heurValueMap[0][5] = 30
                        self.heurValueMap[5][0] = 30
        else:
            direction_of_attak = zombiesDirections[0][0]
            self.setDirection(direction_of_attak) # attack second zombie in the array
        if self.haveAmmo:
            self.forkL.setRot(1)
            shoot()
            self.haveAmmo = False
            if direction_of_attak == self.zombie_direction:
                self.zombie_direction = ''
            self.forkL.setRot(6.5)
        else:
            punch()
            self.zombie_direction = direction_of_attak

    #Recebe o array de cores e devolve um array com o tipo de zombies a volta
    #Ex: [['South'],['North']]
    #A primeira
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

        
        return arrayZombiesDirections


    #Funcao que calcula o cheiro na sua casa usando o cheiro de casas adjacentes
    def saveSmell(self,smellsValues):
        #smellsValues[0]-->SmellNorth
        #smellsValues[1]-->SmellEast
        #smellsValues[2]-->SmellSouth
        #smellsValues[3]-->SmellWest

        if ((smellsValues[0] >= 2) or
            (smellsValues[1] >= 2) or
            (smellsValues[2] >= 2) or
            (smellsValues[3] >= 2) or
            (smellsValues[0] >= 1 and smellsValues[1] >= 1) or
            (smellsValues[1] >= 1 and smellsValues[2] >= 1) or
            (smellsValues[2] >= 1 and smellsValues[3] >= 1) or
            (smellsValues[3] >= 1 and smellsValues[0] >= 1)):
            print('Smell different from zero')
            return 2    #Aqui o valor nao interessa, o importante e que nao seja 0
        else:
            print('Smell is zero')
            return 0

    #Devolve um array com os valores heuristicos que e necessario acrescentar as casas
    def addItemsToValues(self,itemsAround=[0,0,0,0]):

        counter = 1
        addValues = []
        
        try:
            if itemsAround != [0,0,0,0]:
                for direction in itemsAround:
                    for color in direction:
                        directionValue = 0
                        if counter == 1:
                            directionValue += self.smellValues[color]
                        elif counter == 2:
                            directionValue += self.zombieValues[color]
                        elif counter == 3:
                            directionValue += self.pieceValues[color]
                        counter += 1
                    counter = 1
                    addValues.append(directionValue)
            else:
                addValues = [0,0,0,0]
        except:
            addValues = [0,0,0,0]

        print('AddValues: ', str(addValues))
        
        return addValues

    #Calcula a casa com menor valor heuristico
    def bestNextHouse(self,itemsAround=None):

        if itemsAround == None:
            itemsAround = [0,0,0,0]

        addValues = self.addItemsToValues(itemsAround)

        if self.posY != 1:
            north = self.realValuesMap[self.posX-1][self.posY-2] + self.heurValueMap[self.posX-1][self.posY-2]+addValues[0]
            print('North value: ', str(north))
            if self.pickPiece_direction == 'North' and addValues[0]<-10:
                north += self.pieceValue
            if self.pickBullet_direction == 'North' and addValues[0]<-18:
                north += self.bulletValue
            if self.zombie_direction == 'North':
                north += self.ZombieValue
        else:
            north = 40

        if self.posX != 6:
            east = self.realValuesMap[self.posX][self.posY-1] + self.heurValueMap[self.posX][self.posY-1]+addValues[1]
            print('East value: ', str(east))
            if self.pickPiece_direction == 'East' and addValues[1]<-10:
                east += self.pieceValue
            if self.pickBullet_direction == 'East' and addValues[1]<-18:
                east += self.bulletValue
            if self.zombie_direction == 'East':
                east += self.ZombieValue
        else:
            east = 40

        if self.posY != 6:
            south = self.realValuesMap[self.posX-1][self.posY] + self.heurValueMap[self.posX-1][self.posY]+addValues[2]
            print('South value: ', str(south))
            if self.pickPiece_direction == 'South' and addValues[2]<-10:
                south += self.pieceValue
            if self.pickBullet_direction == 'South' and addValues[2]<-18:
                south += self.bulletValue
            if self.zombie_direction == 'South':
                south += self.ZombieValue                            
        else:
            south = 40

        if self.posX != 1:
            west = self.realValuesMap[self.posX-2][self.posY-1] + self.heurValueMap[self.posX-2][self.posY-1]+addValues[3]
            print('West value: ', str(west))
            if self.pickPiece_direction == 'West' and addValues[3]<-10:
                west += self.pieceValue
            if self.pickBullet_direction == 'West' and addValues[3]<-18:
                west += self.bulletValue
            if self.zombie_direction == 'West':
                west += self.ZombieValue
        else:
            west = 40

        print('North value: ', str(north))
        print('East value: ', str(east))
        print('South value: ', str(south))
        print('West value: ', str(west))

        min = north # min is the shortest path
        targetHouse = 'North'

        if min > east:
            min = east
            targetHouse = 'East'
        if min > south:
            min = south
            targetHouse = 'South'
        if min > west:
            min = west
            targetHouse = 'West'

        #Dar print da heuristica do mapa(apenas as casas) para testes(Inclinar cabeca para a esquerda)
        print('Heuristic Map: ',str(self.heurValueMap[5]))
        print('               ',str(self.heurValueMap[4]))
        print('               ',str(self.heurValueMap[3]))
        print('               ',str(self.heurValueMap[2]))
        print('               ',str(self.heurValueMap[1]))
        print('               ',str(self.heurValueMap[0]))
                
        return targetHouse

    #Calcula a casa para onde deve se movimentar usando a heuristica e movesse para la
    def search(self,colorArray=None):
        targetHouse = self.bestNextHouse(colorArray)
        self.goDirection(targetHouse)
        #Caso tenha uma peca para onde o robo se movimentou
        if self.pickPiece_direction == targetHouse:
            self.forkL.pickObject()
            self.currentPieces+=1
            self.forkL.startAlarm()
            #Limpa a heuristica do mapa(excepto os cantos)
            if self.currentPieces == 2:
                for i in range(6):
                    for j in range(6):
                        self.heurValueMap[i][j]=0

                self.heurValueMap[0][1]=30
                self.heurValueMap[0][5]=30
                self.heurValueMap[5][0]=30
        #Caso tenha uma bala para onde o robo se movimentou
        elif self.pickBullet_direction == targetHouse:
            print('Apanhei uma bala!!!\n\n\n\n\n')
            Sound().play('/home/robot/iaSBot/sound/load.wav')
            self.haveAmmo = True
        #Dar reset as direcoes das pecas/bala/zombies
        self.zombie_direction = ''
        self.pickPiece_direction = ''
        self.pickBullet_direction = '' 
            

    def stopAlarm(self):
        self.forkL.stopAlarm()
    
