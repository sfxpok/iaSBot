#!/usr/bin/env python3
from ev3dev2 import button
from ev3dev2.sensor.lego import ColorSensor
from gameGenerator import *
from Motor import *
from ColorSensor import *

def checkColor():
    color = ColorSensor().color_name
    return color

def checkButtons():
    print('A CORRER')
    while True:
        if button.Button().up:
            print('Button UP pressed')
        if button.Button().down:
            print('Button DOWN pressed')
        if button.Button().left:
            print('Button LEFT pressed')
        if button.Button().right:
            print('Button RIGHT pressed')
        if button.Button().enter:
            print('Button ENTER pressed')
        
class InitDir():
    def __init__(self):
        print('Test Start')
        self.dead = False

        threading.Thread(target=self.walking, daemon=True).start()
        self.firstColor = self.waitforColor()
        MoveTank().turnRight()
        
        threading.Thread(target=self.walking, daemon=True).start()
        self.secondColor = self.waitforColor()
        MoveTank().turnLeft()

        self.currentDir()
        print('End of Test')

    def walking(self):
        self.loop = True
        self.movement = 0

        while self.loop:
            MoveTank().movementDeg(75)
            self.movement += 75
            
        self.dead = True
        print('Thread died')

    def waitforColor(self):
        while checkColor() == 'White':
            None
        self.loop = False
        color = checkColor()
        print('Color detected ', color)
        while not self.dead:
            None
        MoveTank().movementDeg(-self.movement)
        return color

    def currentDir(self):
        if self.firstColor == 'Red' and self.secondColor == 'Red':
            print('West')
        elif self.firstColor == 'Red' and self.secondColor == 'Black':
            print('North')
        elif self.firstColor == 'Black' and self.secondColor == 'Black':
            print('East')
        elif self.firstColor == 'Black' and self.secondColor == 'Red':
            print('South')