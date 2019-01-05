from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_3

class ColorDetector():
    def __init__(self):
        #self.inputSensor = ColorSensor.ColorDetector(INPUT_3)
        self.calibrateColor = self.calibrateWhite()
        self.red = ColorSensor().red # [0, 1020]
        self.green = ColorSensor().green # [0, 1020]
        self.blue = ColorSensor().blue # [0, 1020]

        # default values
        self.red_max = 300
        self.green_max = 300
        self.blue_max = 300

        self.white = (255, 217, 147) # 619
        self.red = (182, 20, 12) # 214
        self.brown = (61, 22, 11) # 94
        self.yellow = (255, 107, 19) # 381
        self.blue = (41, 108, 100) # 249
        self.black = (28, 22, 17) # 67
        #self.darkGreen = (29, 42, 17) # 88
        self.green = (72, 124, 34) # 230

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

""" def getRed(self):
        return self.red

    def getGreen(self):
        return self.green
    
    def getBlue(self):
        return self.blue

    def setRed(self, red):
        self.red = red

    def setGreen(self, green):
        self.green = green

    def setBlue(self, blue):
        self.blue = blue """

"""     def convertToRGB(self): # returns RGB within an interval of 0 to 255
        self.setRed(min(int((self.getRed() * 255) / self.red_max), 255))
        self.setGreen(min(int((self.getGreen() * 255) / self.green_max), 255))
        self.setBlue(min(int((self.getBlue() * 255) / self.blue_max), 255)) """