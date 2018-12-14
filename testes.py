#!/usr/bin/env python3

from Motor import LargeMotor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import OUTPUT_C
from ev3dev2.sound import Sound
import threading


class Forklift:
    def __init__(self):
        self.emp = LargeMotor(OUTPUT_C)
        self.emp.movementRot(8)
        self.maxRot = 0
        self.loop = True
        threading.Thread(target=self.calibration, daemon=True).start()    
        self.calibrationAUX()
        Sound().speak('Forklift, ready')
    
    def calibration(self):
        while self.loop:
            self.emp.movementRot(-0.1)
            self.maxRot += 0.1
            round(self.maxRot, 2)
    
    def calibrationAUX(self):
        TouchSensor().wait_for_pressed()
        self.loop = False

a = Forklift()

"""
from ev3dev2.sound import Sound
from time import sleep

ts = TouchSensor()
sound = Sound()

def tones_forever():
    # global loop # NOT NEEDED
    while loop:  # Same as while loop == True
        sound.play_tone(1000, 0.2)  # 1000Hz for 0.2s
        sleep(0.5)

loop = True
t = Thread(target=tones_forever)
t.start()

for i in range(0,5):
    print('here')
    ts.wait_for_bump()

sound.beep()
loop = False """
# So that the loop in the tones_forever thread stops looping