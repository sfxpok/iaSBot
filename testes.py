#!/usr/bin/env python3

from ev3dev2.sound import Sound
from ev3dev2.display import Display
import ev3dev2.fonts as fonts
from time import sleep

lcd = Display()
sound = Sound()

def drawCircle():
    drawing = Display()
    drawing.circle(True, 50, 50, 40)        
    
def show_for(seconds):
    lcd.update()
    sound.beep()
    sleep(seconds)
    lcd.clear()

def basicDrawing():
    # Try each of these different sets:
    style = 'helvB'
    #style = 'courB'
    #style = 'lutBS'

    y_value = 0
    str1 = ' The quick brown fox jumped'
    str2 = '123456789012345678901234567890'
    for height in [10, 14, 18, 24]:
        text = style+str(height)+str1
        lcd.text_pixels(text, False, 0, y_value, font=style+str(height))
        y_value += height+1   # short for  y_value = y_value+height+1
        lcd.text_pixels(str2, False, 0, y_value, font=style+str(height))
        y_value += height+1
    show_for(6)

def drawGameMap():

    # EV3 display resolution: 178x128
    # Rectangle resolution: 29x21

    lcd = Display()
    sound = Sound()

    for vertex in range(0, 5):
        coordX1 = 0+29*vertex
        coordY1 = 0+21*vertex
        coordX2 = coordX1+29
        coordY2 = coordY1+21
        lcd.rectangle(False, coordX1, coordY1, coordX2, coordY2, fill_color=None)
        #lcd.update()

    show_for(6)

def drawGameMapNoFor():
    # EV3 display resolution: 178x128
    # Rectangle resolution: 29x21

    lcd = Display()
    sound = Sound()

    lcd.rectangle(False, 29, 42, 58, 21, fill_color='grey')
    lcd.update()
    lcd.rectangle(False, 29, 42, 109, 105, fill_color='grey')
    lcd.update()
    lcd.rectangle(False, 58, 63, 109, 105, fill_color='grey')
    lcd.update()

    show_for(6)

style = 'helvB'
posX = 2
posY = 7
#usedFont = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 75)
#lcd.draw.text((3,0), 'Hello', font=style)
#lcd.draw.text_pixels("SB: (" + posX + "," + posY + ")", False, 50, 50, text_color='black', font=style)
#lcd.draw.text_grid("SB: (3,3)", False, 50, 50, text_color='black', font=style)
lcd.draw.text((10,10), "SB: (" + str(posX) + "," + str(posY) + ")", font=fonts.load('luBS14'))
show_for(5)

#lcd.rectangle(False, 0, 0, 29, 21, fill_color=None)
#lcd.rectangle(False, 29, 21, 58, 42, fill_color=None)
#lcd.rectangle(False, 58, 42, 87, 63, fill_color=None)
#lcd.rectangle(False, 87, 63, 116, 84, fill_color=None)
#lcd.rectangle(False, 116, 84, 145, 105, fill_color=None)
#lcd.rectangle(False, 145, 105, 174, 126, fill_color=None)
#show_for(6)

#drawGameMap()

def updateScreen(posX, posY):
    lcd = Display()
    updateWarning = Sound()

    lcd.draw.text((10,10), "SB: (" + str(posX) + "," + str(posY) + ")", font=fonts.load('luBS14'))

    lcd.update()
    updateWarning.beep()
    sleep(5)
    #lcd.clear()

updateScreen(2,4)