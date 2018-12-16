#!/usr/bin/env python3

from Motor import LargeMotor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import OUTPUT_C
from ev3dev2.sound import Sound
from Motor import MoveTank
import time
import threading


class Forklift:
    def __init__(self):
        self.fork = LargeMotor(OUTPUT_C)
        self.fork.movementRot(8)
        self.maxRot = self.currentRot = 0
        threading.Thread(target=self.waitForSensor, daemon=True).start()
        self.calibration()
        self.maxRot = round(self.maxRot, 2)
        self.setRot(5)
        Sound().speak('Forklift, ready')
    
    def calibration(self):
        while self.loop:
            self.loop = True
            self.fork.movementRot(-0.2)
            self.maxRot += 0.2
    
    def waitForSensor(self):
        self.loop = True
        time.sleep(1)
        TouchSensor().wait_for_pressed()
        self.loop = False

    def getRot(self):
        return self.currentRot

    def setRot(self, rot):
        if rot <= self.maxRot and rot >= -0.5 and rot != self.currentRot:
            threading.Thread(target=self.waitForSensor, daemon=True).start()
            if self.currentRot <= rot:
                while self.loop and self.currentRot < rot:
                    self.currentRot += 0.2
                    self.fork.movementRot(0.2)
            else:
                while self.loop and self.currentRot > rot:
                    self.currentRot -= 0.2
                    self.fork.movementRot(-0.2)

    def objDetector(self):
        lastCurrent = self.currentRot
        self.setRot(5)
        threading.Thread(target=self.waitForSensor, daemon=True).start()
        while self.loop:
            self.currentRot -= 0.2
            self.fork.movementRot(-0.2)
        if round(self.currentRot, 2) > 0.6:
            self.setRot(lastCurrent)
            return True
        else:
            self.setRot(lastCurrent)
            return False

        
    def pickObject(self):
        self.setRot(5)
        trys = 2
        while trys > 0:
            if self.objDetector():
                MoveTank().movementRot(-1)
                self.setRot(-0.2)
                MoveTank().movementRot(1)
                self.setRot(5)
                break
            else:
                MoveTank().movementRot(1)
                trys -= 1

    
a = Forklift()
