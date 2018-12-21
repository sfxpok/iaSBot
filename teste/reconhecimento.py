from ev3dev2.sensor.lego import ColorSensor
from Motor import MoveTank


def checkColor():
    color = ColorSensor().color_name
    return color

def recognize():
        ###
        # Distance between squares:
        #Motor A = 1139
        #Motor B = 1128
        #to implement 31cm = 1134
        # 15.5 = 567
        # 16 = 585
        # 17 = 621
        # 18 = 658 
        ###
        ColorSensor().calibrate_white()
        a = MoveTank()
        #if self.checkInvalidPositions():
        a.movementDeg(585)
        a.speed = 5
        color = [None]*3
        for i in range(3):
            a.movementDeg(130)
            color[i] = checkColor()
            print('color: ' + str(i) + ' '+ color[i])
        a.speed = 25
        a.movementDeg(-975)
        return color    

