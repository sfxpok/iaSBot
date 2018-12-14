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

    def calibrateFork(self):

        minHeight = 0
        maxHeight = 1850
        heightToPressTouch = -350

        touch = TouchSensor()

        file_object = open("/sys/class/tacho-motor/motor3/position", "r+")
        file_object.write('0')
        #file_object.close()

        #file_object = open("/sys/class/tacho-motor/motor3/position", "r")
        intPos = file_object.read()
        file_object.close()

        #while not(touch.value()):
            #self.engine.movementRot(-30)

        #currentHeight = heightToPressTouch

        #self.engine.movementRot(30)

        

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height

    def moveFork(self, height):
       self.engine.movementRot(height)

    def lookingForObject(self):

        touch = TouchSensor()
        movtan = MoveTank(OUTPUT_A, OUTPUT_B)
        foundBikePiece = 0

        #min height: 0
        #max height: 1850
        #not sure
        #to press touch sensor: -350

        file_object = open("/sys/class/tacho-motor/motor3/position", "r")

        for line in file_object:
            if line.strip():
                intPos = int(line)
    
        print(intPos)

        #while intPos > -350:
        fork.moveFork(0.1)
        walkForward()

        while intPos > -350 or foundBikePiece != 0:
            fork.moveFork(-1) # descobre se existe uma peça onde se situa
            if touch.value():
                foundBikePiece = 1

                for line in file_object:
                    if line.strip():
                        intPos = int(line)
        
            print(intPos)

            #fork.moveFork(10)
            #walkForward()

        fork.moveFork(0.1)    
        walkBackwards()

        while intPos > 0:
            fork.moveFork(-0.1)
            intPos = file_object.read()

        walkForward()
        fork.moveFork(2)
        walkBackwards()

def walkForward():
    engine = MoveTank(OUTPUT_A, OUTPUT_B)
    #engine.on_for_rotations(30, 30, 1.5)
    engine.movementRot(3)

def walkBackwards():
    engine = MoveTank(OUTPUT_A, OUTPUT_B)
    #engine.on_for_rotations(-30, -30, 1)
    engine.movementRot(-3)

fork = Forklift()
#fork2 = Forklift()

fork.calibrateFork()
#fork.lookingForObject()