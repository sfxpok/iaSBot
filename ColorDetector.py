from ev3dev2.sensor.lego import ColorSensor

class ColorDetector():
    def __init__(self):
        self.calibrateColor = self.calibrateWhite()

        #self.white = (255, 217, 147) # 619
        #self.red = (182, 20, 12) # 214
        #self.brown = (61, 22, 11) # 94
        #self.yellow = (255, 107, 19) # 381
        #self.blue = (41, 108, 100) # 249
        #self.black = (28, 22, 17) # 67
        #self.darkGreen = (29, 42, 17) # 88
        #self.green = (72, 124, 34) # 230

    def getRGB(self):
        return ColorSensor().rgb

    def calibrateWhite(self): # use this function at the beginning of the game
        return ColorSensor().calibrate_white

    def getColor(self):
        rgb = self.getRGB()

        if (sum(rgb) == 0):
            return 'No Color'

        if (rgb[0] > 200):
            if (rgb[1] > 180):
                return 'White'
            else:
                return 'Yellow'
        
        if (rgb[0] > 100):
           return 'Red'

        if (rgb[1] > 90 and rgb[2] > 90):
            return 'Blue'

        if (rgb[1] > 100 and rgb[2] < 50):
            return 'Green'

        if (rgb[0] > 50 and rgb[2] < 30):
            return 'Brown'

        return 'Black'