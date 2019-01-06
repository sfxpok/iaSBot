#!/usr/bin/env python3

###
from ev3dev2.sound import Sound
from ev3dev2.display import Display
import ev3dev2.fonts as fonts
from time import sleep
import threading
from ev3dev2 import button
###

# Variable initialization:
haveAmmo = False
levelOneSmell = False
levelTwoSmell = False
deliveredPieces = 0
posX = 1
posY = 1
# Definitions:

def updateScreen():

    # info no ecrã: coords do chappie; se tem bala ou não; se existe cheiro à volta do chappie; quantas peças já devolveu
    lcd = Display()
    updateWarning = Sound()
    lcd.draw.text((10, 10), "Chappie: (" + str(posX) + "," + str(posY) + ")", font=fonts.load('luBS14'))
    lcd.draw.text((10, 20), "O Chappie tem a bala?: " + str(haveAmmo), font=fonts.load('luBS14'))
    lcd.draw.text((10, 30), "Peças na mota: " + str(deliveredPieces), font=fonts.load('luBS14'))
    lcd.draw.text((10, 40), "Cheiro nível 1?: " + str(levelOneSmell), font=fonts.load('luBS14'))
    lcd.draw.text((10, 50), "Cheiro nível 2?: " + str(levelTwoSmell), font=fonts.load('luBS14'))
    lcd.update()
    updateWarning.beep()
    sleep(2)
    # lcd.clear()

def updateScreenLoop():

    lcd = Display()

    while True:
        # info no ecrã: coords do chappie; se tem bala ou não; se existe cheiro à volta do chappie; quantas peças já devolveu

        # carregar nos botões do Brickman não interrompe o output de texto para o ecrã, apenas por uns segundos (a duração está)
        # dependente da duração dada ao sleep()

        #updateWarning = Sound()
        lcd.draw.text((10, 10), "Chappie: (" + str(posX) + "," + str(posY) + ")", font=fonts.load('luBS14'))
        lcd.draw.text((10, 20), "Bala?: " + str(haveAmmo), font=fonts.load('luBS14'))
        lcd.draw.text((10, 30), "Peças na mota: " + str(deliveredPieces), font=fonts.load('luBS14'))
        lcd.draw.text((10, 40), "Cheiro nível 1?: " + str(levelOneSmell), font=fonts.load('luBS14'))
        lcd.draw.text((10, 50), "Cheiro nível 2?: " + str(levelTwoSmell), font=fonts.load('luBS14'))
        lcd.update()
        #updateWarning.beep()
        sleep(10)
        # lcd.clear()

def checkButtons():
    while True:
        if button.Button().right:
            Sound().speak("Button pressed")
        if button.Button().left:
            Sound().speak("Button pressed")
        if button.Button().up:
            Sound().speak("Button pressed")
        if button.Button().down:
            Sound().speak("Button pressed")

threading.Thread(target=updateScreenLoop).start()