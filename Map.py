#!/usr/bin/env python3
from threading import Thread
from Motor import MoveTank
from ColorSensor import checkColor
from ev3dev2.sound import Sound
from ev3dev2.display import Display
import ev3dev2.fonts as fonts
from time import sleep

class Map:
    def __init__(self):
        self.engine = MoveTank()
        self.posX = 1
        self.posY = 1
        self.direction = self.dirCalibration()

        #Sound().speak('Position locked, facing ' + self.direction)

    def updateScreen(self, posX, posY):
        lcd =  Display()
        updateWarning = Sound()

        lcd.draw.text((10,10), "SB: (" + str(posX) + "," + str(posY) + ")", font=fonts.load('luBS14'))

        lcd.update()
        updateWarning.beep()
        sleep(5)
        #lcd.clear()

    def dirCalibration(self):
        self.dead = False
        Thread(target=self.walking, daemon=True).start()
        firstColor = self.waitforColor()
        print('entra1')
        MoveTank().turnRight()
        print('sai1')

        Thread(target=self.walking, daemon=True).start()
        secondColor = self.waitforColor()
        print('entra2')
        MoveTank().turnLeft()
        print('sai2')
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

    def goDirection(self, direction):
        self.setDirection(direction)
        self.engine.startEngine()
        moving = 0
        while checkColor() == 'White':
            moving += 1
        while moving > 0:
            moving -= 1
        self.engine.stopEngine()


    def setDirection(self, direction):
        if self.direction != direction:
            if direction == 'North':
                if self.direction == 'South':
                    self.engine.turnRight()
                    self.engine.turnRight()

                if self.direction == 'East':
                    self.engine.turnRight()

                if self.direction == 'West':
                    self.engine.turnLeft()
            

            if direction == 'South':
                if self.direction == 'North':
                    self.engine.turnRight()
                    self.engine.turnRight() 

                if self.direction == 'West':
                    self.engine.turnRight()

                if self.direction == 'East':
                    self.engine.turnLeft()
            

            if direction == 'East':
                if self.direction == 'West':
                    self.engine.turnRight()
                    self.engine.turnRight() 

                if self.direction == 'South':
                    self.engine.turnRight()

                if self.direction == 'North':
                    self.engine.turnLeft()
            
            if direction == 'West':
                if self.direction == 'East':
                    self.engine.turnRight()
                    self.engine.turnRight() 

                if self.direction == 'North':
                    self.engine.turnRight()

                if self.direction == 'South':
                    self.engine.turnLeft()
        
        self.direction = direction
                

                            

                    
a = Map()