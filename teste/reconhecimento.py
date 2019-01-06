from ev3dev2.sensor.lego import ColorSensor
from Motor import MoveTank


def checkColor():
    color = ColorSensor().color_name
    return color

def recognize(): #done
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
        a.engine.on(20,20)
        while ColorSensor().color_name != 'Black':
            pass
        a.engine.off()
        color = [None] * 3
        a.movementDeg(91)
        color[0] = checkColor()
        a.movementDeg(182)
        color[1] = checkColor()
        a.movementDeg(182)
        color[2] = checkColor()

        a.movementDeg(-727)
        return color    

