#!/usr/bin/env python3

###
# Main file from robot here we will call everything we need
###
from random import randint
from ev3dev2 import button
from Forklift import Forklift
from Map import Map
import Attack as at

#Variable initialization:
fork = Forklift()
world = Map()
haveAmmo = False
#Definitions:

def checkButtons():
    while True:
        if button.Button().right:
            return True
        if button.Button().down:
            fork.stopAlarm()
        if button.Button().backspace:
            return False    
        """ if button.Button().left:
            print('Button LEFT pressed')
        if button.Button().right:
            print('Button RIGHT pressed')
        if button.Button().enter:
            print('Button ENTER pressed')
        """

#Main loop:
while True:
    if checkButtons():
        itemsAround = world.fullRecognition()   #Get all objets arround me
        
        if itemsAround[0] == 'Green':
            world.goDirection('North')
            haveAmmo = True
            continue
        if itemsAround[1] == 'Green':
            world.goDirection('East')
            haveAmmo = True
            continue

        if itemsAround[2] == 'Green':
            world.goDirection('South')
            haveAmmo = True
            continue

        if itemsAround[3] == 'Green':
            world.goDirection('West')
            haveAmmo = True
            continue


            
        if itemsAround[0] == 'Blue':
            world.goDirection('North')
            fork.pickObject()
            continue

        if itemsAround[1] == 'Blue':
            world.goDirection('East')
            fork.pickObject()
            continue

        if itemsAround[2] == 'Blue':
            world.goDirection('South')
            fork.pickObject()
            continue

        if itemsAround[3] == 'Blue':
            world.goDirection('West')
            fork.pickObject()
            continue


        if itemsAround[0] == 'Brown':
            world.setDirection('North')
            if haveAmmo:
                at.shoot()
            else:
                at.punch()
            i = randint(0,2)
            if i == 0:
                world.goDirection('East')
                continue
            if i == 1:
                world.goDirection('South')
                continue
            if i == 2:
                world.goDirection('West')
                continue

        if itemsAround[1] == 'Brown':
            world.setDirection('East')
            if haveAmmo:
                at.shoot()
            else:
                at.punch()
            i = randint(0,2)
            if i == 0:
                world.goDirection('North')
                continue
            if i == 1:
                world.goDirection('South')
                continue
            if i == 2:
                world.goDirection('West')
                continue

        if itemsAround[2] == 'Brown':
            world.setDirection('South')
            if haveAmmo:
                at.shoot()
            else:
                at.punch()
            i = randint(0,2)
            if i == 0:
                world.goDirection('North')
                continue
            if i == 1:
                world.goDirection('East')
                continue
            if i == 2:
                world.goDirection('West')
                continue

        if itemsAround[3] == 'Brown':
            world.setDirection('West')
            if haveAmmo:
                at.shoot()
            else:
                at.punch()
            i = randint(0,2)
            if i == 0:
                world.goDirection('North')
                continue
            if i == 1:
                world.goDirection('East')
                continue
            if i == 2:
                world.goDirection('South')
                continue
        print('aqui')
        i = randint(0,3)
        if i == 0:
            world.goDirection('North')
            continue
        if i == 1:
            world.goDirection('East')
            continue
        if i == 2:
            world.goDirection('South')
            continue
        if i == 3:
            world.goDirection('West')
            continue


        




        