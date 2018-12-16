#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveTank
from Motor import MediumMotor

def punch():
    engine = MediumMotor(OUTPUT_D, 100)
    mov = MoveTank(OUTPUT_A, OUTPUT_B)
    print('Punching!')
    mov.on_for_degrees(30,-30, 100)    
    engine.movementDeg(-362)
    engine.movementDeg(-362)
    mov.on_for_degrees(-30, 30, 100)

def shoot():
    engine = MediumMotor(OUTPUT_D, 50)
    print('Shooting')
    engine.movementDeg(362)
    