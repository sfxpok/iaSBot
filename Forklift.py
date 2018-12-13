#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from Motor import LargeMotor

class Forklift():
    def __init__(self):
        self.height = 0
        self.engine = LargeMotor(OUTPUT_C)
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
    engine.on_for_rotations(30, 30, 1.5)

def walkBackwards():
    engine = MoveTank(OUTPUT_A, OUTPUT_B)
    engine.on_for_rotations(-30, -30, 1)

fork = Forklift()
#fork2 = Forklift()

def lookingForObject():

    touch = TouchSensor()
    movtan = MoveTank(OUTPUT_A, OUTPUT_B)

    while (touch.is_pressed):
        fork.moveFork(40)
        walkForward()
        fork.moveFork(-40) # !

        if touch.is_pressed:
            break

        fork.moveFork(40)
        walkForward()
        
    walkBackwards()
    fork.moveFork(-40)
    walkForward()
    fork.moveFork(40)

lookingForObject()