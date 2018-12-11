#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveJoystick, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from hardware import *

# TODO: Add code here

#bool hasBullet

def calculateCraneHeight(height):
    crane.dist += height

def moveCrane(speed, rotations):
    robotMotors.crane.on_for_rotations(speed, rotations)
    height = speed / rotations
    crane.dist += height

robotMotors = Motor()
robotSensors = Sensor()
crane = Crane()

sound = Sound()
sound.speak("Running")

def attack(punch, bullet): # binary values
    if punch:
        robotMotors.leftLeg.on_for_rotations(10, 1) # apontar o soco
        robotMotors.attackZombie.on_for_rotations(-50, 4) # soco
    elif bullet:
        robotMotors.attackZombie.on_for_rotations(50, 4) # bala

robotMotors.crane.on_for_rotations(50, 8)
print('ROTACOES SUBIR: ' + str(robotMotors.crane.rotations))
rotUp = robotMotors.crane.rotations

robotMotors.crane.on_for_rotations(-100, 8)

#robotMotors.crane.on_for_seconds(100, 10)
#robotMotors.crane.on_for_seconds(-100, 10)

#robotMotors.doubleJoystick.on(-1, -1, 50)
#robotMotors.doubleWalk.on_for_rotations(100, -100, 6)
#robotMotors.leftLeg.on_for_rotations(100, 5)
#robotMotors.rightLeg.on_for_rotations(100, 5)

sumOfDistanceCrane = 0

while robotSensors.touch.is_released:
    robotMotors.crane.on_for_rotations(-50, 4)
    sumOfDistanceCrane += 1
    #print(str(sumOfDistanceCrane))
    print('ROTACOES DESCER: ' + str(robotMotors.crane.rotations))

rotDown = robotMotors.crane.rotations
difDist = rotUp - rotDown

print('total: ' + str(sumOfDistanceCrane))
print('dif de distancia: ' + str(difDist))
 