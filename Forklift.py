#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from Motor import LargeMotor, MoveTank

class Forklift():
    def __init__(self):
        self.height = 0
        self.engine = LargeMotor(OUTPUT_C, 30)
        #self.cal()

    #def cal(self):
     #   self.engine.movementRot(50)
      #  self.heightMax = self.engine.getPosition()
        

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def moveFork(self, height):
       self.engine.movementRot(height)

def walkForward():
    engine = MoveTank(OUTPUT_A, OUTPUT_B)
    #engine.on_for_rotations(30, 30, 1.5)
    engine.movementRot(30, 30, 1.5)

def walkBackwards():
    engine = MoveTank(OUTPUT_A, OUTPUT_B)
    #engine.on_for_rotations(-30, -30, 1)
    engine.movementRot(-30, -30, 1)

fork = Forklift()
#fork2 = Forklift()

def lookingForObject():

    touch = TouchSensor()
    movtan = MoveTank(OUTPUT_A, OUTPUT_B)
    foundBikePiece = 0

    while not(touch.value()):
        fork.moveFork(10)
        walkForward()

        while not(touch.value()):
            fork.moveFork(-1) # descobre se existe uma peça onde se situa
            if touch.value()
                foundBikePiece = 1

        #fork.moveFork(10)
        #walkForward()

    fork.moveFork(1)    
    walkBackwards()

    while not(touch.value()):
        fork.moveFork(-1)

    walkForward()
    fork.moveFork(10)
    walkBackwards()

#lookingForObject()