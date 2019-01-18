#!/usr/bin/env python3

###
# Main file from robot here we will call everything we need
###
from random import randint
from ev3dev2 import button
from Map import GameMap
import Attack as at

###
from ev3dev2.sound import Sound
from ev3dev2.display import Display
import ev3dev2.fonts as fonts
from time import sleep
###

# Variable initialization:
world = GameMap()
haveAmmo = False
deliveredPieces = 0
posX = 1
posY = 1
# Definitions:

def updateScreen():

    # info no ecrã: coords do chappie; se tem bala ou não; se existe cheiro à volta do chappie; quantas peças já devolveu
    lcd = Display()
    updateWarning = Sound()
    lcd.draw.text((10, 10), "SB: (" + str(posX) + "," +
                    str(posY) + ")", font=fonts.load('luBS14'))
    lcd.draw.text((10, 20), haveAmmo, font=fonts.load('luBS14'))
    lcd.draw.text((10, 30), deliveredPieces, font=fonts.load('luBS14'))
    lcd.update()
    updateWarning.beep()
    sleep(2)
    # lcd.clear()

def checkButtons():
    while True:
        if button.Button().right:
            return True
        if button.Button().down:
            world.stopAlarm()
        if button.Button().left:
            return False
        if button.Button().up:
            world.repeatTurn()

#Main Loop
while True:
    #if checkButtons():
    if world.listActions():
        break
    Sound().beep()
    Sound().beep()
    Sound().beep()
    print('Clica num botao....')
    x = input()
    #No caso do sensor de cor falhar
    if x == '3':
        world.repeatTurn()