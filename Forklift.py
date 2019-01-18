#!/usr/bin/env python3

from Motor import LargeMotor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import OUTPUT_C
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from Motor import MoveTank
import time
import threading

class Fork:
    def __init__(self):
        self.fork = LargeMotor(OUTPUT_C)
        self.fork.movementRot(7)
        self.maxRot = 7
        self.currentRot = 0
        # threading.Thread(target=self.waitForSensor, daemon=True).start()
        # self.calibration()
        self.forkLiftDown()
        #self.maxRot = round(self.maxRot, 2)
        self.setRot(7)
        Sound().speak('Forklift, ready')
        self.leds = Leds()

    def startAlarm(self):
        self.alarmLoop = True
        threading.Thread(target=self.alarm, daemon=True).start()
    
    def stopAlarm(self):
        self.alarmLoop = False
        self.leds.all_off()
        self.leds.set_color('LEFT', 'GREEN')
        self.leds.set_color('RIGHT', 'GREEN')

    def alarm(self):
        color = 0
        while self.alarmLoop:
            #Sound().beep()
            if color == 0:
                self.leds.set_color('LEFT', 'RED')
                color = 1
                time.sleep(1)
            else:
                self.leds.set_color('RIGHT', 'GREEN')
                color = 0
                time.sleep(1)
            self.leds.all_off()   
            time.sleep(1)

    # def calibration(self):
    #     while self.loop:
    #         self.loop = True
    #         self.fork.movementRot(-0.2)
    #         self.maxRot += 0.2
    
    def waitForSensor(self):
        self.loop = True
        time.sleep(1)
        TouchSensor().wait_for_pressed()
        self.loop = False

    def getRot(self):
        return self.currentRot

    # def setRot(self, rot):
    #     if rot <= self.maxRot and rot >= -0.5 and rot != self.currentRot:
    #         if self.currentRot <= rot:
    #             threading.Thread(target=self.waitForSensor, daemon=True).start()
    #             while self.loop and self.currentRot < rot:
    #                 self.currentRot += 0.2
    #                 self.fork.movementRot(0.2)
    #         else:
    #             while self.loop and self.currentRot > rot:
    #                 self.currentRot -= 0.2
    #                 self.fork.movementRot(-0.2)

    def setRot(self, rot):
        while(self.currentRot != rot):
            if self.currentRot <= rot:
                self.currentRot += 0.5
                self.fork.movementRot(0.5)
            else:
                self.currentRot -= 0.5
                self.fork.movementRot(-0.5)

    def objDetector(self):
        lastCurrent = self.currentRot
        self.setRot(6)
        threading.Thread(target=self.waitForSensor, daemon=True).start()
        while self.loop:
            self.currentRot -= 0.2
            self.fork.movementRot(-0.2)

        if round(self.currentRot, 2) > 0.6:
            self.setRot(7)
            return True
        else:
            self.setRot(7)
            return False

        
    def pickObject(self):
        # self.setRot(6)
        MoveTank().movementRot(-1)
        self.forkLiftDown()
        MoveTank().movementRot(1)
        self.setRot(7)
        # if self.objDetector():
        #     MoveTank().movementRot(-1)
        #     self.setRot(1.2)
        #     MoveTank().movementRot(1)
        #     self.setRot(6.5) # max height possible
        #     self.startAlarm()
       
    #Brings forklift to the lowest position (where the sensor touches something)
    def forkLiftDown(self):
        self.fork.engine.on(-20)
        TouchSensor().wait_for_pressed()
        self.fork.engine.off()
        self.currentRot = 0

    def dropObject(self):
        lastCurrent = self.currentRot
        #self.setRot(1.2)
        self.forkLiftDown()
        self.stopAlarm()
        MoveTank().movementRot(-1)
        self.setRot(lastCurrent)
