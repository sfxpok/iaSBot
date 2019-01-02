#!/usr/bin/env python3
from threading import Thread
from Motor import MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.display import Display
import ev3dev2.fonts as fonts
from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, LargeMotor
from ev3dev2.sound import Sound


def checkColor():
    color = ColorSensor().color_name
    return color

class Map:
    def __init__(self):
        self.engine = MoveTank()
        self.housesChecked = []
        self.posX = 1
        self.posY = 1
        self.haveAmmo = False
        self.deliveredPieces = 0
        self.levelOneSmell = False
        self.levelTwoSmell = False
        self.direction = self.dirCalibration()
        print(self.direction)
        Sound().speak('Direction ' + self.direction)

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
        self.dead = False
        ColorSensor().calibrate_white()
        Thread(target=self.walking, daemon=True).start()
        firstColor = self.waitforColor()
        MoveTank().turnRight()

        Thread(target=self.walking, daemon=True).start()
        secondColor = self.waitforColor()
        MoveTank().turnLeft()

        if firstColor == 'Red' and secondColor == 'Red':
            return('West')
        elif firstColor == 'Red' and secondColor == 'Black':
            return('North')
        elif firstColor == 'Black' and secondColor == 'Black':
            return('East')
        elif firstColor == 'Black' and secondColor == 'Red':
            return('South') 

    def walking(self):
        self.loop = True
        self.movement = 0
        while self.loop:
            MoveTank().movementDeg(75)
            self.movement += 75 
        self.dead = True

    def waitforColor(self):
        while checkColor() == 'White':
            pass
        self.loop = False
        color = checkColor()
        print('Color detected ', color)
        while not self.dead:
            pass
        MoveTank().movementDeg(-self.movement)
        return color

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

    def recognize(self):
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
        ColorSensor().calibrate_white()
        a = MoveTank()
        #if self.checkInvalidPositions():
        a.engine.on(20,20)
        while ColorSensor().color_name != 'Black':
            pass
        a.engine.off()
        color = [None] * 3
        a.movementDeg(91)
        color[0] = checkColor()
        a.movementDeg(182)
        color[1] = checkColor()
        a.movementDeg(182)
        color[2] = checkColor()

        a.movementDeg(-727)
        return color    

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
        for i in range(3):
            if self.itemsAround[i] == 'White' or self.itemsAround[i] == 'Black':
                self.itemsAround[i] = None
        
        return self.itemsAround

    def checkHouse(self, direction):
        if direction == 'North':
            self.housesChecked.append(str(str(self.posX)+','+str(self.posY-1)))
        elif direction == 'East':
            self.housesChecked.append(str(str(self.posX+1)+','+str(self.posY)))
        elif direction == 'South':
            self.housesChecked.append(str(str(self.posX)+','+str(self.posY+1)))
        elif direction == 'West':
            self.housesChecked.append(str(str(self.posX-1)+','+str(self.posY)))
        else:
            self.housesChecked.append(str(str(self.posX)+','+str(self.posY)))

    def setDirection(self, direction):
        if self.direction != direction:
            if direction == 'North':
                if self.direction == 'South':
                    self.engine.turnRight()
                    self.engine.turnRight()

                if self.direction == 'West':
                    self.engine.turnRight()

                if self.direction == 'East':
                    self.a.turnLeft()

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
