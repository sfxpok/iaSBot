#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveTank
from Motor import MediumMotor
from ev3dev2.sound import Sound
import time


def punch():
    engine = MediumMotor(OUTPUT_D, 100)
    mov = MoveTank(OUTPUT_A, OUTPUT_B)
    print('Punching!')
    time.sleep(1)
    mov.on_for_degrees(30,-30, 100)    
    time.sleep(0.001)
    engine.movementDeg(-362)
    engine.movementDeg(-362)
    mov.on_for_degrees(-30, 30, 100)
    time.sleep(0.001)


def shoot():
    engine = MediumMotor(OUTPUT_D, 50)
    print('Shoooting')
    engine.movementDeg(362)
    



