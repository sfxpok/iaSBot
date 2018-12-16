from ev3dev2.sensor.lego import ColorSensor

class ColorDetector():
    def __init__(self, inputSensor):
        self.inputSensor = ColorSensor(inputSensor)
        self.red = ColorSensor().red # [0, 1020]
        self.green = ColorSensor().green # [0, 1020]
        self.blue = ColorSensor().blue # [0, 1020]

        self.red_max = 300
        self.green_max = 300
        self.blue_max = 300

    def getRed(self):
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
        self.blue = blue

    def raw(self):
        return self.value(0), self.value(1), self.value(2)

    def calibrateWhite(self):
        (self.red_max, self.green_max, self.blue_max) = self.raw

    def convertToRGB(self):
        self.setRed(min(int((self.getRed() * 255) / self.red_max), 255))
        self.setGreen(min(int((self.getGreen() * 255) / self.green_max), 255))
        self.setBlue(min(int((self.getBlue() * 255) / self.blue_max), 255))

def checkColor():
    color = ColorSensor().color_name
    # print(color)
    return color

                