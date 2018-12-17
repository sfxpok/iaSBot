#!/usr/bin/env python3

from Motor import LargeMotor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import OUTPUT_C
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
from Motor import MoveTank
import time
import threading

class Forklift:
    def __init__(self):
        self.fork = LargeMotor(OUTPUT_C)
        self.fork.movementRot(7)
        self.maxRot = self.currentRot = 0
        threading.Thread(target=self.waitForSensor, daemon=True).start()
        self.calibration()
        self.maxRot = round(self.maxRot, 2)
        self.setRot(5)
        Sound().speak('Forklift, ready')
        self.leds = Leds()

    def startAlarm(self):
        self.alarmLoop = True
        threading.Thread(target=self.alarm, daemon=True).start()
    
    def stopAlarm(self):
        self.alarmLoop = False
        self.leds.set_color('LEFT', 'GREEN')
        self.leds.set_color('RIGHT', 'GREEN')

    def alarm(self):
        while self.alarmLoop:
            Sound().beep()
            color = 1
            if color == 1:
                self.leds.set_color('LEFT', 'RED')

                Leds.set(Leds.LEFT, brightness_pct=1, trigger="timer")
                time.sleep(0.1)
                Leds.set(Leds.LEFT, delay_on=2000)

                self.leds.set_color('RIGHT', 'GREEN')
                color = 0
            else:
                self.leds.set_color('RIGHT', 'RED')

                Leds.set(Leds.LEFT, brightness_pct=1, trigger="timer")
                time.sleep(0.1)
                Leds.set(Leds.LEFT, delay_on=2000)

                self.leds.set_color('LEFT', 'GREEN')
                color = 1

            time.sleep(1)




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
                self.setRot(1.2)
                MoveTank().movementRot(1)
                self.setRot(5)
                self.startAlarm()
                break
            else:
                MoveTank().movementRot(1)
                trys -= 1
    
    def dropObject(self):
        lastCurrent = self.currentRot
        self.setRot(1.2)
        self.stopAlarm()
        MoveTank().movementRot(-1)
        self.setRot(lastCurrent)
