#!/usr/bin/env python3

###
# Ficheiro "principal" do projeto. Maior parte do código vai estar aqui definido, portanto o propósito do código que se vê aqui
# pode variar.
###

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedRPM, MoveTank, MoveJoystick, MediumMotor, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from hardware import *
from gameGenerator import *

# TODO: Add code here

robotMotors = Motor()
robotSensors = Sensor()
forklift = Forklift()
gameWorld = mapBehaviour()
survivorBot = Robot()
bike = Bike()
sound = Sound()

sound.speak("Running")

def calculateCraneHeight(height):
    forklift.height += height

def moveCrane(speed, rotations): # see how much the forklift needs to go to 0cm up to 5cm
    robotMotors.forklift.on_for_rotations(SpeedRPM(speed), rotations)
    height = speed / rotations
    forklift.height += height

def punchZombie(zombie):
    robotMotors.leftLeg.on_for_rotations(10, 1) # aim the punch
    robotMotors.attack.on_for_rotations(-50, 4) # punch, negative axis
    stunZombie(zombie)

def shootZombie(robot, zombie):
    robotMotors.attack.on_for_rotations(50, 4) # bullet, positive axis
    killZombie(robot, zombie)

def playAlarm():
    gameWorld.alarm = True
    # set zombies on alarm

def stopAlarm():
    gameWorld.alarm = False
    # set zombies to default behaviour

def getBikePiece(character): # character is either survivorBot or zombie
    playAlarm()
    character.bikePieces += 1

def dropBikePiece(character): # character is either survivorBot or zombie
    stopAlarm()
    character.bikePieces -= 1

def killRobot(robot):
    robot.isDead = True
    endGame()

def killZombie(robot, zombie):
    zombie.isDead = True
    
    if zombie.bikePieces:
        robot.bikePieces += zombie.bikePieces

def stunZombie(zombie):
    zombie.isStunned = True
    zombie.turnsUnableToPlay = 2

def stunHasPassed(zombie):
    zombie.isStunned = False

def isBikeFixed(robot):
    if robot.bikePieces:
        bike.mountedPieces += robot.bikePieces
    elif bike.mountedPieces == 2:
        endGame()

def endGame():
    sound.speak("Victory")
    exit(0)
    
robotMotors.forklift.on_for_rotations(50, 8)
print('ROTACOES SUBIR: ' + str(robotMotors.forklift.rotations))
rotUp = robotMotors.forklift.rotations

robotMotors.forklift.on_for_rotations(-100, 8)

#robotMotors.forklift.on_for_seconds(100, 10)
#robotMotors.forklift.on_for_seconds(-100, 10)

#robotMotors.doubleJoystick.on(-1, -1, 50)
#robotMotors.doubleWalk.on_for_rotations(100, -100, 6)
#robotMotors.leftLeg.on_for_rotations(100, 5)
#robotMotors.rightLeg.on_for_rotations(100, 5)

sumOfDistanceCrane = 0

while robotSensors.touch.is_released:
    robotMotors.forklift.on_for_rotations(-50, 4)
    sumOfDistanceCrane += 1
    #print(str(sumOfDistanceCrane))
    print('ROTACOES DESCER: ' + str(robotMotors.forklift.rotations))

rotDown = robotMotors.forklift.rotations
difDist = rotUp - rotDown

print('total: ' + str(sumOfDistanceCrane))
print('dif de distancia: ' + str(difDist))

#def moveRobot():
    # to be defined

#def reconSurroundings():
    # to be defined

#def playRobot():
    # to be defined

#def playZombie():
    # to be defined